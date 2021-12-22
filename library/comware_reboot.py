#!/usr/bin/python

DOCUMENTATION = """
---

module: comware_reboot
short_description: Perform a reboot of a Comware 7 device
description:
    - Offers ability to reboot Comware 7 devices instantly
      at a scheduled time, or after a given period of time
version_added: 1.8
category: System (RW)
notes:
    - Time/date and delay are mutually exclusive parameters
    - Time is required when specifying date
    - Reboot must be set to true to reboot the device
    - This module is not idempotent
options:
    reboot:
        description:
            - Needs to be set to true to reboot the device
        required: true
        default: null
        choices: ['true', 'false']
        aliases: []
    time:
        description:
            - Specify the time at which the reboot will take place.
              Format should be HH:MM enclosed in quotes.
        required: false
        default: null
        choices: []
        aliases: []
    date:
        description:
            - Specify the date at which the reboot will take place.
              The time parameter is required to use this parameter.
              Format should be MM/DD/YYYY in quotes.
        required: false
        default: null
        choices: []
        aliases: []
    delay:
        description:
            - Delay (in minutes) to wait to reboot the device
        required: false
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
    hostname:
        description:
            - IP Address or hostname of the Comware v7 device that has
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

# name: reboot immedidately
- comware_reboot: reboot=true username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

# name: reboot at 5:00
- comware_reboot: reboot=true time="05:00" username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

# name: reboot in 5 minutes
- comware_reboot: reboot=true delay="05:00" username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

# name: reboot at 22:00 on July 30 2015
- comware_reboot: reboot=true time="22:00" date="07/10/2015" username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

"""

import socket
try:
    HAS_PYHP = True
    from pyhpecw7.features.reboot import Reboot
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
            reboot=dict(required=True, choices=BOOLEANS, type='bool'),
            delay=dict(required=False, type='str'),
            date=dict(required=False, type='str'),
            time=dict(required=False, type='str'),
            port=dict(default=830, type='int'),
            hostname=dict(required=True),
            username=dict(required=True),
            password=dict(required=False, default=None),
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

    reboot = module.params['reboot']
    delay = module.params['delay']
    date = module.params['date']
    time = module.params['time']

    if date:
        if not time:
            module.fail_json(msg='time is also required when specifying date')

    proposed = dict(reboot=reboot, delay=delay,
                    time=time, date=date)

    changed = False

    try:
        look_for_keys = module.params['look_for_keys']
        device.open(look_for_keys=look_for_keys)
    except ConnectionError as e:
        safe_fail(module, device, msg=str(e),
                  descr='error opening connection to device')

    try:
        reboot_me = Reboot(device)
        reboot_me.param_check(**proposed)
    except RebootDateError as rde:
        safe_fail(module, device, msg=str(rde))
    except RebootTimeError as rte:
        safe_fail(module, device, msg=str(rte))
    except PYHPError as e:
        safe_fail(module, device, msg=str(e),
                  descr='error using Reboot object')

    reboot_me.build(stage=True, **proposed)

    commands = None
    response = None
    changed = False

    results = {}

    if device.staged:
        commands = device.staged_to_string()
        if module.check_mode:
            safe_exit(module, device, changed=True,
                      commands=commands)
        else:
            try:
                response = device.execute_staged()
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

    results['proposed'] = proposed
    results['commands'] = commands
    results['changed'] = changed
    results['end_state'] = 'N/A for this module'
    results['response'] = response

    safe_exit(module, device, **results)

from ansible.module_utils.basic import *
main()
