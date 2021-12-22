#!/usr/bin/python

DOCUMENTATION = """
---

module: comware_ospf
short_description: Manage ospf
description:
    - 
version_added: 1.0
category: Feature (RW)
author: hanyangyang
notes:

options:
    ospfname:
        description:
            - Instance name.(1~65535)
        required: true
        default: null
        choices: []
        aliases: []
    routerid:
        description:
            - Router identifier.
        required: false
        default: null
        choices: []
        aliases: []
    area:
        description:
            - Area ID
        required: false
        default: null
        choices: []
        aliases: []
    areatype:
        description:
            - Area type
        required: false
        default: null
        choices: ['NSSA', 'Stub']
        aliases: []
    bandwidth:
        description:
            - Configure the bandwidth reference value by which link overhead is calculated(1~4294967)
        required: false
        default: null
        choices: []
        aliases: []
    lsa_generation_max:
        description:
            - Maximum time interval between OSPF LSA regenerations(1~60s)
        required: false
        default: null
        choices: []
        aliases: []
    lsa_generation_min:
        description:
            - Minimum time interval between OSPF LSA regenerations(10~60000ms)
        required: false
        default: null
        choices: []
        aliases: []
    lsa_generation_inc:
        description:
            - Interval penalty increment for OSPF LSA regeneration(10~60000ms)
        required: false
        default: null
        choices: []
        aliases: []
    lsa_arrival:
        description:
            - Configure the minimum time interval for repeat arrival of OSPF LSA(0~60000ms)
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
- comware_ospf: ospfname=4 area=2.2.2.2 areatype=NSSA lsa_generation_max=20 lsa_generation_min=20 lsa_generation_inc=20 username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
"""

import socket

try:
    HAS_PYHP = True
    from pyhpecw7.comware import HPCOM7
    from pyhpecw7.features.ospf import Ospf
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
            ospfname=dict(required=True,type='str'),
            routerid=dict(type='str'),
            import_route=dict(choices=['bgp', 'direct','isis',\
                                       'ospf','rip','static']),
            area=dict(required=False,type='str'),
            networkaddr=dict(type='str'),
            wildcardmask=dict(type='str'),
            areatype=dict(choices=['NSSA', 'Stub']),
            bandwidth=dict(type='str'),
            lsa_generation_max=dict(type='str'),
            lsa_generation_min=dict(type='str'),
            lsa_generation_inc=dict(type='str'),
            lsa_arrival=dict(type='str'),
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
    state = module.params['state']
    ospfname = module.params['ospfname']
    area = module.params['area']
    areatype = module.params['areatype']
    routerid = module.params['routerid']
    lsa_generation_max = module.params['lsa_generation_max']
    lsa_generation_min = module.params['lsa_generation_min']
    lsa_generation_inc = module.params['lsa_generation_inc']
    lsa_arrival = module.params['lsa_arrival']
    bandwidth = module.params['bandwidth']
    import_route = module.params['import_route']
    networkaddr = module.params['networkaddr']
    wildcardmask = module.params['wildcardmask']
    changed = False
    proposed = dict((k, v) for k, v in module.params.items()
                    if v is not None and k not in filtered_keys)

    try:
        look_for_keys = module.params['look_for_keys']
        device.open(look_for_keys=look_for_keys)
    except ConnectionError as e:
        safe_fail(module, device, msg=str(e),
                  descr='Error opening connection to device.')


    if area == '0.0.0.0' and areatype:
        safe_fail(module,msg='OSPF backbone invalid for any options.')

    if area == None and networkaddr != None:
        safe_fail(module,msg='networkaddr and wildcardmask needs to be configured in the area')

    if networkaddr == None and wildcardmask != None:
        safe_fail(module, msg='networkaddr and wildcardmask need to be provided together')

    if networkaddr != None and wildcardmask == None:
        safe_fail(module, msg='networkaddr and wildcardmask need to be provided together')

    try:
        ospf = Ospf(device,ospfname, area)
    except PYHPError as e:
        safe_fail(module,device,descr='there is problem in setting ospf config',
                  msg=str(e))

    try:
        ospf.param_check(**proposed)
    except PYHPError as e:
        safe_fail(module,device,descr='There was problem with the supplied parameters.',
                  msg=str(e))

    try:
        existing = ospf.get_config()
    except PYHPError as e:
        safe_fail(module, device, msg=str(e),
                  descr='Error getting existing config.')

    proposed_lsa = dict(ospfname=ospfname, \
                        lsa_generation_max=lsa_generation_max, \
                        lsa_arrival=lsa_arrival, \
                        lsa_generation_min=lsa_generation_min, \
                        lsa_generation_inc=lsa_generation_inc, \
                        bandwidth=bandwidth)

    if state == 'present':
        if ospfname:
            proposed_ospf = dict(ospfname=ospfname)
            ospf.build_instance(stage=True,**proposed_ospf)
            if lsa_generation_max:
                ospf.build_lsa(stage=True, **proposed_lsa)
            else:
                if bandwidth:
                    ospf.build_lsa(stage=True, **proposed_lsa)
        if proposed:
            if routerid:
                proposed_router = dict(ospfname=ospfname,routerid=routerid)
                ospf.build_instance(stage=True, **proposed_router)
                if area:
                    proposed_area = dict(ospfname=ospfname, area=area)
                    ospf.build_area(stage=True, **proposed_area)
                    if areatype:
                        proposed_area = dict(ospfname=ospfname, area=area, areatype=areatype)
                        ospf.build_area(stage=True, **proposed_area)
                    if networkaddr:
                        proposed_networks = dict(area=area,networkaddr=networkaddr,\
                                                 wildcardmask=wildcardmask)
                        ospf.build_networks(stage=True,**proposed_networks)
            else:
                if area:
                    proposed_area = dict(ospfname=ospfname, area=area)
                    ospf.build_area(stage=True, **proposed_area)
                    if areatype:
                        proposed_area = dict(ospfname=ospfname, area=area, areatype=areatype)
                        ospf.build_area(stage=True, **proposed_area)
                    if networkaddr:
                        proposed_networks = dict(area=area,networkaddr=networkaddr,\
                                                 wildcardmask=wildcardmask)
                        ospf.build_networks(stage=True,**proposed_networks)
        if import_route:
            proposed_import = dict(import_route=import_route)
            ospf.build_import(stage=True,**proposed_import)

    elif state == 'default':
        if ospfname:
            delta = dict(ospfname=ospfname)
            ospf.default(stage=True, **delta)

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
                end_state = ospf.get_config()
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
