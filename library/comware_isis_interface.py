#!/usr/bin/python


DOCUMENTATION = """
---

module: comware_isis_interface
short_description: Manage isis for Comware 7 devices
author:gongqianyu
version_added: 1.0
category: Feature (RW)
options:
    name:
        description:
            - interface name
        required: true
        default: null
        choices: []
        aliases: []
    isisID:
        description:
            - cSpecifies that IS-IS functions are enabled on the interface and configures the IS-IS 
               processes associated with the interface
        required: true
        default: null
        choices: []
        aliases: []
    level:
        description:
            - Link adjacency type of configuration interface.
        required: false
        default: 3
        choices: ['1', '2', '3']  1:Level 1, 2:Level 2, 3:Level-1-2
        aliases: []
    cost:
        description:
            - Configure the link cost value of IS-IS interface.(1～16777215)
        required: false
        default: null
        choices: []
        aliases: []
    routerid:
        description:
            - Configure the link cost value of IS-IS interface,to chose router.
        required: false
        default: null
        choices: ['level-1', 'level-2']
        aliases: []
    silent:
        description:
            - Forbid the interface to send and receive IS-IS message.
        required: false
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
- comware_isis_interface: name=vlan-interface30 isisID=4 level=2 networkType=p2p cost=5 routerid=level-2 silent=true state=present 
                username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

# delete isis 4
- comware_isis_interface: name=vlan-interface30 isisID=4 level=2 networkType=p2p cost=5 routerid=level-2 silent=true state=absent 
                username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

"""

import socket
try:
    HAS_PYHP = True
    from pyhpecw7.features.isis_interface import Isis
    from pyhpecw7.features.isis_interface import ISis
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
            name=dict(required=True),
            # enable=dict(required=False),
            isisID=dict(required=True, type='str'),
            level=dict(required=False, choices=['level-1', 'level-2', 'level-1-2']),
            networkType=dict(required=False, choices=['p2p']),
            cost=dict(required=False),
            routerid=dict(required=False, choices=['level-1', 'level-2']),
            silent=dict(required=False, choices=['true', 'false']),
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

    name = module.params['name']
    isisID = module.params['isisID']
    level = module.params['level']
    cost = module.params['cost']
    routerid = module.params['routerid']
    networkType = module.params['networkType']
    silent = module.params['silent']
    state = module.params['state']

    changed = False

    args = dict(name=name, isisID=isisID, level=level, cost=cost, routerid=routerid, networkType=networkType, silent=silent)
    proposed = dict((k, v) for k, v in args.items() if v is not None)

    try:
        look_for_keys = module.params['look_for_keys']
        device.open(look_for_keys=look_for_keys)
    except ConnectionError as e:
        safe_fail(module, device, msg=str(e))

    try:

        isis = Isis(device, name)
        iSis = ISis(device, name, isisID, level, cost, routerid, networkType, silent)
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
            if module.params['cost'] or module.params['routerid'] or module.params['networkType'] or module.params['silent'] or module.params['level']:
                iSis.build(stage=True)
            else:
                isis.build(stage=True, **delta)
    elif state == 'absent':
        if existing:
            iSis.remove(stage=True)

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
