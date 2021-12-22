#!/usr/bin/python

DOCUMENTATION = """
---

module: comware_portchannel
short_description: Manage port-channel (LAG) on Comware 7 devices
description:
    - Manage routed and bridged aggregation configurations on Comware 7
      devices.  This includes physical interface configs for LACP.
version_added: 1.0
author:wangliang,gongqianyu
category: Feature (RW)

notes:
    - When configuring a LAGG, the members param must be included
    - Members is ALL members - it is ensuring that the members sent
      is the full list of all members.  This means to remove a member
      it just needs to be removed from the members list.
    - When removing a LAGG, members is not required
    - If mode is set to static, lacp_edge and lacp_mode are disregarded
      if those params are set
options:
    group:
        description:
            - Group number to identify the Aggregate interface
        required: true
        default: null
        choices: []
        aliases: []
    members:
        description:
            - COMPLETE Interface List that should be in the agg group.
              Full names should be used AND Interface names ARE case
              sensitive. For example, FortyGigE1/0/1 should NOT be written
              as fortygige1/0/1.  This is for safety.
        required: false
        default: null
        choices: []
        aliases: []
    mode:
        description:
            - Mode of the Aggregate interface.If you want to Configure the port rate as a condition for selecting the 
              reference port first, require it.
        required: false
        default: dynamic
        choices: ['static', 'dynamic']
        aliases: []
    type:
        description:
            - Type of the Aggregate interface (L2 or L3)
        required: true
        default: null
        choices: ['bridged', 'routed']
        aliases: []
    lacp_mode:
        description:
            - If mode is set to LACP, the type operating mode can be selected.
              This  mode will then be set for all members in the group.
        required: false
        default: active
        choices: ['active', 'passive']
        aliases: []
    hash_mode:
        description:
            -Hash mode  for the agg group.
             some mode cannot config use netconfig,like 'flexible' and 'per-packet'.
        required: false
        default: null
        choices: ['destination-ip', 'destination-mac', 'source-ip', 'source-mac']
        aliases: []
    min_ports:
        description:
            - Minimum number of selected ports for the agg group
        required: false
        default: null
        choices: []
        aliases: []
    max_ports:
        description:
            - Maximum number of selected ports for the agg group
        required: false
        default: null
        choices: []
        aliases: []
    lacp_edge:
        description:
            - Determine if an LACP agg group should be an edge aggregate
              interface
        required: false
        default: null
        choices: ['enabled', 'disabled']
        aliases: []
    s_mlag:
        description:
            - Determine if add agg group into s_mlag group.If you want to collocate lacp system-mac,
              you must require it
        required: false
        default: null
        choices: []
        aliases: []   
    speed:
        description:
            - Configure the port rate as a condition for selecting the reference port first.The default state is port ID
               as a condition for selecting the reference port first.Before configure it, the agg group interface must 
               be dynamic agg interface.
        required: false
        default: null
        choices: ['enabled', 'disabled']
        aliases: []
    state:
        description:
            - Desired state for the interface configuration
        required: false
        default: present
        choices: ['present', 'absent']
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
    look_for_keys:
        description:
            - Whether searching for discoverable private key files in ~/.ssh/
        required: false
        default: False
        choices: []
        aliases: []

"""

EXAMPLES = """

  # Portchannel config
  -  comware_portchannel: group=100 members=HundredGigE1/0/3 mode=static type=bridged lacp_mode=active hash_mode=source-ip min_ports=2 max_ports=4 lacp_edge=enabled s_mlag=1 speed=enabled state=present username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
#delete config
  -  comware_portchannel: group=100 members=HundredGigE1/0/3 mode=static type=bridged lacp_mode=active hash_mode=source-ip min_ports=2 max_ports=4 lacp_edge=enabled s_mlag=1 speed=enabled state=absent username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
  
"""

import socket
try:
    HAS_PYHP = True
    from pyhpecw7.features.portchannel import Portchannel
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


