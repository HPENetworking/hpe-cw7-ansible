#!/usr/bin/python

DOCUMENTATION = """
---

module: comware_ospf_intf
short_description: Manage ospf in interface
description:
    - Manage ospf in interface
version_added: 1.0
category: Feature (RW)
author: hanyangyang
notes:
    - The module is used to config interface ospf setting , before using the module , please
      ensure the interface exists and is able to make ospf setting . 
    - Interface ospf auth mode can config as simple or md5 , however these two mode can not be
      set at the same time.
    - Some of the setting must be set together e.g. ospfname must together with area.
    - state default or absent will delete all the ospf settings , 
options:
    name:
        description:
            - full name of interface
        required: true
        default: null
        choices: []
        aliases: []
    ospfname:
        description:
            - Instance name.(1~65535)
        required: false
        default: null
        choices: []
        aliases: [] 
    ospfcost:
        description:
            - Configure the overhead required for the interface to run OSPF
        required: false
        default: null
        choices: []
        aliases: []   
    area:
        description:
            - Specify the OSPF area
        required: false
        default: null
        choices: []
        aliases: []   
    simplepwdtype:
        description:
            - Specify the password type of ospf auth_mode simple
        required: false
        default: null
        choices: ['cipher', 'plain']
        aliases: []  
    simplepwd:
        description:
            - Specify the password  of ospf auth_mode simple
        required: false
        default: null
        choices: []
        aliases: []    
    keyid:
        description:
            - Specify the md5 or hwac-md5 key of ospf auth_mode
        required: false
        default: null
        choices: []
        aliases: []   
    md5type:
        description:
            - Specify the ospf auth_mode md5 type
        required: false
        default: null
        choices: ['md5', 'hwac-md5]
        aliases: []  
    md5pwdtype:
        description:
            - Specify the password type of ospf auth_mode md5
        required: false
        default: null
        choices: ['cipher', 'plain']
        aliases: []   
    md5pwd:
        description:
            - Specify the password of ospf auth_mode md5
        required: false
        default: null
        choices: []
        aliases: []  
    network_type:
        description:
            - Specify OSPF network type
        required: false
        default: null
        choices: ['broadcast', 'nbma','p2p','p2mp']
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
  ensure name (interface name) exists in device and the interface support ospf setting.
- comware_ospf_intf: name=Ten-GigabitEthernet1/0/7 ospfname=1 area=0 ospfcost=10 network_type=p2p keyid=11 \
  md5type=md5 md5pwdtype=plain md5pwd=1 username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
- comware_ospf_intf: name=Ten-GigabitEthernet1/0/7 state=default \
  username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
"""

import socket

try:
    HAS_PYHP = True
    from pyhpecw7.comware import HPCOM7
    from pyhpecw7.features.ospf_intf import Ospf
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
            name=dict(required=True,type='str'),
            ospfname=dict(required=False,type='str'),
            ospfcost=dict(required=False,type='str'),
            area=dict(required=False,type='str'),
            simplepwdtype=dict(choices=['cipher', 'plain']),
            simplepwd=dict(type='str'),
            keyid=dict(type='str'),
            md5type=dict(choices=['md5', 'hwac-md5']),
            md5pwdtype=dict(choices=['cipher', 'plain']),
            md5pwd=dict(type='str'),
            network_type=dict(choices=['broadcast', 'nbma','p2p','p2mp']),
            state=dict(choices=['present', 'absent','default'],
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
    ospfname = module.params['ospfname']
    ospfcost = module.params['ospfcost']
    area = module.params['area']
    simplepwdtype = module.params['simplepwdtype']
    simplepwd = module.params['simplepwd']
    keyid = module.params['keyid']
    md5type = module.params['md5type']
    md5pwdtype = module.params['md5pwdtype']
    md5pwd = module.params['md5pwd']
    network_type = module.params['network_type']
    changed = False
    proposed = dict((k, v) for k, v in module.params.items()
                    if v is not None and k not in filtered_keys)

    try:
        look_for_keys = module.params['look_for_keys']
        device.open(look_for_keys=look_for_keys)
    except ConnectionError as e:
        safe_fail(module, device, msg=str(e),
                  descr='Error opening connection to device.')

    if simplepwdtype and md5type:
        safe_fail(module,msg='only one authentication-mode is effective')

    if area or ospfname:
        if module.params.get('area') and module.params.get('ospfname'):
            pass
        else:
            safe_fail(module,msg='param area must be setting together with ospfname')

    if simplepwd or simplepwdtype:
        if module.params.get('simplepwd') and module.params.get('simplepwdtype'):
            pass
        else:
            safe_fail(module, msg='param simplepwd must be setting together with simplepwdtype')

    if md5pwd or keyid or md5type or md5pwdtype:
        if module.params.get('md5pwd') and module.params.get('keyid') and \
                module.params.get('md5type') and module.params.get('md5pwdtype'):
            pass
        else:
            safe_fail(module,msg='all the paramaters md5pwd keyid md5type md5pwdtype are needed when setting md5 auth mode')

    try:
        ospf = Ospf(device,name)
        ospf_interface = Interface(device,name)
    except PYHPError as e:
        safe_fail(module,device,descr='there is problem in setting ospf config',
                  msg=str(e))

    if not ospf_interface.iface_exists:
        safe_fail(module, device, msg='interface does not exist.')
    is_eth, is_rtd = ospf_interface._is_ethernet_is_routed()
    if not is_rtd:
        safe_fail(module,msg='Interface is not l3 interface. please use interface module set first.')

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
    proposed_area = dict(ospfname=ospfname, area=area)
    proposed_cost = dict(ospfcost=ospfcost)
    proposed_nets = dict(network_type=network_type)
    proposed_spwd = dict(simplepwdtype=simplepwdtype, \
                         simplepwd=simplepwd)
    proposed_md5 = dict(keyid=keyid, md5type=md5type, \
                        md5pwdtype=md5pwdtype, md5pwd=md5pwd)

    if state == 'present':
        ospf.build_area(stage=True, **proposed_area)
        if ospfcost:
            ospf.build(stage=True,**proposed_cost)
            if network_type:
                ospf.build(stage=True, **proposed_nets)
                if simplepwd:
                    ospf.build_auth_simple(stage=True, state='present', **proposed_spwd)
                elif md5pwd:
                    ospf.build_auth_md5(stage=True, state='present', **proposed_md5)
            else:
                if simplepwd:
                    ospf.build_auth_simple(stage=True, state='present', **proposed_spwd)
                elif md5pwd:
                    ospf.build_auth_md5(stage=True, state='present', **proposed_md5)
        else:
            if network_type:
                ospf.build(stage=True, **proposed_nets)
                if simplepwd:
                    ospf.build_auth_simple(stage=True, state='present', **proposed_spwd)
                elif md5pwd:
                    ospf.build_auth_md5(stage=True, state='present', **proposed_md5)
            else:
                if simplepwd:
                    ospf.build_auth_simple(stage=True, state='present', **proposed_spwd)
                elif md5pwd:
                    ospf.build_auth_md5(stage=True, state='present', **proposed_md5)

    elif state == 'absent' or 'default':
        if existing:
            ospf.default_ospf(stage=True)

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
