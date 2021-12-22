#!/usr/bin/python


DOCUMENTATION = """
---

module: comware_isis_global
short_description: Manage isis for Comware 7 devices
author:gongqianyu
version_added: 1.0
category: Feature (RW)
options:
    isisID:
        description:
            - create isis process
        required: true
        default: null
        choices: []
        aliases: []
    level:
        description:
            - Configure the level of the router,the default value is Level-1-2.
        required: false
        default: Level-1-2
        choices: ['level-1', 'level-1-2', 'level-2']
        aliases: []
    cost_style:
        description:
            - Configure the type of IS-IS overhead value, that is, 
            the type of destination path overhead value in the message received and sent by IS-IS.
        required: false
        default: narrow
        choices: ['narrow', 'wide', 'wide-compatible', 'compatible', 'narrow-compatible']
        aliases: []
    spf_limit:
        description:
            - Indicates that it is allowed to receive a message with a destination path overhead value 
             greater than 1023. If this parameter is not specified, a message with an overhead value greater than 
             1023 will be discarded. This parameter is optional only when compatible or narrow compatible is specified.
        required: false
        default: null
        choices: ['true', 'false']
        aliases: []
    network:
        description:
            - Network entity name of the configuration IS-IS process(X...X.XXXX....XXXX.00)
        required: false
        default: null
        choices: []
        aliases: []
    add_family:
        description:
            - Create IS-IS IPv4 or IPV6 address family and enter IS-IS IPv4 address family view
        required: false
        default: null
        choices: ['ipv4', 'ipv6']
        aliases: []
    preference:
        description:
            - Configure routing priority of IS-IS protocol(1~225),before config it,you need to 
              config add_family first.
        required: false
        default: 15
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
    state:
        description:
            - Desired state of the vlan
        required: false
        default: present
        choices: ['present', 'absent']
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

# create sisi 4 and releated params.
- comware_isis_global: isisID=4 level=level-2 cost_style=narrow-compatible spf_limit=true network=10.0001.1010.1020.1030.00 
                add_family=ipv4 preference=25 state=present username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

# delete isis 4
- comware_isis_global: isisID=4 level=level-2 cost_style=narrow-compatible spf_limit=true network=10.0001.1010.1020.1030.00 
                add_family=ipv4 preference=25 state=absent username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

"""

import socket
try:
    HAS_PYHP = True
    from pyhpecw7.features.isis_global import Isis
    from pyhpecw7.features.isis_global import ISis
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
            isisID=dict(required=True, type='str'),
            level=dict(required=False, choices=['level-1', 'level-1-2', 'level-2'], default='level-1-2'),
            cost_style=dict(required=False, choices=['narrow', 'wide', 'wide-compatible', 'compatible', 'narrow-compatible']),
            spf_limit=dict(required=False, choices=['true', 'false']),
            network=dict(required=False),
            add_family = dict(required=False, choices=['ipv4', 'ipv6']),
            preference=dict(required=False),
            state=dict(choices=['present', 'absent'], default='present'),
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

    isisID = module.params['isisID']
    cost_style = module.params['cost_style']
    spf_limit = module.params['spf_limit']
    network = module.params['network']
    add_family = module.params['add_family']
    level = module.params['level']
    preference = module.params['preference']
    state = module.params['state']

    changed = False

    args = dict(isisID=isisID, network=network, level=level, cost_style=cost_style,  spf_limit=spf_limit, preference=preference, add_family=add_family)

    proposed = dict((k, v) for k, v in args.items() if v is not None)

    try:
        look_for_keys = module.params['look_for_keys']
        device.open(look_for_keys=look_for_keys)
    except ConnectionError as e:
        safe_fail(module, device, msg=str(e))

    try:

        isis = Isis(device, isisID)
        iSis = ISis(device, isisID, level, cost_style, spf_limit, preference, add_family, network)
    #     isis.param_check(**proposed)
    except PYHPError as e:
        safe_fail(module, device, msg=str(e))

    try:
        existing = isis.get_config()
    except PYHPError as e:
        safe_fail(module, device, msg=str(e),
                  descr='error getting isis config')

    if state == 'present':
        delta = dict(set(proposed.items()).difference(
            existing.items()))
        if delta:
            if module.params['network'] or module.params['cost_style'] or module.params['preference'] or module.params['spf_limit'] or module.params['add_family'] or module.params['level']:
                iSis.build(stage=True)
            else:
                isis.build(stage=True, **delta)
    elif state == 'absent':
        if existing:
            isis.remove(stage=True)

    commands = None
    end_state = existing

    if device.staged:
        commands = device.staged_to_string()
        if module.check_mode:
            device.close()
            safe_exit(module, device, changed=True,
                      commands=commands)
        else:
            try:
                device.execute_staged()
                end_state = isis.get_config()
            except PYHPError as e:
                safe_fail(module, device, msg=str(e),
                          descr='error during execution')
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
