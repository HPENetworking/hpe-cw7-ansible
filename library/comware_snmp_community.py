#!/usr/bin/python

DOCUMENTATION = """
---

module: comware_snmp_community
short_description: Manages SNMP community configuration on H3C switches.
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
    community_name:
        description:
            - Unique name to identify the community.
        required: false
        default: null
    access_right:
        description:
            - Access right read or write.
        required: false
        default: null
        choices: ['read','write']
    community_mib_view:
        description:
            - Mib view name.
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

- name: "Config SNMP group"
    comware_snmp_group:
      comware_snmp_community: state=present access_right=read community_mib_view=view community_name=ansible_gqy  
      acl_number=3000 username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
      
- name: "Undo SNMP community"
    comware_snmp_community: state=absent access_right=write community_mib_view=view community_name=ansible_gqy  
    acl_number=2000 username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
"""

import socket
import os
import re

try:
    HAS_PYHP = True
    from pyhpecw7.comware import HPCOM7
    from pyhpecw7.features.snmp_community import SnmpCommunity
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

def param_check_snmp_community(**kwargs):
    """Basic param validation for snmp community.
    """
    module = kwargs["module"]
    community_name = module.params['community_name']
    access_right = module.params['access_right']
    community_mib_view = module.params['community_mib_view']
    acl_number = module.params['acl_number']
    if community_name and access_right:
        if len(community_name) > 32 or len(community_name) == 0:
            module.fail_json(
                msg='Error: The len of community_name %s is out of [1 - 32].' % community_name)

        if acl_number:
            if acl_number.isdigit():
                if int(acl_number) > 3999 or int(acl_number) < 2000:
                    module.fail_json(
                        msg='Error: The value of acl_number %s is out of [2000 - 3999].' % acl_number)
            else:
                if not acl_number[0].isalpha() or len(acl_number) > 32 or len(acl_number) < 1:
                    module.fail_json(
                        msg='Error: The len of acl_number %s is out of [1 - 32] or is invalid.' % acl_number)

        if community_mib_view:
            if len(community_mib_view) > 32 or len(community_mib_view) == 0:
                module.fail_json(
                    msg='Error: The len of community_mib_view %s is out of [1 - 32].' % community_mib_view)

    else:
        module.fail_json(
            msg='please provide community_name and access_right')


def main():
    module = AnsibleModule(
        argument_spec=dict(
            state=dict(choices=['present', 'absent'], default='present'),
            acl_number=dict(type='str'),
            community_name=dict(type='str'),
            access_right=dict(choices=['read', 'write']),
            community_mib_view=dict(type='str', default='ViewDefault'),
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

    proposed = dict()
    existing = dict()
    end_state = dict()
    changed = False

    filtered_keys = ('hostname', 'username', 'password', 'state',
                     'port', 'look_for_keys')

    state = module.params['state']
    acl_number = module.params['acl_number']
    community_name = module.params['community_name']
    community_mib_view = module.params['community_mib_view']
    access_right = module.params['access_right']

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

    if community_name:
        try:
            snmp_community_obj = SnmpCommunity(device, community_name)
        except PYHPError as e:
            safe_fail(module,
                      device,
                      descr='There was problem recognizing that community_name.',
                      msg=str(e))

        try:
            param_check_snmp_community(module=module)
        except PYHPError as e:
            safe_fail(module,
                      device,
                      descr='There was problem with the supplied parameters.',
                      msg=str(e))

        try:
            existing = snmp_community_obj.get_config()
        except PYHPError as e:
            safe_fail(module, device, msg=str(e),
                      descr='Error getting existing config.')

        if state == 'present':

            snmp_community_obj.create_build(stage=True, **proposed)
        elif state == 'absent':
            if existing:
                snmp_community_obj.commmunity_remove(stage=True, **proposed)

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
                    end_state = snmp_community_obj.get_config()
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
