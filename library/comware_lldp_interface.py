#!/usr/bin/python

DOCUMENTATION = """
---

module: comware_lldp_interface
short_description: Manage lldp enable on interfaces.The default state is enable.
version_added: 1.0
author: gongqianyu
category: Feature (RW)
notes:
    - Before config interface lldp enable, the global lldp must be enable.
options:
    name:
        description:
            - Full name of the interface
        required: true
        default: null
        choices: []
        aliases: []
    interface_enable:
        description:
            - Layer 2 mode of the interface
        required: true
        default: null
        choices: ['enabled', 'disabled']
        aliases: []
    state:
        description:
            - Desired state of the interface lldp state.
        required: false
        default: present
        choices: ['present', 'default']
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

# Basic interface lldp config
- comware_lldp_interface: name=FortyGigE1/0/2 interface_enable=enabled username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

"""

import socket

try:
    HAS_PYHP = True
    from pyhpecw7.comware import HPCOM7
    from pyhpecw7.features.lldp_interface import Lldp
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
            name=dict(required=True),
            interface_enable=dict(required=True,
                           choices=['enabled', 'disabled']),
            state=dict(choices=['present', 'default'],
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
                     'port', 'CHECKMODE', 'name', 'look_for_keys')

    hostname = socket.gethostbyname(module.params['hostname'])
    username = module.params['username']
    password = module.params['password']
    port = module.params['port']

    device = HPCOM7(host=hostname, username=username,
                    password=password, port=port)

    name = module.params['name']
    state = module.params['state']
    changed = False

    try:
        look_for_keys = module.params['look_for_keys']
        device.open(look_for_keys=look_for_keys)
    except ConnectionError as e:
        safe_fail(module, device, msg=str(e),
                  descr='Error opening connection to device.')

#    interface_enable = module.params.get('interface_enable')
    try:
        lldp = Lldp(device, name)
    except PYHPError as e:
        safe_fail(module, device, msg=str(e),
                  descr='Error initialzing Switchport object.')

    # Make sure interface exists and is ethernet
    if not lldp.interface.iface_exists:
        safe_fail(module, device,
                  msg='{0} doesn\'t exist on the device.'.format(name))

    try:
        existing = lldp.get_config()
    except PYHPError as e:
        safe_fail(module, device, msg=str(e),
                  descr='Error getting lldp config.')

    proposed = dict((k, v) for k, v in module.params.items()
                    if v is not None and k not in filtered_keys)

    if state == 'present':
        delta = dict(set(proposed.items()).difference(
            existing.items()))

        if delta:
            delta['interface_enable'] = proposed.get('interface_enable')
            lldp.build(stage=True, **delta)
    elif state == 'default':
        defaults = lldp.get_default()
        delta = dict(set(existing.items()).difference(
            defaults.items()))
        if delta:
            lldp.default(stage=True)

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
                end_state = lldp.get_config()
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
