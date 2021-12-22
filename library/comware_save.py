#!/usr/bin/python


DOCUMENTATION = '''
---

module: comware_save
short_description: Save the running configuration
description:
    - Save the running configuration
version_added: 1.8
category: System (RW)
notes:
    - This modules saves the running config as startup.cfg, or the supplied
      filename, in flash. It is not
      changing the config file to load on next boot.
options:
    filename:
        description:
            - Name of file that will be used when saving the current
              running conifg to flash.
        required: false
        default: startup.cfg
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
    port:
        description:
            - NETCONF port number
        required: false
        default: 830
        choices: []
        aliases: []
    look_for_keys:
        description:
            - Whether searching for discoverable private key files in ~/.ssh/
        required: false
        default: False
        choices: []
        aliases: []

'''
EXAMPLES = '''

# save as myfile.cfg (in flash)
- comware_save: filename=myfile.cfg username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

# save as startup.cfg (in flash)
- comware_save: username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

'''

import socket
try:
    HAS_PYHP = True
    from pyhpecw7.comware import HPCOM7
    from pyhpecw7.features.errors import *
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
            filename=dict(required=False, default='startup.cfg'),
            port=dict(default=830, type='int'),
            hostname=dict(required=True),
            username=dict(default='hp'),
            password=dict(default='hp123'),
            look_for_keys=dict(default=False, type='bool'),
        ),
        supports_check_mode=True
    )
    if not HAS_PYHP:
        module.fail_json(msg='There was a problem loading from the pyhpecw7 '
                         + 'module.', error=str(ie))

    username = module.params['username']
    password = module.params['password']
    port = module.params['port']
    hostname = socket.gethostbyname(module.params['hostname'])

    device_args = dict(host=hostname, username=username,
                       password=password, port=port)

    device = HPCOM7(**device_args)

    filename = module.params['filename']

    if "/" in filename:
        module.fail_json(msg="specify only filename. it'll be saved in flash")
    if filename[-4:] != '.cfg':
        module.fail_json(msg='filename should end with .cfg')

    changed = False

    try:
        look_for_keys = module.params['look_for_keys']
        device.open(look_for_keys=look_for_keys)
    except ConnectionError as e:
        safe_fail(module, device, msg=str(e),
                  descr='error opening connection to device')

    device.stage_config('{0}'.format(filename), "save")

    if device.staged:
        commands = device.staged_to_string()
        if module.check_mode:
            safe_exit(module, device, changed=True,
                      commands=commands)
        else:
            try:
                device.execute_staged()
            except PYHPError as e:
                safe_fail(module, device, msg=str(e),
                          descr='error during execution')
            changed = True

    results = {}
    results['commands'] = commands
    results['changed'] = changed

    safe_exit(module, device, **results)

from ansible.module_utils.basic import *
main()
