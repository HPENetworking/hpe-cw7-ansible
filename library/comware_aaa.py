#!/usr/bin/python

DOCUMENTATION = """
---

module: comware_aaa
short_description: This module provides AAA related management configuration and applications
description:
   
version_added: 1.8
category: Feature (RW)
author: null
notes: When the state is present , all options are required.
       This module support access type include 'LANaccess','login','super','PPP','default','portal',
       other types to be updated.
       Scheme list include 'HWTACACS','RADIUS','local' are permitted . 
       If the aaa_type is authentication , access_type can't be super .
       If the access_type is super , scheme_list not support for local.

options:
    domain_name:
        description:
            - Configure SSL VPN access instance to use the specified ISP domain for AAA Authentication
        required: true
        default: null
        choices: []
        aliases: []
    aaa_type:
        description:
            - Safety certification method.
        required: false
        default: null
        choices: ['authentication', 'authorization', 'accounting']
        aliases: [] 
    access_type:
        description:
            - Configure authorization methods for LAN access users.
        required: false
        default: null
        choices: ['LANaccess','login','super','PPP', 'default','portal']
        aliases: []  
    scheme_list:
        description:
            - AAA method types
        required: false
        default: null
        choices: ['radius','hwtacacs','local']
        aliases: [] 
    scheme_name_list:
        description:
            - Scheme name list.
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

# Basic Ethernet config
     - name:  create domain myserver and config it
       comware_aaa: domain_name=myserver aaa_type=authentication access_type=login scheme_list=radius \
            scheme_name_list=test username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
     # - name:  delete domain name myserver relates
       # comware_aaa: domain_name=myserver state=default username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
"""

import socket

try:
    HAS_PYHP = True
    from pyhpecw7.comware import HPCOM7
    from pyhpecw7.features.aaa import Aaa
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
            domain_name=dict(required=True),
            aaa_type=dict(choices=['authentication', 'authorization', 'accounting']),
            access_type=dict(choices=['LANaccess','login','super','PPP',\
                                      'default','portal']),
            scheme_list=dict(choices=['radius','hwtacacs','local']),
            scheme_name_list=dict(type='str'),
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
    domain_name = module.params['domain_name']
    scheme_name = module.params['scheme_name_list']
    access_type = module.params['access_type']
    if state == 'present':
        if module.params['aaa_type'] != None and module.params['access_type'] != None and \
                module.params['scheme_list'] != None and module.params['scheme_name_list'] != None:
            pass
        else:
            safe_fail(module,msg='All options are required')

    if access_type == 'LANaccess':
        access_type = 'LAN access'
        module.params.update(access_type=access_type)
    if scheme_name:
        if len(scheme_name) < 10:
            scheme_name_list = '0'+str(len(scheme_name))+scheme_name
        else:
            scheme_name_list = str(len(scheme_name)) + scheme_name
        module.params.update(scheme_name_list=scheme_name_list)
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
        aaa = Aaa(device,domain_name)
    except PYHPError as e:
        safe_fail(module,device,descr='there is problem in setting localuser',
                  msg=str(e))

    try:
        aaa.param_check(**proposed)
    except PYHPError as e:
        safe_fail(module,device,descr='There was problem with the supplied parameters.',
                  msg=str(e))

    try:
        existing_domain = aaa.get_domain_info()
        existing = aaa.get_config()
    except PYHPError as e:
        safe_fail(module, device, msg=str(e),
                  descr='Error getting existing config.')

    if state == 'present':
        delta = dict(set(proposed.items()).difference(
            existing.items()))
        if delta:
            delta_domain = dict(domain_name=domain_name)
            aaa.build(stage=True, **delta_domain)
            aaa.build_aaa(stage=True,**proposed)

    elif state == 'default' or 'absent':
        if domain_name in existing_domain:
            delta = dict(domain_name=domain_name)
            aaa.default(stage=True, **delta)

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
                end_state = aaa.get_config()
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
