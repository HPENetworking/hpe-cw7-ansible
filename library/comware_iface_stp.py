#!/usr/bin/python

DOCUMENTATION = """
---

module: comware_iface_stp
short_description: Manage stp config in interface
description:
    - Manage stp config in interface
version_added: 1.8
category: Feature (RW)
author:hanyangyang
notes:
    - stp interface configs must be setting in l2 ethernet mode .
    - loop protect is conflict with edgeport and root protect , while loop protect
      exists , edgeport and root protect can not be setted , vice versa.
    
options:
    name:
        description:
            - Full name of the interface
        required: True
        default: null
        choices: []
        aliases: []
    edgedport:
        description:
            - Specify edge port
        required: false
        default: null
        choices: []
        aliases: []
    loop:
        description:
            - Specify loop protection
        required: false
        default: null
        choices: []
        aliases: []
    root:
        description:
            - Specify root protection
        required: false
        default: null
        choices: []
        aliases: []
    tc_restriction:
        description:
            - Restrict propagation of TC message
        required: false
        default: null
        choices: []
        aliases: []
    transimit_limit:
        description:
            - Specify transmission limit count
        required: false
        default: null
        choices: []
        aliases: []
    state:
        description:
            - Desired state for the interface configuration
        required: false
        default: present
        choices: ['present', 'absent', 'default']
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
            - The Comware port used to connect to the switch
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
EXAMPLE = """

# Basic interface stp config
- comware_iface_stp:  name=Ten-GigabitEthernet1/0/7 tc_restriction=true transimit_limit=200 username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

# Delete interface stp config
- comware_iface_stp:  name=Ten-GigabitEthernet1/0/7  state=default username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

# Interface stp full configuration
- comware_iface_stp:  name=HundredGigE1/0/25 edgedport=true root=true tc_restriction=true transimit_limit=200   username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
"""

import socket

try:
    HAS_PYHP = True
    from pyhpecw7.comware import HPCOM7
    from pyhpecw7.features.iface_stp import Stp
    from pyhpecw7.features.errors import InterfaceError
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
            edgedport=dict(required=False,choices=['true', 'false',]),
            loop=dict(required=False, choices=['true', 'false', ]),
            root=dict(required=False, choices=['true', 'false', ]),
            tc_restriction=dict(required=False,choices=['true', 'false',]),
            transimit_limit=dict(type='str'),
            state=dict(choices=['present', 'absent', 'default'],
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
        safe_fail(module, msg='There was a problem loading from the pyhpecw7 '
                  + 'module.', error=str(ie))

    filtered_keys = ('state', 'hostname', 'username', 'password',
                     'port', 'CHECKMODE', 'name', 'look_for_keys')

    hostname = socket.gethostbyname(module.params['hostname'])
    username = module.params['username']
    password = module.params['password']
    port = module.params['port']
    device = HPCOM7(host=hostname, username=username,
                    password=password, port=port)
    state = module.params['state']
    name = module.params['name']
    changed = False

    if module.params['edgedport'] or module.params['root']:
        if module.params['loop']:
            safe_fail(module,msg='loop protect can not be set \
            while edgeport or root protect exist')
    if module.params['loop']:
        if module.params['edgedport'] or module.params['root']:
            safe_fail(module, msg='edgeport or root protect can not be set \
                        while loop protect exist')

    proposed = dict((k, v) for k, v in module.params.items()
                    if v is not None and k not in filtered_keys)

    try:
        look_for_keys = module.params['look_for_keys']
        device.open(look_for_keys=look_for_keys)
    except ConnectionError as e:
        safe_fail(module, device, msg=str(e),
                  descr='Error opening connection to device.')

    try:
        stp = Stp(device,name)
    except PYHPError as e:
        safe_fail(module,device,descr='there is problem in setting stp config',
                  msg=str(e))

    try:
        existing = stp.get_config()
    except PYHPError as e:
        safe_fail(module, device, msg=str(e),
                  descr='Error getting existing config.')

    if state == 'present':
        delta = dict(set(proposed.items()).difference(
            existing.items()))
        if delta:
            stp.build(stage=True, **delta)

    elif state == 'default' or 'absent':
        defaults = stp.get_default_config()
        delta = dict(set(existing.items()).difference(
            defaults.items()))
        if delta:
            stp.default(stage=True)

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
                end_state = stp.get_config()
            except PYHPError as e:
                safe_fail(module, device, msg=str(e),
                          descr='Error on device execution.')
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
