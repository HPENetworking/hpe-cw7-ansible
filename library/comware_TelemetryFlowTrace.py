#!/usr/bin/python

DOCUMENTATION = """
---

module: comware_TelemetryFlowTrace
short_description: Manage Package information of the message sent to the collector on V7 devices
version_added: 1.0
author: gongqianyu
category: Feature (RW)
notes:
    - If state=absent, the config will be removed
options:
    sourceID:
        description:
            - The source IP address of the packet package of the uplink collector
        required: True
        default: null
        choices: []
        aliases: []
    destinID:
        description:
            - Destination IP address of the packet package of the uplink collector
        required: True
        default: null
        choices: []
        aliases: []
    sourcePort:
        description:
            - The source port number of the message package of the up sending collector.
        required: True
        default: null
        choices: []
        aliases: []
    destinPort:
        description:
            - Destination port number of the message package of the uplink collector.
        required: True
        default: null
        choices: []
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
- comware_TelemetryFlowTrace: sourceID=10.10.10.1 destinID=10.10.10.2 sourcePort=10 destinPort=30 username={{ username }} 
   password={{ password }} hostname={{ inventory_hostname }}

# delete config
 -comware_TelemetryFlowTrace: sourceID=10.10.10.1 destinID=10.10.10.2 sourcePort=10 destinPort=30 state=absent 
   username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

"""

import socket

try:
    HAS_PYHP = True
    from pyhpecw7.comware import HPCOM7
    from pyhpecw7.features.TelemetryFlowTrace import Telemetry
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
            sourceID=dict(required=True, type = 'str'),
            destinID=dict(required=True, type = 'str'),
            sourcePort=dict(required=True, type = 'str'),
            destinPort=dict(required=True, type = 'str'),

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

    filtered_keys = ('state', 'hostname', 'username', 'password',
                     'port', 'CHECKMODE', 'look_for_keys')

    hostname = socket.gethostbyname(module.params['hostname'])
    username = module.params['username']
    password = module.params['password']
    port = module.params['port']

    device = HPCOM7(host=hostname, username=username,
                    password=password, port=port)

    sourceID = module.params['sourceID']
    destinID = module.params['destinID']
    sourcePort = module.params['sourcePort']
    destinPort = module.params['destinPort']

    state = module.params['state']

    args = dict(sourceID=sourceID, destinID=destinID, sourcePort=sourcePort, destinPort=destinPort)
    proposed = dict((k, v) for k, v in args.items() if v is not None)
    changed = False

    try:
        look_for_keys = module.params['look_for_keys']
        device.open(look_for_keys=look_for_keys)
    except ConnectionError as e:
        safe_fail(module, device, msg=str(e),
                  descr='Error opening connection to device.')

    try:

        telemetry = Telemetry(device, sourceID, destinID, sourcePort, destinPort)
 #       telemetry.param_check(**proposed)
    #        telemetry = Telemetry(device)
    except PYHPError as e:
        safe_fail(module, device, msg=str(e))

    try:
        existing = telemetry.get_config()
    except PYHPError as e:
        safe_fail(module, device, msg=str(e),
                  descr='Error getting telemetry config.')

    if state == 'present':
#        delta = dict(set(proposed.iteritems()).difference(
#            existing.iteritems()))
#        if delta:
        telemetry.build(stage=True)

    elif state == 'absent':
        if existing:
            telemetry.remove(stage=True)

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
                end_state = telemetry.get_config()
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
