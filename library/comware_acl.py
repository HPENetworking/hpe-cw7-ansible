#!/usr/bin/python

DOCUMENTATION = """
---

module: comware_acl
short_description: Configure the acl issue to be applied to the interface.
description:
    -Configure the acl issue to be applied to the interface.
version_added: 1.8
category: Feature (RW)
author: null
notes:
    - When using this feature, "acliid" and "groupcg" are required parameters.
    - You must select a groupcategory when configurating the acl.
    - If you want to configure rule,you need to configure the acl first.
      The rule value range 0 to 65535.The value 65535 is an invalid rule ID.
      If you want to configure acl advanded,the acl id rang from 3000 to 3999.
    - If you want to configure acl basic,the acl id rang from 2000 to 2999.
    - When you want to create an rule, you must have a "aclid" and "action" and "scripaddr".
    - When you want to apply an rule to the interface, you must configure "aclid" and "groupcg".
    - You cannot have a "groupcg" parameter when deleting a rule.

options:
    aclid:
        description:
            - The ID of ACL
        aclid: true
        default: null
        choices: []
        aliases: []
    name:
        description:
            - Full name of the interface
        required: false
        default: null
        choices: []
        aliases: []
    state:
        description:
            - Desired state for the interface configuration
        required: false
        default: present
        choices: ['present', 'absent']
        aliases: []
    ruleid:
        description:
            - The ID of rule
        required: false
        default: null
        choices: []
        aliases: []
    scripaddr:
        description:
            -  Ip source address of rule
        required: false
        default: null
        choices: []
        aliases: []
    action:
        description:
            - Action of the rule
        required: false
        default: null
        choices: ['deny','permit']
        aliases: []
    appdirec:
        description:
            - Direction Applied to the interface
        required: false
        default: null
        choices: ['inbound', 'outbound']
        aliases: []
    groupcg:
        description:
            - ACL groupacategory
        required: false
        default: null
        choices: ['basic', 'advanced']
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

# deploy advanced ACL (IPv4 advanced ACL 3000 to 3999)
- comware_acl: aclid=3010  groupcg=advanced appdirec=inbound username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
# deploy basic ACL (IPv4 basic ACL 2000 to 2999)
- comware_acl: aclid=2010  groupcg=advanced appdirec=inbound username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
# delete advanced ACL
- comware_acl: aclid=3010 groupcg=advanced state=absent username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
# create rule
- comware_acl: aclid=3010 groupcg=advanced ruleid=0 action=deny scripaddr=10.1.1.1 username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
# apply ACL to interface
- comware_acl: aclid=3010 groupcg=advanced name=hun1/2/2 appdirec=inbound username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
# delete rule
- comware_acl: aclid=3010 ruleid=0 state=absent username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
#delete interface ACL application
- comware_acl: aclid=3010 name=hun1/2/2 appdirec=inbound state=absent username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
"""

import socket
import re
try:
    HAS_PYHP = True
    from pyhpecw7.comware import HPCOM7
    from pyhpecw7.features.interface import Interface
    from pyhpecw7.features.errors import *
    from pyhpecw7.errors import *
    from pyhpecw7.features.acl import Acl
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
            aclid=dict(type='str', required=True),
            name=dict(required=False),
            state=dict(choices=['present', 'absent'],
                       default='present'),
            ruleid=dict(type='str'),
            scripaddr=dict(type='str'),
            action=dict(choices=['deny', 'permit']),
            appdirec=dict(choices=['inbound', 'outbound']),
            groupcg=dict(choices=['basic', 'advanced']),
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
    aclid = str(module.params['aclid'])
    ruleid= module.params['ruleid']
    scripaddr=module.params['scripaddr']
    action = str(module.params['action'])
    appdirec = module.params['appdirec']
    changed = False

    proposed = dict((k, v) for k, v in module.params.items()
                    if v is not None and k not in filtered_keys)

    try:
        look_for_keys = module.params['look_for_keys']
        device.open(look_for_keys=look_for_keys)
    except ConnectionError as e:
        safe_fail(module, device, msg=str(e),
                  descr='Error opening connection to device.')

    if module.params.get('appdirec'):
        if not module.params.get('name'):
            safe_fail(module,msg='appdirec needs to be provided with name')

    if module.params.get('name'):
        name = module.params.get('name')
        try:
            interface = Interface(device, name)
        except PYHPError as e:
            safe_fail(module,
                      device,
                      descr='There was problem recognizing that interface.',
                      msg=str(e))
        if not module.params.get('aclid') or not module.params.get('appdirec'):
            module.fail_json(msg='The type parameter must be compatible with:'
                                 '\naclid, appdirec.'
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
    if state == 'present':
        if module.params.get('ruleid'):
            ruleid = module.params.get('ruleid')
            if not module.params.get('aclid') or not module.params.get('action')\
                        or not module.params.get('scripaddr'):
                module.fail_json(msg='The type parameter must be compatible with:'
                                     '\naclid, action, scripaddr.'
                                     '\nPlease configure type first by itself,'
                                     '\nthen run again.')
        else:
            ruleid = None

    if not module.params.get('aclid'):
        module.fail_json(msg='The type parameter must be set'
                             '\nPlease configure type first by itself,'
                             '\nthen run again.')
    if not module.params.get('scripaddr'):
        scripaddr = None

    acl = Acl(device, aclid, name, ruleid, scripaddr)

    if state == 'present':
        if not module.params.get('groupcg'):
            module.fail_json(msg='The type parameter must be compatible with:'
                                 '\ngroupcg.'
                                 '\nPlease configure type first by itself,'
                                  '\nthen run again.')
   
        else:
            args = dict(groupcg=module.params.get('groupcg'))
            acl.create_acl(stage = True, **args)
            if ruleid:
                acl.create_rule(stage=True, action=action)
                if name !='':
                    arg = dict(appdirec=module.params.get('appdirec'))
                    acl.create_packet_filter(stage=True, **arg)
            if name !='':
                arg = dict(appdirec=module.params.get('appdirec'))
                acl.create_packet_filter(stage=True, **arg)
    else:
        if module.params.get('groupcg'):
            args = dict(groupcg=module.params.get('groupcg'))
            acl.remove_acl(stage = True, **args)
        elif ruleid :
            acl.remove_rule(stage = True)
        if name !='':
            args = dict(appdirec=module.params.get('appdirec'))
            acl.remove_packet_filter(stage = True, **args)
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
