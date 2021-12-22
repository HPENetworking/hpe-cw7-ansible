#!/usr/bin/python

DOCUMENTATION = """
---

module: comware_clean_erase
short_description: Factory default HP Comware 7 device
description:
    - Reset system to factory default settings.  You will
      lose connectivity to the switch.  This module deletes all configuration
      files (.cfg files) in the root directories of the storage media.
      It deletes all log files (.log files in the folder /logfile). Clears
      all log information (in the log buffer), trap information, and debugging
      information. Restores the parameters for the Boot ROM options to the
      factory-default settings. Deletes all files on an installed
      hot-swappable storage medium, such as a USB disk
version_added: 1.8
category: System (RW)
options:
    factory_default:
        description:
            - Set to true if all logs and user-created files
              should be deleted and removed from the system
              and the device should be set to factory default
              settings
        required: true
        default: null
        choices: ['true', 'false']
        aliases: []
    port:
        description:
            - NETCONF port number
        required: false
        default: 830
        choices: []
        aliases: []
    hostname:
        description:
            - IP Address or hostname of the Comware 7 device that has
              NETCONF enabled
        required: true
        default: null
        choices: []
        aliases: []
    username:
        description:
            - Username used to login to the switch
        required: true
        default: null
        choices: []
        aliases: []
    password:
        description:
            - Password used to login to the switch
        required: true
        default: null
        choices: []
        aliases: []
    look_for_keys:
        description:
            - Whether searching for discoverable private key files in ~/.ssh/
        required: false
        default: False
        choices: []
        aliases: []

"""
EXAMPLES = """

# factory default and reboot immediately
- comware_clean_erase: factory_default=true username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

"""

import socket
try:
    HAS_PYHP = True
    from pyhpecw7.features.cleanerase import CleanErase
    from pyhpecw7.comware import HPCOM7
    from pyhpecw7.features.errors import *
    from pyhpecw7.errors import *
except ImportError as ie:
    HAS_PYHP = False


def safe_fail(module, device=None, **kwargs):
    if device:
        device.close()
    module.fail_json(**kwargs)


def safe_exit(module, device=None, **kwargs):
    if device:
        device.close()
    module.exit_json(**kwargs)


def main():
    module = AnsibleModule(
        argument_spec=dict(
            factory_default=dict(default=False, choices=BOOLEANS, type='bool'),
            port=dict(default=830, type='int'),
            hostname=dict(required=True),
            username=dict(required=True),
            password=dict(required=False, default=None),
            look_for_keys=dict(default=False, type='bool'),
        ),
        supports_check_mode=True
    )

    if not HAS_PYHP:
        safe_fail(module, msg='There was a problem loading from the pyhpecw7 '
                  + 'module.', error=str(ie))

    username = module.params['username']
    password = module.params['password']
    port = module.params['port']
    hostname = socket.gethostbyname(module.params['hostname'])

    device_args = dict(host=hostname, username=username,
                       password=password, port=port)

    device = HPCOM7(**device_args)

    factory_default = module.params['factory_default']
    try:
        look_for_keys = module.params['look_for_keys']
        device.open(look_for_keys=look_for_keys)
    except ConnectionError as e:
        safe_fail(module, device, msg=str(e),
                  descr='error opening connection to device')

    try:
        cleanerase = CleanErase(device)
    except PYHPError as e:
        safe_fail(module, device, msg=str(e),
                  descr='error initializing CleanErase')

    if factory_default:
        cleanerase.build(stage=True, factory_default=factory_default)

    results = {}
    results['changed'] = False
    results['rebooted'] = False
    results['commands'] = None

    if device.staged:
        commands = device.staged_to_string()
        if module.check_mode:
            safe_exit(module, device, changed=True,
                      commands=commands)
        else:
            try:
                device.execute_staged()
                changed = True
            except PYHPError as e:
                if isinstance(e, NCTimeoutError):
                    results['changed'] = True
                    results['rebooted'] = True
                    results['commands'] = commands
                    module.exit_json(**results)
                else:
                    safe_fail(module, device, msg=str(e),
                              descr='error during execution')

    safe_exit(module, device, **results)

from ansible.module_utils.basic import *
main()