def get_delta(existing, proposed, existing_members, proposed_members,
              lacp_mode, portchannel):

    portchannel.members_to_remove = list(set(existing_members).difference(
        proposed_members))

    members_to_add = list(set(proposed_members).difference(
                              existing_members))

    lacp_modes_by_interface = []
    if 'lacp_modes_by_interface' in existing.keys():
        lacp_modes_by_interface = existing.pop('lacp_modes_by_interface')

    attr_delta = dict(set(proposed.items()).difference(
                      existing.items()))

    if members_to_add:
        attr_delta['members'] = members_to_add

    lacp_to_change = []

    for each in lacp_modes_by_interface:
        if each.get('lacp_mode') != lacp_mode\
                and each.get('mode') == 'dynamic':
            lacp_to_change.append(each.get('interface'))

    if lacp_to_change:
        attr_delta['lacp_to_change'] = lacp_to_change
        portchannel.desired_lacp_mode = attr_delta.pop('lacp_mode')
    if 'lacp_mode' in attr_delta.keys():
        attr_delta.pop('lacp_mode')

    return attr_delta


def main():
    module = AnsibleModule(
        argument_spec=dict(
            group=dict(required=True, type='str'),
            members=dict(required=False, type='list'),
            mode=dict(required=False, choices=['static', 'dynamic']),
            type=dict(required=True, choices=['bridged', 'routed']),
            lacp_mode=dict(required=False, choices=['active', 'passive']),
            hash_mode=dict(required=False, choices=['destination-ip', 'destination-mac', 'source-ip', 'source-mac']),
            lacp_edge=dict(required=False, choices=['enabled', 'disabled']),
            s_mlag = dict(required=False, type='str'),
            speed = dict(required=False, choices=['enabled', 'disabled']),
            min_ports=dict(required=False, type='str'),
            max_ports=dict(required=False, type='str'),
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

    groupid = module.params['group']
    members = module.params['members']
    lacp_mode = module.params['lacp_mode']
    hash_mode = module.params['hash_mode']
    mode = module.params['mode']
    lacp_edge = module.params['lacp_edge']
    min_ports = module.params['min_ports']
    max_ports = module.params['max_ports']
    s_mlag = module.params['s_mlag']
    speed = module.params['speed']

    pc_type = module.params['type']

    state = module.params['state']

    if members:
        if not isinstance(members, list):
            module.fail_json(msg='members param must be a list.  YAML format '
                             + '\nmust be used within the playbook')
    if state == 'present' and not members:
        module.fail_json(msg='members param required when state=present')

    if mode == 'static' and lacp_mode:
        lacp_mode = None
        lacp_edge = None

    changed = False

    args = dict(groupid=groupid, lacp_edge=lacp_edge, mode=mode, hash_mode=hash_mode, s_mlag=s_mlag, speed=speed,
                min_ports=min_ports, max_ports=max_ports, lacp_mode=lacp_mode)

    proposed = dict((k, v) for k, v in args.items() if v is not None)

    try:
        look_for_keys = module.params['look_for_keys']
        device.open(look_for_keys=look_for_keys)
    except ConnectionError as e:
        safe_fail(module, device, msg=str(e),
                  descr='error connecting to device')

    try:
        portchannel = Portchannel(device, groupid, pc_type)
#        portchannel.param_check(members=members, **proposed)
        existing = portchannel.get_config()
    except InvalidPortType as ipte:
        safe_fail(module, device, msg=str(ipte))
    except AggregationGroupError as age:
        safe_fail(module, device, msg=str(age))
    except PYHPError as e:
        safe_fail(module, device, msg=str(e))

    if 'members' in existing.keys():
        existing_members = existing.pop('members')
    else:
        existing_members = []

    if state == 'present':
        delta = get_delta(existing, proposed, existing_members,
                          members, lacp_mode, portchannel)
        if delta:
            # delta['groupid'] = groupid
            portchannel.build(stage=True, **delta)
    elif state == 'absent':
        if existing:
            portchannel.remove(stage=True)

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
                end_state = portchannel.get_config()
            except PYHPError as e:
                safe_fail(module, device, msg=str(e),
                          descr='error during execution')
            changed = True

    proposed['members'] = members
    proposed['type'] = pc_type

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
