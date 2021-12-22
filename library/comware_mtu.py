#!/usr/bin/python

DOCUMENTATION = """
---

module: comware_mtu
short_description: Manage mtu and jumboframe of the interface
description:
    - Manage mtu and jumboframe of the interface
version_added: 1.0
category: Feature (RW)
author:hanyangyang
notes:
    - mtu can be set in interface type of ['GigabitEthernet','Ten-GigabitEthernet','FortyGigE',
      'Vlan-interface','Route-Aggregation','TwentyGigE','Twenty-FiveGigE','HundredGigE'] and 
      some of these must be set as route mode.
    - jumboframe can be set in interface type of ['GigabitEthernet','Ten-GigabitEthernet',
      'FortyGigE','Bridge-Aggregation','Route-Aggregation','TwentyGigE','Twenty-FiveGigE','HundredGigE']
options:
    name:
        description:
            - Full name of the interface
        required: true
        default: null
        choices: []
        aliases: []
    mtu:
        description:
            - Specify Maximum Transmission Unit(MTU) of the interface
        required: false
        default: null
        choices: []
        aliases: []
    jumboframe:
        description:
            - Specify Maximum jumbo frame size allowed of the interface
        required: false
        default: null
        choices: []
        aliases: []
    state:
        description:
            - Desired state for the interface configuration
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
- comware_mtu: name=Ten-GigabitEthernet1/0/7 jumboframe=1537 mtu=1600 username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

"""

import socket

try:
    HAS_PYHP = True
    from pyhpecw7.comware import HPCOM7
    from pyhpecw7.features.mtu import Mtu
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
            mtu=dict(type='str'),
            jumboframe=dict(type='str'),
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
    state = module.params['state']
    mtu = module.params['mtu']
    jumboframe = module.params['jumboframe']

    changed = False

    proposed = dict((k, v) for k, v in module.params.items()
                    if v is not None and k not in filtered_keys)

    try:
        look_for_keys = module.params['look_for_keys']
        device.open(look_for_keys=look_for_keys)
    except ConnectionError as e:
        safe_fail(module, device, msg=str(e),
                  descr='Error opening connection to device.')

    try:
        mtu = Mtu(device, name)
    except PYHPError as e:
        safe_fail(module,
                  device,
                  descr='There was problem recognizing that interface.',
                  msg=str(e))

    try:
        mtu.param_check(**proposed)
    except PYHPError as e:
        safe_fail(module,
                  device,
                  descr='There was problem with the supplied parameters.',
                  msg=str(e))
    if module.params.get('jumboframe'):
        args = dict(jumboframe=jumboframe)
    try:
        existing = mtu.get_config()
    except PYHPError as e:
        safe_fail(module, device, msg=str(e),
                  descr='Error getting existing config.')

    if state == 'present':
        delta = dict(set(proposed.items()).difference(
            existing.items()))
        if module.params.get('jumboframe'):
            mtu.build_jumbo(stage=True, **args)
            del delta['jumboframe']
        if delta or not existing:
            if not mtu.iface_exists:
                try:
                    mtu.create_logical()
                    mtu.update()
                    changed=True
                    existing = mtu.get_config()
                except PYHPError as e:
                    safe_fail(
                        module, device,
                        msg='Exception message ' + str(e),
                        descr='There was a problem creating'
                        + ' the logical interface.')
                delta = dict(set(proposed.items()).difference(
                    existing.items()))

            if delta:
                mtu.build(stage=True, **delta)
    elif state == 'default':
        defaults = mtu.get_default_config()
        delta = dict(set(existing.items()).difference(
            defaults.items()))
        jumbo_config = mtu.get_jumbo_config()
        if jumbo_config:
            jumbo_lst = []
            for k,v in jumbo_config.items():
                jumbo_lst.append(v)
            #jumboframe default 9416
            if int(jumbo_lst[0]) != 9416:
                mtu.remove_jumbo(stage=True,**jumbo_config)
        if delta:
            mtu.default(stage=True)

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
                end_state = mtu.get_config()
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
