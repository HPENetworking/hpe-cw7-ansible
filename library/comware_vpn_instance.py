#!/usr/bin/python

DOCUMENTATION = """
---

module: comware_instance_rely
short_description: config instance rely ensure some instance configs can be set
description:
    - config instance rely ip vpn-instance and route-distinguisher 
version_added: 1.8
category: Feature (RW)
author:hanyangyang
notes:
    - some of the instance configs can be set before ip vpn-instance and route-distinguisher already 
      exists . 
    - state default or absent will make the device default config , if you want delete instance insance
      autonomous_system and instance_instance are both required . if  you want delete vpn_instance, 
      provide vpn_instance is OK.
options:     
    vpn_instance:
        description:
            - Name of the VPN instance
        required: True
        default: null
        choices: []
        aliases: []          
    vpn_instance_rd:
        description:
            - Route distinguisher, in the format ASN:nn or IP_address:nn
        required: False
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
     - name:  create and config ip vpn-instance
       comware_vpn_instance: vpn_instance=vpna vpn_instance_rd=1:1  address_family=ipv4  vpn_target=2:2 vpn_target_mode=both \
       username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

     - name:  create and config ip vpn-instance
       comware_vpn_instance: vpn_instance=vpna vpn_instance_rd=1:1  address_family=evpn  vpn_target=1:1 vpn_target_mode=both \
       username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

     - name:  create and config ip vpn-instance
       comware_vpn_instance: vpn_instance=vpna state=default username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
"""

import socket

try:
    HAS_PYHP = True
    from pyhpecw7.comware import HPCOM7
    from pyhpecw7.features.vpn_instance import Instance
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
            vpn_instance=dict(required=True,type='str'),
            vpn_instance_rd=dict(type='str'),
            address_family=dict(choices=['evpn', 'ipv4', 'ipv6']),
            vpn_target=dict(type='str'),
            vpn_target_mode=dict(choices=['both', 'export', 'import']),
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
    vpn_instance = module.params['vpn_instance']
    vpn_instance_rd = module.params['vpn_instance_rd']
    address_family = module.params['address_family']
    vpn_target = module.params['vpn_target']
    vpn_target_mode = module.params['vpn_target_mode']
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
        instance = Instance(device,vpn_instance)
    except PYHPError as e:
        safe_fail(module,device,descr='there is problem in creating ip vpn-instance',
                  msg=str(e))

    try:
        instance.param_check(**proposed)
    except PYHPError as e:
        safe_fail(module,device,descr='There was problem with the supplied parameters.',
                  msg=str(e))

    try:
        existing = instance.get_config()
    except PYHPError as e:
        safe_fail(module, device, msg=str(e),
                  descr='Error getting existing config.')

    if state == 'present':
        delta = proposed
        if delta:
            delta_vpn_instance = dict(vpn_instance=vpn_instance,\
                                      vpn_instance_rd=vpn_instance_rd,\
                                      address_family=address_family,\
                                      vpn_target=vpn_target,\
                                      vpn_target_mode=vpn_target_mode,
                                      )
            instance.build_vpn(stage=True,**delta_vpn_instance)

    elif state == 'default':
        delta_vpn_instance = dict(vpn_instance=vpn_instance)
        instance.remove_vpn(stage=True, **delta_vpn_instance)

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
                end_state = instance.get_config()
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
