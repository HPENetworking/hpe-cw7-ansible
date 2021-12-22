#!/usr/bin/python

DOCUMENTATION = """
---

module: comware_bgp_af
short_description: Manage address family configs
description:
    - Manage address family configs such as ipv4 ipv6 .
version_added: 1.8
category: Feature (RW)
author:hanyangyang
notes:
    - Address family vpnv4 and vpnv6 has no parameter 'local_pref','frr_policy','policy_target'
      and 'allow_invalid_as'.
    - Different af options cannot be configured at the same time , for example , address family
      ipv4 and ipv6 must be config in different task.
    - Default state will directly delete bgp as, please use it with carefully
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
    address_familys:
        description:
            - Specify an address family
        required: false
        default: null
        choices: ['ipv4', 'ipv6', 'vpnv4','vpnv6']
        aliases: []
    local_pref:
        description:
            - Set the default local preference value
        required: false
        default: null
        choices: []
        aliases: []
    frr_policy:
        description:
            - Configure fast reroute policy
        required: false
        default: false
        choices: ['true', 'false']
        aliases: []
    policy_target:
        description:
            - Filter VPN4 routes with VPN-Target attribute
        required: false
        default: true
        choices: ['true', 'false']
        aliases: []
    route_select_delay:
        description:
            - Set the delay time for optimal route selection
        required: false
        default: null
        choices: []
        aliases: []
    allow_invalid_as:
        description:
            - Apply the origin AS validation state to optimal route selection
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
 - name:  Configue bgp ipv4 address family
   comware_bgp_af: bgp_as=10 bgp_instance=test address_familys=ipv4 local_pref=20 frr_policy=true \
    username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
 - name:  Configue bgp vpnv4 address family
   comware_bgp_af: bgp_as=10 bgp_instance=test address_familys=vpnv4 route_select_delay=20  \
   username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

"""

import socket

try:
    HAS_PYHP = True
    from pyhpecw7.comware import HPCOM7
    from pyhpecw7.features.bgp_af import Bgp
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
            bgp_instance=dict(required=False, type='str'),
            address_familys=dict(choices=['ipv4', 'ipv6', 'vpnv4','vpnv6']),
            local_pref=dict(type='str'),
            frr_policy=dict(choices=['true', 'false']),
            policy_target=dict(choices=['true', 'false']),
            route_select_delay=dict(type='str'),
            allow_invalid_as=dict(choices=['true', 'false']),
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
    bgp_as = module.params['bgp_as']
    bgp_instance = module.params['bgp_instance']
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
        bgp = Bgp(device,)
    except BgpAfParamsError as params_e:
        safe_fail(module,device,msg=str(params_e))
    except BgpAfConfigError as config_e:
        safe_fail(module,device,msg=str(config_e))
    except PYHPError as e:
        safe_fail(module, device, msg=str(e))

    try:
        bgp.param_check(**proposed)
    except PYHPError as e:
        safe_fail(module,device,
                  descr='There was problem with the supplied parameters.',
                  msg=str(e))

    try:
        existing = bgp.get_config()
    except PYHPError as e:
        safe_fail(module, device, msg=str(e),
                  descr='Error getting existing config.')

    if state == 'present':
        delta = proposed
        if delta:
            bgp.build_bgp_af(stage=True, **delta)

    elif state == 'default':
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
