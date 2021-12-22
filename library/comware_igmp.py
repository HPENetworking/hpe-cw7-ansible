#!/usr/bin/python

DOCUMENTATION = """
---

module: comware_igmp
short_description: Configure the igmp issue to be applied to the interface.
description:
    -Configure the acl igmp to be applied to the interface.
version_added: 1.8
category: Feature (RW)
author: liudongxue
notes:
    - When configuring IGMP,the interface must be a routing interface.
    - Parameter 'name' is required when deleting IGMP.

options:
    name:
        description:
            - Full name of the interface
        required: false
        default: null
        choices: []
        aliases: []
    igstate:
        description:
            - The status of IGMP
        required: false
        default: null
        choices: ['enabled', 'disabled']
        aliases: []
    state:
        description:
            - Desired state for the interface configuration
        required: false
        default: present
        choices: ['present', 'absent']
        aliases: []
    version:
        description:
            - The version of IGMP
        required: false
        default: version2
        choices: ['version1', 'version2', 'version3']
        aliases: []
    snstate:
        description:
            -  The state of igmp-snooping 
        required: false
        default: disable
        choices: ['enable', 'disable']
        aliases: []
    mode:
        description:
            - The mode of PIM
        required: false
        default: null
        choices: ['sm', 'dm']
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

# create IGMP and configure IGMP version
- comware_igmp: name=HundredGigE1/2/2 igstate=enabled version=version1 state=present username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
# delete IGMP ,delete IGMP version
- comware_igmp: name=hun1/2/2 igstate=disabled state=absent username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
# configure PIM mode
-  comware_igmp: name=hun1/2/2 mode=dm state=present username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
# delete PIM mode
-  comware_igmp: name=hun1/2/2 mode=dm state=absent username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
# configure IMGP-Snooping
- comware_igmp: snstate=enable state=present username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
# delete IMGP-Snooping
- comware_igmp: snstate=disable state=absent username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
"""

import socket
import re
try:
    HAS_PYHP = True
    from pyhpecw7.comware import HPCOM7
    from pyhpecw7.features.interface import Interface
    from pyhpecw7.features.errors import *
    from pyhpecw7.errors import *
    from pyhpecw7.features.igmp import Igmp
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
            name=dict(type='str'),
            igstate=dict(choices=['enabled', 'disabled']),
            state=dict(choices=['present', 'absent'],
                       default='present'),
            version=dict(choices=['version1', 'version2', 'version3'],
                       default='version2'),
            snstate=dict(choices=['enable', 'disable'],
                       default='disable'),
            mode=dict(choices=['sm', 'dm']),
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
    igstate = str(module.params['igstate'])
    version= module.params['version']
    mode= module.params['mode']
    snstate = module.params['snstate']
    changed = False

    proposed = dict((k, v) for k, v in module.params.items()
                    if v is not None and k not in filtered_keys)

    try:
        look_for_keys = module.params['look_for_keys']
        device.open(look_for_keys=look_for_keys)
    except ConnectionError as e:
        safe_fail(module, device, msg=str(e),
                  descr='Error opening connection to device.')

    
    if module.params.get('name'):
        name = module.params.get('name')
        try:
            interface = Interface(device, name)
        except PYHPError as e:
            safe_fail(module,
                      device,
                      descr='There was problem recognizing that interface.',
                      msg=str(e))
    else:
        name = ''
        try:
            interface = Interface(device, name)
        except PYHPError as e:
            safe_fail(module,
                      device,
                      descr='There was problem recognizing that interface.',
                      msg=str(e))
    is_ethernet, is_routed = interface._is_ethernet_is_routed()
    if state == 'present':
        if igstate == 'enabled':
            if name == '':
                module.fail_json(msg='The \'igstate\' parameter must be compatible with:'
                                     '\nname.'
                                     '\nPlease configure type first by itself,'
                                     '\nthen run again.')
            else:
                if is_ethernet:
                    module.fail_json(msg='The interface type must be a routing mode.'
                                     '\nPlease configure type first by itself,'
                                     '\nthen run again.')
        if module.params.get('mode'):
            mode = module.params.get('mode')
            if name == '':
                module.fail_json(msg='The \'mode\' parameter must be compatible with:'
                                     '\nname.'
                                     '\nPlease configure type first by itself,'
                                     '\nthen run again.')  
            else:
                if is_ethernet:
                    module.fail_json(msg='The interface mode must be route.'
                                     '\nPlease configure type first by itself,'
                                     '\nthen run again.')
    if state == 'absent' and snstate != 'disable':
        if name =='':
            module.fail_json(msg='The \'name\' parameter must be set.'
                                 '\nPlease configure type first by itself,'
                                 '\nthen run again.')
    igmp=Igmp(device,name)
    if state == 'present':
        if is_routed:
            if igstate == 'enabled':
                args = dict(igstate = str(module.params.get('igstate')),version=str(module.params.get('version')))
                igmp.build_igmp(stage = True, **args)
            if mode:
                args = dict(mode = str(module.params.get('mode')))
                igmp.config_pim_mode(stage =True, **args)
        else:
            raise InterfaceAbsentError(name)
        if snstate == 'enable':
            igmp.build_igmp_snooping(stage = True, snstate=snstate)
    elif state == 'absent':
        if is_routed:
            if igstate == 'disabled':
                igmp.remove_igmp(stage = True)
            if mode:
                igmp.remove_pim_mode(stage =True)
        else:
            raise InterfaceAbsentError(name)
        if snstate == 'disable':
            igmp.build_igmp_snooping(stage = True, snstate=snstate)

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
