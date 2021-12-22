#!/usr/bin/python

DOCUMENTATION = """
---

module: comware_bgp_global
short_description: config bgp configs in the bgp instance view such as routerid
description:
    - config bgp configs in the bgp instance view such as routerid
version_added: 1.8
category: Feature (RW)
author:hanyangyang
notes:
    - all the configs except bgp_as and bgp_instance are set in bgp instance view.
    - timer keepalive and time hold must be set together .
    - timer hold must be greater than 3 times timer keepalive.
    - peer relations are need peer ip first.
    - state default and absent are the same , if you want delete the setting configs , the comware
      will undo the bgp_as and instance .
options:
    bgp_as:
        description:
            - Autonomous system number <1-4294967295>
        required: True
        default: null
        choices: []
        aliases: []
    bgp_instance:
        description:
            - Specify a BGP instance by its name
        required: false
        default: null
        choices: []
        aliases: []
    router_id:
        description:
            - Router ID in IP address format
        required: false
        default: null
        choices: []
        aliases: []
    advertise_rib_active:
        description:
            - Advertise the best route in IP routing table
        required: false
        default: false
        choices: ['true', 'false']
        aliases: []
    timer_connect_retry:
        description:
            - Configure the session retry timer for all BGP peers
        required: false
        default: null
        choices: []
        aliases: []
    timer_keepalive:
        description:
            - Keepalive timer ,Value of keepalive timer in seconds
        required: false
        default: null
        choices: []
    timer_hold:
        description:
            - Hold timer , Value of hold timer in seconds
        required: false
        default: null
        choices: []
        aliases: []
    compare_as_med:
        description:
            - Compare the MEDs of routes from different ASs
        required: false
        default: null
        choices: []
        aliases: []
    compare_as_med:
        description:
            - Compare the MEDs of routes from different ASs
        required: false
        default: false
        choices: [true', 'false']
        aliases: []
    peer_ip:
        description:
            - Specify BGP peers IPv4 address
        required: false
        default: null
        choices: []
        aliases: []
    peer_as_num:
        description:
            - Specify BGP peers AS number
        required: false
        default: null
        choices: []
        aliases: []
    peer_ignore:
        description:
            - Disable session establishment with the peers
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

# bgp global views configs
-  comware_bgp_global: bgp_as=10 bgp_instance=test router_id=192.168.1.185 advertise_rib_active=true timer_connect_retry=100 timer_keepalive=100 timer_hold=301 \
   compare_as_med=true peer_ip=1.1.1.3 peer_as_num=10 peer_ignore=true username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

"""

import socket

try:
    HAS_PYHP = True
    from pyhpecw7.comware import HPCOM7
    from pyhpecw7.features.bgp_global import Bgp
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
            bgp_as=dict(required=True,type='str'),
            bgp_instance=dict(required=False,type='str'),
            router_id=dict(type='str'),
            advertise_rib_active=dict(choices=['true', 'false'],
                       default='false'),
            timer_connect_retry=dict(type='str'),
            timer_keepalive=dict(type='str'),
            timer_hold=dict(type='str'),
            compare_as_med=dict(choices=['true', 'false'],
                       default='false'),
            peer_ip=dict(type='str'),
            peer_as_num=dict(type='str'),
            peer_ignore=dict(choices=['true', 'false'],
                       default='false'),
            peer_connect_intf=dict(type='str'),
            address_family=dict(choices=['l2vpn']),
            evpn=dict(choices=['true', 'false'],
                       default='false'),
            peer_state=dict(choices=['true', 'false']),
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
    bgp_as = module.params['bgp_as']
    bgp_instance = module.params['bgp_instance']
    timer_keepalive = module.params['timer_keepalive']
    timer_hold = module.params['timer_hold']
    peer_as_num = module.params['peer_as_num']
    peer_ignore = module.params['peer_ignore']
    peer_connect_intf = module.params['peer_connect_intf']
    evpn = module.params['evpn']
    changed = False
    proposed = dict((k, v) for k, v in module.params.items()
                    if v is not None and k not in filtered_keys)

    try:
        look_for_keys = module.params['look_for_keys']
        device.open(look_for_keys=look_for_keys)
    except ConnectionError as e:
        safe_fail(module, device, msg=str(e),
                  descr='Error opening connection to device.')
    if timer_keepalive:
        if not module.params.get('timer_hold'):
            safe_fail(module,msg='timer keepalive and hold config at the same time')
    if timer_hold:
        if not module.params.get('timer_keepalive'):
            safe_fail(module, msg='timer keepalive and hold config at the same time')
    if timer_keepalive:
        if int(timer_keepalive) < 0 or int(timer_keepalive) >21845:
            safe_fail(module,msg='keepalive time not in the range')
    if timer_hold:
        if int(timer_hold) < 0 or int(timer_hold) >65535:
            safe_fail(module,msg='hold time not in the range')
    if timer_keepalive and timer_hold:
        if int(timer_keepalive)*3 > int(timer_hold):
            safe_fail(module,msg='hold time must be bigger than triple-keepalive time')

    if peer_as_num:
        if int(peer_as_num) < 0 or int(peer_as_num) > 4294967295:
            safe_fail(module, msg='peer_as_num is not in the range')
    if peer_as_num:
        if module.params.get('peer_ip') == None:
            safe_fail(module, msg='peer ip is required when')
    if peer_ignore:
        if module.params.get('peer_ip') == None:
            safe_fail(module, msg='peer ip is required when setting ignore')
    if peer_connect_intf:
        if module.params.get('peer_ip') == None:
            safe_fail(module, msg='peer ip is required when setting connect-interface')
    if evpn == 'true':
        if module.params.get('address_family') == None:
            safe_fail(module, msg='address_family is required when setting evpn')

    if peer_connect_intf:
        try:
            interface = Interface(device, peer_connect_intf)
        except PYHPError as e:
            safe_fail(module, msg='There was problem recognizing that interface.')

        if not interface.iface_exists:
            safe_fail(module,msg='Interfce does not exist , please use comware_interface module create it')

    try:
        bgp = Bgp(device,)
    except PYHPError as e:
        safe_fail(module,device,descr='there is problem in creating bgp instance',
                  msg=str(e))
    try:
        existing = bgp.get_config()
    except PYHPError as e:
        safe_fail(module, device, msg=str(e),
                  descr='Error getting existing config.')

    if state == 'present':
        delta = proposed
        if delta:
            bgp.build_bgp_global(stage=True, **delta)

    elif state == 'default' or 'absent':
        default_bgp = dict(bgp_as=bgp_as,\
                                 bgp_instance=bgp_instance)
        bgp.remove_bgp(stage=True, **default_bgp)

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
                end_state = bgp.get_config()
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
