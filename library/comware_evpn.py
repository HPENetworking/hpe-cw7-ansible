#!/usr/bin/python

DOCUMENTATION = """
---

module: comware_evpn
short_description: Configure the EVPN issue to be applied to the device.
description:
    -Configure the EVPN issue to be applied to the device.
version_added: 1.8
category: Feature (RW)
author: liudongxue
notes:
    - The asnum is unsigned integer,and the value range is 1 to 4294967295.
    - The type of vrf is string,the length is 1 to 31 characters.
    - The type of mask is Unsigned integer,and the value range is 0 to 128,or 255.
      For non-dynamic peers, this is 255.For IPv4 dynamic peers,this is 0 to 32.For IPv6 dynamic peers, this is 0 to 128. 
      Dynamic peers are not supported.
    - if you want to config bgp  evpn   ,please use comware_bgp_global.py to create bgp process first.

options:
    name:
        description:
            - Full name of the interface
        required: false
        default: null
        choices: []
        aliases: []
    vrf:
        description:
            - VPN instance name.
        required: false
        default: false
        choices: []
        aliases: []
    state:
        description:
            - Desired state for the interface configuration
        required: false
        default: present
        choices: ['present', 'absent']
        aliases: []
    rd:
        description:
            - Route distinguisher
        required: false
        default: false
        choices: []
        aliases: []
    rtentry:
        description:
            - Route target
        required: false
        default: null
        choices: []
        aliases: []
    addrfamily:
        description:
            - Address family
        required: false
        default: null
        choices: ['ipv4', 'ipv6', 'vpn', 'evpn']
        aliases: []
    rttype:
        description:
            - RT type
        required: false
        default: null
        choices: ['import', 'export']
        aliases: []
    asnum:
        description:
            - Autonomous System number
        required: false
        default: null
        choices: ['md5', 'hmac_sha_1', 'hmac_sha_256', 'hmac_sha_384', 'hmac_sha_384']
        aliases: [] 
    sessaf:
        description:
            - Address family of session
        required: false
        default: null
        choices: ['ipv4', 'ipv6']
        aliases: [] 
    ipaddr:
        description:
            - Address of session
        required: false
        default: false
        choices: ['true', 'false']
        aliases: []
    ipadd:
        description:
            - Remote IPv4 or IPv6 address
        required: false
        default: null
        choices: []
        aliases: []
    mask:
        description:
            - Mask of session address
        required: false
        default: null
        choices: []
        aliases: []
    aftype:
        description:
            - Address Family Identifier
        required: false
        default: null
        choices: ['ipv4uni','ipv4mul','mdt', 'vpnv4','ipv6uni','ipv6mul', 'vpnv6','l2vpn','l2vpn_evpn','link_state', 'ipv4mvpn','ipv4flosp', 'vpnv4flosp', 'ipv6flosp', 'vpnv6flosp']
        aliases: []
    family:
        description:
            - Address Family Identifier of Neighbor
        required: false
        default: null
        choices: ['ipv4uni','ipv4mul','mdt', 'vpnv4','ipv6uni','ipv6mul', 'vpnv6','l2vpn','l2vpn_evpn','link_state', 'ipv4mvpn','ipv4flosp', 'vpnv4flosp', 'ipv6flosp', 'vpnv6flosp']
        aliases: []
    del_bgp:
        description:
            - Whether delete BGP
        required: false
        default: null
        choices: ['true', 'false']
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

# configure evpn rt
- comware_evpn: vrf=ali1 addrfamily=ipv4 rttype=export rtentry=30:2  username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
# delete bgp
- comware_evpn: del_bgp=true state=absent username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

comware_evpn: bgp_name=10 vrf=200 asnum=120 mask=255 ipaddr=1.1.1.1 sessaf=ipv4 state=present username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

"""

