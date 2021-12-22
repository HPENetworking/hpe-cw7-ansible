#!/usr/bin/python

DOCUMENTATION = """
---

module: comware_log_source
short_description: Manage output rules for log information on V7 devices
version_added: 1.0
author: gongqianyu
category: Feature (RW)
notes:
    - If state=default, the config will be removed
options:
    channelID:
        description:
            - Specifies syslog output destination
        required: True
        default: null
        choices: ['1', '2', '3', '4', '5'] 1:Console 2:Monitor terminal 3:Log buffer 4:Log host 5:Log file
        aliases: []
    channelName:
        description:
            - Specifies a module by its name.
        required: True
        default: null
        choices: []
        aliases: []
    level:
        description:
            - A log output rule specifies the source modules and severity level of logs that can be output to a destination. Logs matching the output rule are output to the destination.
        required: False
        default: null
        choices: ['emergency', 'alert', 'critical', 'error', 'warning', 'notification', 'informational', 'debugging', 'deny']
        aliases: []
    state:
        description:
            - Desired state of the switchport
        required: false
        default: present
        choices: ['present', 'absent']
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
"""
EXAMPLES = """

# basic config
- comware_log_source: channelID=1 channelName=ARP level=critical username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

# delete config
- comware_log_source: channelID=1 channelName=ARP level=critical state=absent username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

"""


import socket

try:
    HAS_PYHP = True
    from pyhpecw7.comware import HPCOM7
    from pyhpecw7.features.syslog import Source
    from pyhpecw7.errors import PYHPError
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
            channelID = dict(required=True, type = 'str', choices=['1', '2', '3', '4', '5']),
            channelName = dict(required=True, type = 'str'),
            level = dict(required=False, type = 'str', choices=['emergency', 'alert', 'critical', 'error', 'warning', 'notification', 'informational', 'debugging', 'deny']),

            state=dict(required=False, choices=['present', 'absent'],
                       default='present'),
            hostname=dict(required=True),
            username=dict(required=True),
            password=dict(required=False, default=None),
            port=dict(type='int', default=830),
            look_for_keys=dict(default=False, type='bool'),
        ),
        supports_check_mode=True
    )

    if not HAS_PYHP:
        safe_fail(module,
                  msg='There was a problem loading from the pyhpecw7 module')

#    filtered_keys = ('state', 'hostname', 'username', 'password',
#                     'port', 'CHECKMODE', 'look_for_keys')

    hostname = socket.gethostbyname(module.params['hostname'])
    username = module.params['username']
    password = module.params['password']
    port = module.params['port']

    device = HPCOM7(host=hostname, username=username,
                    password=password, port=port)

    channelID = module.params['channelID']
    channelName = module.params['channelName']
    level = module.params['level']

    state = module.params['state']

    args = dict(channelID=channelID, channelName=channelName, level=level)
    proposed = dict((k, v) for k, v in args.items() if v is not None)
    changed = False

    try:
        look_for_keys = module.params['look_for_keys']
        device.open(look_for_keys=look_for_keys)
    except ConnectionError as e:
        safe_fail(module, device, msg=str(e),
                  descr='Error opening connection to device.')

    try:
        SOURCE = Source(device, channelID, channelName, level)

    except LengthOfStringError as lose:
        safe_fail(module, device, msg=str(lose))
    except VlanIDError as vie:
        safe_fail(module, device, msg=str(vie))
    except PYHPError as e:
        safe_fail(module, device, msg=str(e))

    try:
        existing = SOURCE.get_config()
    except PYHPError as e:
        safe_fail(module, device, msg=str(e),
                  descr='Error getting syslog source config.')

    if state == 'present':
        delta = dict(set(proposed.items()).difference(
            existing.items()))
        if delta:
            SOURCE.build(stage=True)

    elif state == 'absent':
        if existing:
            SOURCE.remove(stage=True)

    commands = None
    end_state = existing

    if device.staged:
        commands = device.staged_to_string()
        if module.check_mode:
            safe_exit(module, device, changed=True,
                      commands=commands)
        else:
            try:
                device.execute_staged()
                end_state = SOURCE.get_config()
            except PYHPError as e:
                safe_fail(module, device, msg=str(e),
                          descr='Error during command execution.')
            changed = True

    results = {}
    results['proposed'] = proposed
    results['existing'] = existing
    results['state'] = state
    results['commands'] = commands
    results['changed'] = changed
    results['end_state'] = end_state

    safe_exit(module, device, **results)

from ansible.module_utils.basic import *
main()
