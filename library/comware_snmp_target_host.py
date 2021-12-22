#!/usr/bin/python

DOCUMENTATION = """
---

module: comware_snmp_target_host
short_description: Manages SNMP user configuration on H3c switches.
description:
    - Manages SNMP target host configuration on H3c switches.
version_added: 1.8
category: System (RW)  
author: wangliang    
options:
    target_type:
        description:
            - Notifications type.
        default: trap
        choices: ['inform', 'trap']
    usm_user_name:
        description:
            - Unique name for the user.
        required: true
        default: null
    server_address:
        description:
            - Address of the remote manage.
        required: true
        default: null
    vpnname:
        description:
            - VRF instance name.
        required: false
        default: null
    user_group:
        description:
            - Unique name for the user group.
        required: true
        default: null
    sercurity_model:
        description:
            - The security model by this user is provided.
        required: false
        default: null
        choices: ['v1', 'v2c', 'v3']
    security_level:
        description:
            - The security level by this user is provided.
        required: false
        default: noAuthNoPriv
        ['noAuthNoPriv', 'authentication', 'privacy']
    state:
        description:
            - Manage the state of the resource.
        required: false
        default: present
        choices: ['present','absent']]
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

EXAMPLE = """
- name: Config SNMP v3 TagetHost
  comware_snmp_target_host:
    state=absent target_type=trap server_address=10.1.1.1 usm_user_name=Uv3
    sercurity_model=v3 security_level=authentication vpnname=testvpn
    username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
          
- name: Undo SNMP v3 TagetHost
  comware_snmp_target_host:
    state=absent target_type=trap server_address=10.1.1.1 usm_user_name=Uv3
    vpnname=testvpn
    username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

- name: Config SNMP TagetHost
  comware_snmp_target_host:
    state=present target_type=trap server_address=100.1.1.1 usm_user_name=testuv2c 
    sercurity_model=v2c
    username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
          
- name: Undo SNMP TagetHost
  comware_snmp_target_host:
    state=present target_type=trap server_address=100.1.1.1 usm_user_name=testuv2c 
    sercurity_model=v2c vpnname=testvpn
    username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
"""

import socket
import os
import re

try:
    HAS_PYHP = True
    from pyhpecw7.comware import HPCOM7
    from pyhpecw7.features.snmp_target_host import SnmpTargetHost
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


def param_check_snmp_target_host(**kwargs):
    """Basic param validation for targethost

    Args:
        state (str): REQUIRED must be "present" or "absent"
        community: see options
    """

    module = kwargs["module"]
    usm_user_name = module.params['usm_user_name']
    target_type = module.params['target_type']
    vpnname = module.params['vpnname']
    server_address = module.params['server_address']
    sercurity_model = module.params['sercurity_model']
    security_level = module.params['security_level']

    if usm_user_name and server_address and target_type:
        if sercurity_model != 'v3' and security_level != 'noAuthNoPriv':
            module.fail_json(
                msg='only v3 have authentication and privacy config')

        if len(usm_user_name) > 32 or len(usm_user_name) == 0:
            module.fail_json(
                msg='Error: The len of usm_user_name %s is out of [1 - 32].' % usm_user_name)
        if vpnname:
            if len(vpnname) > 32 or len(vpnname) == 0:
                module.fail_json(
                    msg='Error: The len of vpnname %s is out of [1 - 32].' % vpnname)

    else:
        module.fail_json(
            msg='please provide usm_user_name, target_type and server_address at least')


def main():
    module = AnsibleModule(
        argument_spec=dict(
            state=dict(choices=['present', 'absent'], default='present'),
            target_type=dict(choices=['inform', 'trap'], default='trap'),
            vpnname=dict(type='str'),
            usm_user_name=dict(required=True, type='str'),
            server_address=dict(required=True, type='str'),
            sercurity_model=dict(choices=['v1', 'v2c', 'v3']),
            security_level=dict(choices=['noAuthNoPriv', 'authentication', 'privacy'], default='noAuthNoPriv'),
            hostname=dict(required=True),
            username=dict(required=True),
            password=dict(required=True, default=None, no_log=True),
            port=dict(type='int', default=830),
            look_for_keys=dict(default=False, type='bool'),
        ),
        supports_check_mode=True
    )

    if not HAS_PYHP:
        safe_fail(module, msg='There was a problem loading from the pyhpecw7 '
                              + 'module.', error=str(ie))

    existing = dict()
    end_state = dict()
    changed = False

    filtered_keys = ('hostname', 'username', 'password', 'state',
                     'port', 'look_for_keys')

    state = module.params['state']
    usm_user_name = module.params['usm_user_name']
    target_type = module.params['target_type']
    sercurity_model = module.params['sercurity_model']
    vpnname = module.params['vpnname']
    server_address = module.params['server_address']
    security_level = module.params['security_level']

    username = module.params['username']
    password = module.params['password']
    port = module.params['port']
    hostname = socket.gethostbyname(module.params['hostname'])

    device_args = dict(host=hostname, username=username,
                       password=password, port=port)

    proposed = dict((k, v) for k, v in module.params.items()
                    if v is not None and k not in filtered_keys)

    device = HPCOM7(**device_args)

    try:
        look_for_keys = module.params['look_for_keys']
        device.open(look_for_keys=look_for_keys)
    except ConnectionError as e:
        safe_fail(module, device, msg=str(e),
                  descr='Error opening connection to device.')

    try:
        snmp_target_host_obj = SnmpTargetHost(device, target_type, server_address, usm_user_name)
    except PYHPError as e:
        safe_fail(module,
                  device,
                  descr='There was problem recognizing that server_address.',
                  msg=str(e))

    try:
        param_check_snmp_target_host(module=module)
    except PYHPError as e:
        safe_fail(module,
                  device,
                  descr='There was problem with the supplied parameters.',
                  msg=str(e))

    try:
        existing = snmp_target_host_obj.get_config()
    except PYHPError as e:
        safe_fail(module, device, msg=str(e),
                  descr='Error getting existing config.')

    if state == 'present':
        # delta = dict(set(proposed.iteritems()).difference(
        #     existing.iteritems()))
        # if delta:
        snmp_target_host_obj.target_host_build(stage=True, **proposed)
    elif state == 'absent':
        if existing:
            snmp_target_host_obj.target_host_remove(stage=True, **proposed)

    commands = None
    end_state = existing

    if device.staged:
        commands = device.staged_to_string()
        if module.check_mode:
            device.close()
            safe_exit(module, device, changed=True,
                      commands=commands)
        else:
            try:
                device.execute_staged()
                end_state = snmp_target_host_obj.get_config()
            except PYHPError as e:
                safe_fail(module, device, msg=str(e),
                          descr='error during execution')
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
