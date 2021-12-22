#!/usr/bin/python

DOCUMENTATION = """
---

module: comware_interface
short_description: Manage administrative state and physical attributes of the interface
description:
    - Manage administrative state and physical attributes of the interface
version_added: 1.8
category: Feature (RW)
author: liudongxue
notes:
    - Only logical interfaces can be removed with state=absent.
    - If you want to configure type (bridged or routed),
      run this module first with no other interface parameters.
      Then, remove the type parameter and include the other desired parameters.
      When the type parameter is given, other parameters are defaulted.
    - When state is set to default, the interface will be "defaulted"
      regardless of what other parameters are entered.
    - When state is set to default, the interface must already exist.
    - When state is set to absent, logical interfaces will be removed
      from the switch, while physical interfaces will be "defaulted"
    - Tunnel interface creation and removal is not currently supported.
options:
    name:
        description:
            - Full name of the interface
        required: true
        default: null
        choices: []
        aliases: []
    admin:
        description:
            - Admin state of the interface
        required: false
        default: up
        choices: ['up', 'down']
        aliases: []
    description:
        description:
            - Single line description for the interface
        required: false
        default: null
        choices: []
        aliases: []
    type:
        description:
            - Type of interface, i.e. L2 or L3
        required: false
        default: null
        choices: ['bridged', 'routed']
        aliases: []
    duplex:
        description:
            - Duplex of the interface
        required: false
        default: null
        choices: ['auto', 'full']
        aliases: []
    speed:
        description:
            - Speed of the interface in Mbps
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

# Basic Ethernet config
- comware_interface: name=FortyGigE1/0/5 admin=up description=mydesc duplex=auto speed=40000 username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
- comware_interface: name=hun1/0/26.1 type=routed state=present username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
"""

import socket
import re
try:
    HAS_PYHP = True
    from pyhpecw7.comware import HPCOM7
    from pyhpecw7.features.interface import Interface
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
            admin=dict(choices=['up', 'down']),
            description=dict(),
            type=dict(choices=['bridged', 'routed']),
            duplex=dict(choices=['auto', 'full']),
            speed=dict(type='str'),
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

    name = module.params['name']
    subnum_list = name.split('.')
    state = module.params['state']
    changed = False

    # if state == 'present':
    #     if module.params.get('type'):
    #         if module.params.get('admin') or module.params.get('description')\
    #                 or module.params.get('duplex') or module.params.get('speed'):
    #             module.fail_json(msg='The type parameter is incompatible with:'
    #                                  '\nadmin, description, duplex, speed.'
    #                                  '\nPlease configure type first by itself,'
    #                                  '\nthen run again.')

    proposed = dict((k, v) for k, v in module.params.items()
                    if v is not None and k not in filtered_keys)

    try:
        look_for_keys = module.params['look_for_keys']
        device.open(look_for_keys=look_for_keys)
    except ConnectionError as e:
        safe_fail(module, device, msg=str(e),
                  descr='Error opening connection to device.')

    try:
        interface = Interface(device, name)
    except PYHPError as e:
        safe_fail(module,
                  device,
                  descr='There was problem recognizing that interface.',
                  msg=str(e))

    try:
        interface.param_check(**proposed)
    except PYHPError as e:
        safe_fail(module,
                  device,
                  descr='There was problem with the supplied parameters.',
                  msg=str(e))

    try:
        existing = interface.get_config()
    except PYHPError as e:
        safe_fail(module, device, msg=str(e),
                  descr='Error getting existing config.')

    if state == 'present':
        delta = dict(set(proposed.items()).difference(
            existing.items()))
        if delta or not existing:
            if not interface.iface_exists:
                try:
                    interface.create_logical()
                    interface.update()
                    changed=True
                    existing = interface.get_config()
                except PYHPError as e:
                    safe_fail(
                        module, device,
                        msg='Exception message ' + str(e),
                        descr='There was a problem creating'
                        + ' the logical interface.')
                delta = dict(set(proposed.items()).difference(
                    existing.items()))

            if delta:
                res_sub = re.search(r'\.', name)
                if interface.is_routed and res_sub != None:
                    interface.create_sub_iface(stage=True)
                interface.build(stage=True, **delta)
        else:
            res_sub = re.search(r'\.', name)
            if interface.is_routed and res_sub != None:
                interface.create_sub_iface(stage=True)

    elif state == 'default':
        defaults = interface.get_default_config()
        delta = dict(set(existing.items()).difference(
            defaults.items()))
        if delta:
            interface.default(stage=True)
    elif state == 'absent':
        if interface.iface_exists:
            if interface.is_ethernet:
                defaults = interface.get_default_config()
                delta = dict(set(existing.items()).difference(
                    defaults.items()))
                if delta:
                    try:
                        interface.default(stage=True)
                    except InterfaceError as e:
                        safe_fail(module, device, msg=str(e),
                                  descr='Error getting default configuration.')
            elif len(subnum_list) == 2:
                try:
                    interface.remove_sub_iface(stage=True)
                except InterfaceError as e:
                    safe_fail(module, device, msg=str(e),
                              descr='Error removing routing sub interface.')
        else:
            try:
                interface.remove_logical(stage=True)
            except InterfaceError as e:
                safe_fail(module, device, msg=str(e),
                          descr='Error removing logical interface.')

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
                end_state = interface.get_config()
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
