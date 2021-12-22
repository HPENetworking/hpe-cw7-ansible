#!/usr/bin/python

DOCUMENTATION = """
---

module: comware_hwtacacs
short_description: Manage hwtacacs scheme
description:
    - Manage hwtacacs scheme
version_added: 1.8
category: Feature (RW)
author:hanyangyang
notes:
    - authentication host name can not set together with authentication ip
      authorization host name can not set together with authorization ip
      accounting host name can not set together with accounting ip
options:
    hwtacacs_scheme_name:
        description:
            - hwtacacs scheme name
        required: True
        default: null
        choices: []
        aliases: []
    priority:
        description:
            - Specify the primary or secondary HWTACACS server
        required: false
        default: null
        choices: ['primary', 'secondary']
        aliases: []  
    auth_host_name:
        description:
            - Specify the primary HWTACACS authentication server name
        required: false
        default: null
        choices: []
        aliases: []  
    auth_host_ip:
        description:
            - authentication ip address
        required: false
        default: null
        choices: []
        aliases: []     
    auth_host_port:
        description:
            - port number, 49 by default
        required: false
        default: '49'
        choices: []
        aliases: []      
    author_host_name:
        description:
            - Specify the primary HWTACACS authorization server name
        required: false
        default: '49'
        choices: []
        aliases: []       
    author_host_ip:
        description:
            - authorization ip address
        required: false
        default: null
        choices: []
        aliases: []    
    author_host_port:
        description:
            - port number, 49 by default
        required: false
        default: '49'
        choices: []
        aliases: []   
    acct_host_name:
        description:
            - Specify the primary HWTACACS accounting server name
        required: false
        default: null
        choices: []
        aliases: []     
    acct_host_ip:
        description:
            - accounting ip address
        required: false
        default: null
        choices: []
        aliases: []   aliases: []     
    acct_host_port:
        description:
            - port number, 49 by default
        required: false
        default: '49'
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

# config hwtacacs scheme
- comware_hwtacacs: hwtacacs_scheme_name=test priority=primary auth_host_ip=192.168.1.186 auth_host_port=48 username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

"""

import socket

try:
    HAS_PYHP = True
    from pyhpecw7.comware import HPCOM7
    from pyhpecw7.features.hwtacacs import Hwtacacs
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
            hwtacacs_scheme_name=dict(required=True),
            priority=dict(choices=['primary', 'secondary',]),
            auth_host_name=dict(type='str'),
            auth_host_ip=dict(type='str'),
            auth_host_port=dict(type='str',default='49'),
            author_host_name=dict(type='str'),
            author_host_ip=dict(type='str'),
            author_host_port=dict(type='str', default='49'),
            acct_host_name=dict(type='str'),
            acct_host_ip=dict(type='str'),
            acct_host_port=dict(type='str', default='49'),
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
    hwtacacs_scheme_name = module.params['hwtacacs_scheme_name']
    priority = module.params['priority']

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
        hwtacacs_scheme = Hwtacacs(device,hwtacacs_scheme_name,priority)
    except PYHPError as e:
        safe_fail(module,device,descr='there is problem in setting hwtacacs_scheme',
                  msg=str(e))
    if module.params['auth_host_name'] and module.params['auth_host_ip']:
        safe_fail(module,msg='Only one of authentication name and ip is effective.')

    if module.params['author_host_name'] and module.params['author_host_ip']:
        safe_fail(module,msg='Only one of authorization name and ip is effective.')

    if module.params['acct_host_name'] and module.params['acct_host_ip']:
        safe_fail(module,msg='Only one of accounting name and ip is effective')

    if state == 'present':
        if not priority:
            if module.params['auth_host_name'] or module.params['auth_host_ip'] or \
               module.params['author_host_name'] or module.params['author_host_ip'] or \
               module.params['acct_host_name'] or module.params['acct_host_ip']:
                safe_fail(module, msg='please assign priority ')

    try:
        hwtacacs_scheme.param_check(**proposed)
    except PYHPError as e:
        safe_fail(module,device,descr='There was problem with the supplied parameters.',
                  msg=str(e))

    try:
        existing = hwtacacs_scheme.get_config()
    except PYHPError as e:
        safe_fail(module, device, msg=str(e),
                  descr='Error getting existing config.')

    if state == 'present':
        delta = dict(set(proposed.items()).difference(
            existing.items()))
        if delta:
            delta_hwtacacs = dict(hwtacacs_scheme_name=hwtacacs_scheme_name)
            hwtacacs_scheme.build(stage=True,**delta_hwtacacs)
            hwtacacs_scheme.build_host_name_ip(stage=True,**delta)
    elif state == 'default':
        if hwtacacs_scheme_name:
            delta = dict(hwtacacs_scheme_name=hwtacacs_scheme_name)
            hwtacacs_scheme.default(stage=True,**delta)

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
                end_state = hwtacacs_scheme.get_config()
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
