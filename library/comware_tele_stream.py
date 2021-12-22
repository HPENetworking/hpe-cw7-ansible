#!/usr/bin/python

DOCUMENTATION = """
---

module: comware_tele_stream
short_description: Manage telemetry global enable(disable) and telemetry stream timestamp enable(disable) and device-id 
                   on Comware 7 devices.Before config device-id,the timestamp must be enable.
version_added: 1.0
category: Feature (RW)
author: gongqianyu
options:
    glo_enable:
        description:
            - config global telemetry stream enable.The default state is enable.
        required: false
        default: enable
        choices: ['enable', 'disable']
        aliases: []
    timestamp:
        description:
            - config telemetry stream timestamp enable.The default state is disable.
        required: false
        default: disable
        choices: ['enable', 'disable']
        aliases: []
	device-id
        description:
            - config telemetry stream device-id.
        required: false
        default: null
        choices: []
        aliases: []
    state:
        description:
            - Recovering the dufault state of telemetry stream
        required: false
        default: present
        choices: ['present', 'default']
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

  # telemetry config
  - comware_tele_stream:
      glo_enable: enable
      timestamp: enable
	  deviceID: 10.10.10.1
      username: "{{ username }}"
      password: "{{ password }}"
      hostname: "{{ inventory_hostname }}"
      state: present

"""

import socket
try:
    HAS_PYHP = True
    from pyhpecw7.features.tele_stream import Telemetry
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
            timestamp = dict(required=False, choices=['enable', 'disable'], default='disable'),
            glo_enable =dict(required=False, choices=['enable', 'disable'], default='enable'),
            deviceID = dict(required=False, type='str'),
            state = dict(required=False, choices=['present', 'default'], default='present'),
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

    timestamp = module.params['timestamp']
    glo_enable = module.params['glo_enable']
    state = module.params['state']
    deviceID = module.params['deviceID']


    changed = False

    args = dict(timestamp=timestamp, glo_enable=glo_enable, deviceID=deviceID)

    proposed = dict((k, v) for k, v in args.items() if v is not None)

    try:
        look_for_keys = module.params['look_for_keys']
        device.open(look_for_keys=look_for_keys)
    except ConnectionError as e:
        safe_fail(module, device, msg=str(e),
                  descr='error connecting to device')

    try:
        telemetry = Telemetry(device)
#        existing = telemetry.get_config()
    except PYHPError as e:
        safe_fail(module, device, msg=str(e))

    if state == 'present':
        telemetry.build(stage=True,timestamp=timestamp,glo_enable=glo_enable, deviceID=deviceID)

    elif state == 'default':
        telemetry.remove(stage=True,timestamp=timestamp,glo_enable=glo_enable, deviceID=deviceID)

    commands = None
#    end_state = existing

    if device.staged:
        commands = device.staged_to_string()
        if module.check_mode:
            safe_exit(module, device, changed=True,
                      commands=commands)
        else:
            try:
                device.execute_staged()
 #               end_state = telemetry.get_config()
            except PYHPError as e:
                safe_fail(module, device, msg=str(e),
                          descr='error during execution')
            changed = True


    results = {}
    results['proposed'] = proposed
    results['state'] = state
    results['commands'] = commands
    results['changed'] = changed
#    results['end_state'] = end_state

    safe_exit(module, device, **results)

from ansible.module_utils.basic import *
main()
