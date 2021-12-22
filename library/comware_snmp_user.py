#!/usr/bin/python

DOCUMENTATION = """
---

module: comware_snmp_user
short_description: Manages SNMP user configuration on H3c switches.
description:
    - Manages SNMP community configuration on H3C switches.
version_added: 1.8
category: System (RW)
author: wangliang
options:
    acl_number:
        description:
            - Access control list number.
        required: false
        default: null
    usm_user_name:
        description:
            - Unique name for the user.
        required: true
        default: null
    user_group:
        description:
            - Unique name for the user group.
        required: true
        default: null
    sercurity_model:
        description:
            - The security model by this user is provided.
        required: true
        default: null
        choices: ['v1', 'v2c', 'v3']
    auth_protocol:
        description:
            - Authentication algorithm.
        required: false
        default: null
    priv_protocol:
        description:
            - Encryption algorithm privacy.
        required: false
        default: null
    auth_key:
        description:
            - Authentication key.
        required: false
        default: null
    priv_key:
        description:
            - Privacy key.
        required: false
        default: null
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
         
- name: Config SNMP v3 User
    comware_snmp_user:
      state=present usm_user_name=gtest_w_ansbile sercurity_model=v3 user_group=gtest_w_ansbile
      auth_protocol=sha priv_protocol=3des auth_key=gtest_w_ansbile priv_key=gtest_w_ansbile
      username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

- name: undo SNMP v3 User
    comware_snmp_user:
      state=absent usm_user_name=gtest_w_ansbile sercurity_model=v3 user_group=gtest_w_ansbile
      auth_protocol=sha priv_protocol=3des auth_key=gtest_w_ansbile priv_key=gtest_w_ansbile
      username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

- name: Config SNMP v2c User
    comware_snmp_user:
      state=present usm_user_name=gtest_w_ansbile sercurity_model=v2c user_group=gtest_w_ansbile
      username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

- name: undo SNMP v2c User
    comware_snmp_user:
      state=absent usm_user_name=gtest_w_ansbile sercurity_model=v2c user_group=gtest_w_ansbile
      username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
"""

import socket
import os
import re

try:
    HAS_PYHP = True
    from pyhpecw7.comware import HPCOM7
    from pyhpecw7.features.snmp_user import SnmpUser
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


def param_check_snmp_user(**kwargs):
    """Basic param validation for snmp user

    Args:
        state (str): REQUIRED must be "present" or "absent"
        user: see options
    """

    module = kwargs["module"]
    usm_user_name = module.params['usm_user_name']
    user_group = module.params['user_group']
    sercurity_model = module.params['sercurity_model']
    acl_number = module.params['acl_number']
    auth_protocol = module.params['auth_protocol']
    priv_protocol = module.params['priv_protocol']
    auth_key = module.params['auth_key']
    priv_key = module.params['priv_key']

    if usm_user_name and sercurity_model:
        if sercurity_model != 'v3' and auth_protocol:
            module.fail_json(
                msg='only v3 have auth_protocol config')

        if sercurity_model != 'v3' and priv_protocol:
            module.fail_json(
                msg='only v3 have priv_protocol config')

        if len(user_group) > 32 or len(user_group) == 0:
            module.fail_json(
                msg='Error: The len of user_group %s is out of [1 - 32].' % user_group)

        if acl_number:
            if acl_number.isdigit():
                if int(acl_number) > 3999 or int(acl_number) < 2000:
                    module.fail_json(
                        msg='Error: The value of acl_number %s is out of [2000 - 3999].' % acl_number)
            else:
                if not acl_number[0].isalpha() or len(acl_number) > 32 or len(acl_number) < 1:
                    module.fail_json(
                        msg='Error: The len of acl_number %s is out of [1 - 32] or is invalid.' % acl_number)
    else:
        module.fail_json(
            msg='please provide usm_user_name and sercurity_model at least')


def main():
    module = AnsibleModule(
        argument_spec=dict(
            state=dict(choices=['present', 'absent'], default='present'),
            acl_number=dict(type='str'),
            usm_user_name=dict(required=True, type='str'),
            user_group=dict(required=True, type='str'),
            sercurity_model=dict(required=True, choices=['v1', 'v2c', 'v3']),
            auth_protocol=dict(choices=['md5', 'sha']),
            priv_protocol=dict(choices=['3des', 'aes128', 'aes192', 'aes256', 'des56']),
            auth_key=dict(type='str'),
            priv_key=dict(type='str'),
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
    user_group = module.params['user_group']
    sercurity_model = module.params['sercurity_model']
    acl_number = module.params['acl_number']
    auth_protocol = module.params['auth_protocol']
    priv_protocol = module.params['priv_protocol']
    auth_key = module.params['auth_key']
    priv_key = module.params['priv_key']

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

    if usm_user_name:
        try:
            snmp_user_obj = SnmpUser(device, usm_user_name, user_group, sercurity_model)
        except PYHPError as e:
            safe_fail(module,
                      device,
                      descr='There was problem recognizing that usm_user_name.',
                      msg=str(e))

        try:
            param_check_snmp_user(module = module)
        except PYHPError as e:
            safe_fail(module,
                      device,
                      descr='There was problem with the supplied parameters.',
                      msg=str(e))

        try:
            existing = snmp_user_obj.get_config()
        except PYHPError as e:
            safe_fail(module, device, msg=str(e),
                      descr='Error getting existing config.')

        if state == 'present':
            # delta = dict(set(proposed.iteritems()).difference(
            #     existing.iteritems()))
            # if delta:
            snmp_user_obj.user_build(stage=True, **proposed)
        elif state == 'absent':
            if existing:
                snmp_user_obj.user_remove(stage=True, **proposed)

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
                    end_state = snmp_user_obj.get_config()
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
