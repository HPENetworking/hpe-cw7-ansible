#!/usr/bin/python

DOCUMENTATION = """
---

module: comware_loghost
short_description: Manage info-center log host and related parameters on V7 devices
version_added: 1.0
author: gongqianyu
category: Feature (RW)
notes:
    - 
options:
    loghost:
        description:
            - Address of the log host
        required: True
        default: null
        choices: []
        aliases: []
    VRF:
        description:
            - VRF instance name
        required: True
        default: null
        choices: []
        aliases: []
    hostport:
        description:
            - Port number of the log host.
        required: False
        default: 514
        choices: []
        aliases: []
    facility:
        description:
            - Logging facility used by the log host.
        required: False
        default: 184
        choices: ['128', '136', '144', '152', '160', '168', '176', '184'] 128:local0, 136:local1 144:local2 152:local3 160:local4
		          168:local5 176:local6 184:local7
        aliases: []
	sourceID:
        description:
            - Configure the source IP address of the sent log information.The default state is Using the primary IP address of the outgoing interface as the source IP address of the sent log information
        required: False
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
- comware_loghost: loghost=3.3.3.7 VRF=vpn2 hostport=512 facility=128 sourceID=LoopBack0 username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

# delete config
- comware_loghost: loghost=3.3.3.7 VRF=vpn2 hostport=512 facility=128 sourceID=LoopBack0 state=absent username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

"""

import socket

try:
    HAS_PYHP = True
    from pyhpecw7.comware import HPCOM7
    from pyhpecw7.features.syslog import Loghost
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
            loghost=dict(required=True, type = 'str'),
            VRF=dict(required=True, type = 'str'),
            hostport=dict(required=False, type = 'str', default='514'),
            facility=dict(required=False, choices=['128', '136', '144', '152', '160', '168', '176','184'], type = 'str', default='184'),
            sourceID = dict(required=False, type = 'str'),
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

    loghost = module.params['loghost']
    VRF = module.params['VRF']
    hostport = module.params['hostport']
    facility = module.params['facility']
    sourceID = module.params['sourceID']

    state = module.params['state']

    args = dict(loghost=loghost, VRF=VRF, hostport=hostport, facility=facility, sourceID=sourceID)
    proposed = dict((k, v) for k, v in args.items() if v is not None)
    changed = False

    try:
        look_for_keys = module.params['look_for_keys']
        device.open(look_for_keys=look_for_keys)
    except ConnectionError as e:
        safe_fail(module, device, msg=str(e),
                  descr='Error opening connection to device.')

    try:

        LOGhost = Loghost(device, loghost, VRF, hostport, facility)

    except PYHPError as e:
        safe_fail(module, device, msg=str(e))

    try:
        existing = LOGhost.get_config()
    except PYHPError as e:
        safe_fail(module, device, msg=str(e),
                  descr='Error getting loghost config.')

    if state == 'present':
        delta = dict(set(proposed.items()).difference(
            existing.items()))
        if delta:
            LOGhost.build(stage=True)
        if module.params.get('sourceID'):
            LOGhost.build_time(stage=True, sourceID=sourceID)

    elif state == 'absent':
        if existing:
            LOGhost.remove(stage=True)
        if module.params.get('sourceID'):
            LOGhost.build_time_absent(stage=True, sourceID=sourceID)

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
                end_state = LOGhost.get_config()
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
