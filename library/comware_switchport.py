#!/usr/bin/python

DOCUMENTATION = """
---

module: comware_switchport
short_description: Manage Layer 2 parameters on switchport interfaces
author:hanyangyang
description:
    - Manage Layer 2 parameters on switchport interfaces
version_added: 1.0
category: Feature (RW)
notes:
    - If the interface is configured to be a Layer 3 port, the module
      will fail and ask the user to use the comware_interface module
      to convert it to be a Layer 2 port first.
    - If the interface is a member in a LAG, the module will fail
      telling the user changes hould be made to the LAG interface
    - If VLANs are trying to be assigned that are not yet created on
      the switch, the module will fail asking the user to create
      them first.
    - If state=default, the switchport settings will be defaulted.
      That means it will be set as an access port in VLAN 1.
options:
    name:
        description:
            - Full name of the interface
        required: true
        default: null
        choices: []
        aliases: []
    link_type:
        description:
            - Layer 2 mode of the interface
        required: true
        default: null
        choices: ['access', 'trunk', 'hybrid']
        aliases: []
    pvid:
        description:
            - If link_type is set to trunk this will be used as the native
              native VLAN ID for that trunk. If link_type is set to access
              then this is the VLAN ID of the interface.
        required: false
        default: null
        choices: []
        aliases: []
    permitted_vlans:
        description:
            - If mode is set to trunk this will be the complete list/range
              (as a string) of VLANs allowed on that trunk interface.
              E.g. 1-3,5,8-10
              Any VLAN not in the list
              will be removed from the interface.
        required: false
        default: null
        choices: []
        aliases: []
    untaggedvlan:
        description:Assign hybrid port to untagged VLANs
              E.g. 1-3,5,8-10
        required: false
        default: null
        choices: []
        aliases: []
    taggedvlan:
        description:Assign hybrid port to tagged VLANs
              E.g. 1-3,5,8-10
        required: false
        default: null
        choices: []
        aliases: []
    state:
        description:
            - Desired state of the switchport
        required: false
        default: present
        choices: ['present', 'default','absent']
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

# Basic access config
- comware_switchport: name=Ten-GigabitEthernet1/0/3 link_type=access pvid=3 username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

# Basic trunk config
- comware_switchport: name=FortyGigE1/0/2 link_type=trunk permitted_vlans="1-3,5,8-10" username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

"""

import socket

try:
    HAS_PYHP = True
    from pyhpecw7.comware import HPCOM7
    from pyhpecw7.features.switchport import Switchport
    from pyhpecw7.features.vlan import Vlan
    from pyhpecw7.features.portchannel import Portchannel
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
            link_type=dict(required=True,
                           choices=['access', 'trunk', 'hybrid']),
            pvid=dict(type='str'),
            permitted_vlans=dict(type='str'),
            untaggedvlan=dict(type='str'),
            taggedvlan=dict(type='str'),
            state=dict(choices=['present', 'default','absent'],
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
    if state == 'present':
        if module.params.get('link_type') == 'access':
            if module.params.get('permitted_vlans') or module.params.get('taggedvlan') or module.params.get('untaggedvlan'):
                safe_fail(module,
                          msg='Access interfaces don\'t take'
                          + ' permitted vlan lists, untaggedvlan or taggedvlan .')
        elif module.params.get('link_type') == 'trunk':
            if module.params.get('untaggedvlan') or module.params.get('taggedvlan'):
                safe_fail(module,
                          msg='Trunk interfaces don\'t take'
                          + 'untaggedvlan or taggedvlan .')
        elif module.params.get('link_type') == 'hybrid':
            if module.params.get('permitted_vlans'):
                safe_fail(module,msg='Hybrid interface don\'t take '
                          + 'permitted vlan lists.')

    try:
        look_for_keys = module.params['look_for_keys']
        device.open(look_for_keys=look_for_keys)
    except ConnectionError as e:
        safe_fail(module, device, msg=str(e),
                  descr='Error opening connection to device.')

    # Make sure vlan exists
    pvid = module.params.get('pvid')
    if pvid and state != 'default':
        try:
            vlan = Vlan(device, pvid)
            if not vlan.get_config():
                safe_fail(module, device,
                          msg='Vlan {0} does not exist,'.format(pvid)
                          + ' Use vlan module to create it.')
        except PYHPError as e:
            module.fail_json(msg=str(e),
                             descr='Error initializing Vlan object'
                             + ' or getting current vlan config.')

    # Make sure port is not part of port channel
    try:
        portchannel = Portchannel(device, '99', 'bridged')
        pc_list = portchannel.get_all_members()
    except PYHPError as e:
        module.fail_json(msg=str(e),
                         descr='Error getting port channel information.')
    if name in pc_list:
        safe_fail(module, device,
                  msg='{0} is currently part of a port channel.'.format(name)
                  + ' Changes should be made to the port channel interface.')

    try:
        switchport = Switchport(device, name)
    except PYHPError as e:
        safe_fail(module, device, msg=str(e),
                  descr='Error initialzing Switchport object.')

    # Make sure interface exists and is ethernet
    if not switchport.interface.iface_exists:
        safe_fail(module, device,
                  msg='{0} doesn\'t exist on the device.'.format(name))

    # Make sure interface is in bridged mode
    try:
        if_info = switchport.interface.get_config()
    except PYHPError as e:
        safe_fail(module, device, msg=str(e),
                  descr='Error getting current interface config.')

    if if_info.get('type') != 'bridged':
        safe_fail(module, device, msg='{0} is not in bridged mode.'.format(name)
                  + ' Please use the interface module to change that.')

    try:
        existing = switchport.get_config()
    except PYHPError as e:
        safe_fail(module, device, msg=str(e),
                  descr='Error getting switchpot config.')

    proposed = dict((k, v) for k, v in module.params.items()
                    if v is not None and k not in filtered_keys)

    if state == 'present':
        delta = dict(set(proposed.items()).difference(
            existing.items()))
        if delta:
            delta['link_type'] = proposed.get('link_type')
            pvid = proposed.get('pvid')
            if pvid:
                delta['pvid'] = pvid

            switchport.build(stage=True, **delta)
    elif state == 'default':
        defaults = switchport.get_default()
        delta = dict(set(existing.items()).difference(
            defaults.items()))
        if delta:
            switchport.default(stage=True)
    elif state == 'absent':
        # options = {'link_type': "module.params.get('link_type')",
        #                   'pvid': "module.params.get('pvid')",
        #                   'permitted_vlans': "module.params.get('permitted_vlans')",
        #                   'untaggedvlan': "module.params.get('untaggedvlan')",
        #                   'taggedvlan': "module.params.get('taggedvlan')"}
        # options = dict((k, v) for k, v in module.params.items()
        #                 if v is not None and k not in filtered_keys)
        defaults = switchport.get_default()
        delta = dict(set(existing.items()).difference(
            defaults.items()))
        if delta:
            if module.params.get('link_type') == 'hybrid':
                switchport.remove_hybrid(stage=True)
            if module.params.get('link_type') == 'trunk':
                switchport.remove_trunk(stage=True)
            if module.params.get('link_type') == 'access':
                switchport.remove_access(stage=True)
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
                end_state = switchport.get_config()
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
print('*********************************')