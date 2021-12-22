#!/usr/bin/python

DOCUMENTATION = """
---

module: comware_snmp_group
short_description: Manages SNMP group configuration on H3C switches.
description:
    - Manages SNMP group configuration on H3C switches.
version_added: 1.8
category: System (RW)
author: wangliang
options:
    acl_number:
        description:
            - Access control list number.
        required: false
        default: null
    version:
        description:
            - The security model by this user is provided.
        required: true
        default: null
    group_name:
        description:
            - Unique name for the group.
        required: false
        default: null
    security_level:
        description:
            - Security level indicating whether to use authentication and encryption.
        required: false
        default: null
        choices: ['noAuthNoPriv', 'authentication']
    read_view:
        description:
            - Mib view name for read.
        required: false
        default: null
    write_view:
        description:
            - Mib view name for write.
        required: false
        default: null
    notify_view:
        description:
            - Mib view name for notification.
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
   comware_snmp_group: state=present version=v2c group_name=wdz_group security_level=noAuthNoPriv acl_number=2000 
   username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
      
- name: "Undo SNMP group"
  comware_snmp_group: state=absent  version=v2c group_name=wdz_group security_level=noAuthNoPriv acl_number=2000 
   username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
    
- name: Config SNMP V3 group
    comware_snmp_group:
      state=present group_name=test_wl version=v3 security_level=authentication  acl_number=3000  write_view='testv3c'
      username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
      
- name: Config SNMP V3 group
    comware_snmp_group:
      state=absent group_name=test_wl version=v3 security_level=authentication  acl_number=3000  write_view='testv3c'
      username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
"""

import socket
import os
import re

try:
    HAS_PYHP = True
    from pyhpecw7.comware import HPCOM7
    from pyhpecw7.features.snmp_group import SnmpGroup
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


def param_check_snmp_group(**kwargs):
    """Basic param validation for community snmp group

    Args:
        state (str): REQUIRED must be "present" or "absent"
        community: see options
    """

    module = kwargs["module"]
    group_name = module.params['group_name']
    version = module.params['version']
    security_level = module.params['security_level']
    acl_number = module.params['acl_number']
    read_view = module.params['read_view']
    write_view = module.params['write_view']
    notify_view = module.params['notify_view']

    if group_name and version and security_level:
        if version != 'v3' and security_level != 'noAuthNoPriv':
            module.fail_json(
                msg='only v3 have another choice for security_level')

        if len(group_name) > 32 or len(group_name) == 0:
            module.fail_json(
                msg='Error: The len of group_name %s is out of [1 - 32].' % group_name)

        if acl_number:
            if acl_number.isdigit():
                if int(acl_number) > 3999 or int(acl_number) < 2000:
                    module.fail_json(
                        msg='Error: The value of acl_number %s is out of [2000 - 3999].' % acl_number)
            else:
                if not acl_number[0].isalpha() or len(acl_number) > 32 or len(acl_number) < 1:
                    module.fail_json(
                        msg='Error: The len of acl_number %s is out of [1 - 32] or is invalid.' % acl_number)

        if read_view:
            if len(read_view) > 32 or len(read_view) < 1:
                module.fail_json(
                    msg='Error: The len of read_view %s is out of [1 - 32].' % read_view)

        if write_view:
            if len(write_view) > 32 or len(write_view) < 1:
                module.fail_json(
                    msg='Error: The len of write_view %s is out of [1 - 32].' % write_view)

        if notify_view:
            if len(notify_view) > 32 or len(notify_view) < 1:
                module.fail_json(
                    msg='Error: The len of notify_view %s is out of [1 - 32].' % notify_view)
    else:
        module.fail_json(
            msg='please provide group_name, version and security_level')


def main():
    module = AnsibleModule(
        argument_spec=dict(
            state=dict(choices=['present', 'absent'], default='present'),
            acl_number=dict(type='str'),
            group_name=dict(required=True, type='str'),
            version=dict(required=True, choices=['v1', 'v2c', 'v3']),
            security_level=dict(choices=['noAuthNoPriv', 'authentication', 'privacy'], default='noAuthNoPriv'),
            read_view=dict(type='str'),
            write_view=dict(type='str'),
            notify_view=dict(type='str'),
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
    group_name = module.params['group_name']
    version = module.params['version']
    security_level = module.params['security_level']
    read_view = module.params['read_view']
    write_view = module.params['write_view']
    notify_view = module.params['notify_view']

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

    if group_name:
        try:
            snmp_group_obj = SnmpGroup(device, group_name, version, security_level)
        except PYHPError as e:
            safe_fail(module,
                      device,
                      descr='There was problem recognizing that group_name.',
                      msg=str(e))

        try:
            param_check_snmp_group(module = module)
        except PYHPError as e:
            safe_fail(module,
                      device,
                      descr='There was problem with the supplied parameters.',
                      msg=str(e))

        try:
            existing = snmp_group_obj.get_config()
        except PYHPError as e:
            safe_fail(module, device, msg=str(e),
                      descr='Error getting existing config.')

        if state == 'present':
            # delta = dict(set(proposed.iteritems()).difference(
            #     existing.iteritems()))
            # if delta:
            snmp_group_obj.group_build(stage=True, **proposed)
        elif state == 'absent':
            if existing:
                snmp_group_obj.group_remove(stage=True, **proposed)

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
                    end_state = snmp_group_obj.get_config()
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