import socket
import re
try:
    HAS_PYHP = True
    from pyhpecw7.comware import HPCOM7
    from pyhpecw7.features.interface import Interface
    from pyhpecw7.features.errors import *
    from pyhpecw7.errors import *
    from pyhpecw7.features.evpn import Evpn,EVPN
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
            name=dict(required=False),
            state=dict(choices=['present', 'absent'],
                       default='present'),
            vrf=dict(type='str'),
            rd=dict(type='str'),
            rtentry=dict(type='str'),
            addrfamily=dict(choices=['ipv4', 'ipv6', 'vpn', 'evpn']),
            rttype=dict(choices=['import', 'export']),
            bgp_name=dict(type='str'),
            asnum=dict(type='str'),
            sessaf=dict(choices=['ipv4', 'ipv6']),
            ipaddr=dict(type='str'),
            mask=dict(type='str'),
            aftype=dict(choices=['ipv4uni','ipv4mul','mdt', 'vpnv4','ipv6uni','ipv6mul', 'vpnv6','l2vpn','l2vpn_evpn','link_state', 'ipv4mvpn','ipv4flosp', 'vpnv4flosp', 'ipv6flosp', 'vpnv6flosp']),
            family=dict(choices=['ipv4uni','ipv4mul','mdt', 'vpnv4','ipv6uni','ipv6mul', 'vpnv6','l2vpn','l2vpn_evpn','link_state', 'ipv4mvpn','ipv4flosp', 'vpnv4flosp', 'ipv6flosp', 'vpnv6flosp']),
            del_bgp=dict(choices=['true', 'false']),
            hostname=dict(required=True),
            username=dict(required=True),
            password=dict(required=False, default=None),
            port=dict(type='int', default=830),
            look_for_keys=dict(default=False, type='bool')
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
    vrf = str(module.params['vrf'])
    rd = module.params['rd']
    rtentry =  module.params['rtentry']
    bgp_name = module.params['bgp_name']
    addrfamily=module.params['addrfamily']
    rttype = str(module.params['rttype'])
    asnum = module.params['asnum']
    sessaf = module.params['sessaf']
    ipaddr = module.params['ipaddr']
    mask = str(module.params['mask'])
    aftype = module.params['aftype']
    family = module.params['family']
    del_bgp = module.params['del_bgp']
    changed = False

    proposed = dict((k, v) for k, v in module.params.items()
                    if v is not None and k not in filtered_keys)

    try:
        look_for_keys = module.params['look_for_keys']
        device.open(look_for_keys=look_for_keys)
    except ConnectionError as e:
        safe_fail(module, device, msg=str(e),
                  descr='Error opening connection to device.')

    if module.params.get('mask'):
        if int(mask)>32:
            safe_fail(module,msg='IPv4 address mask length is out of range')

    if module.params.get('name'):
        name = module.params.get('name')
        try:
            interface = Interface(device, name)
            name_exist =True
        except PYHPError as e:
            safe_fail(module,
                      device,
                      descr='There was problem recognizing that interface.',
                      msg=str(e))
        if name_exist:
            is_ethernet, is_routed = interface._is_ethernet_is_routed()
            if is_ethernet:
                module.fail_json(msg='The interface mode must be routing.'
                                     '\nPlease configure type first by itself,'
                                     '\nthen run again.')                
    else:
        name = ''
        try:
            interface = Interface(device, name)
        except PYHPError as e:
            safe_fail(module,
                      device,
                      descr='There was problem recognizing that interface.',
                      msg=str(e))
    if state =='present':
        if module.params.get('rd'):
            if not module.params.get('vrf'):
                module.fail_json(msg='The \'rd\' parameter must be compatible with:'
                                     '\nvrf.'
                                     '\nPlease configure type first by itself,'
                                     '\nthen run again.')
        if module.params.get('addrfamily'):
            if not module.params.get('vrf') or not module.params.get('rttype')\
                        or not module.params.get('rtentry'):
                module.fail_json(msg='The \'addrfamily\' parameter must be compatible with:'
                                     '\nvrf, rttype, rtentry.'
                                     '\nPlease configure type first by itself,'
                                     '\nthen run again.')
        if module.params.get('family'):
            if not module.params.get('sessaf') or not module.params.get('ipaddr')\
                        or not module.params.get('mask'):
                module.fail_json(msg='The \'family\' parameter must be compatible with:'
                                     '\nsessaf, ipaddr, mask.'
                                     '\nPlease configure type first by itself,'
                                     '\nthen run again.')
    if state =='absent':
        if module.params.get('addrfamily'):
            if not module.params.get('vrf') or not module.params.get('rttype')\
                        or not module.params.get('rtentry'):
                module.fail_json(msg='The \'addrfamily\' parameter must be compatible with:'
                                     '\nvrf, rttype,rtentry,when you want to delete the configurations.'
                                     '\nPlease configure type first by itself,'
                                     '\nthen run again.')
    evpn=Evpn(device,name)
    if state == 'present':
        if module.params.get('rd'):
            evpn.create_evpn(stage = True, vrf=vrf, rd=rd)
        if module.params.get('addrfamily'):
            args = dict(addrfamily = str(module.params.get('addrfamily')), rttype=str(module.params.get('rttype')))
            evpn.comfigue_evpn_rt(stage = True, vrf=vrf, rtentry=rtentry, **args)
        if module.params.get('asnum') and not module.params.get('sessaf'):
            evpn.create_bgp_instance(stage = True, asnum=asnum)
        if module.params.get('asnum') and module.params.get('sessaf'):
            EVpn = EVPN(device, asnum, bgp_name, ipaddr, mask, vrf)
            EVpn.build(stage=True)
        if module.params.get('aftype') and module.params.get('family'):
            arg = dict(aftype = module.params.get('aftype'))
            evpn.entry_bgp_view(stage = True, **arg)
            args = dict(family = str(module.params.get('family')), sessaf=str(module.params.get('sessaf')))
            evpn.publish_bgp_route(stage = True,ipaddr=ipaddr, mask=mask, **args)   
    if state=='absent':
        if module.params.get('vrf') and not module.params.get('addrfamily'):
            evpn.remove_evpn_rd(stage = True,vrf=vrf)
        if module.params.get('addrfamily'):
            args = dict(addrfamily = str(module.params.get('addrfamily')), rttype=str(module.params.get('rttype')))
            evpn.remove_evpn_rt(stage = True, vrf=vrf, rtentry=rtentry, **args)
        if del_bgp == 'true':
            evpn.remove_bgp_instance(stage = True)
    existing = True
    commands = None
    end_state = True

    if device.staged:
        commands = device.staged_to_string()
        if module.check_mode:
            safe_exit(module, device, changed=True,
                      commands=commands)
        else:
            try:
                device.execute_staged()
                #end_state = interface.get_config()
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
