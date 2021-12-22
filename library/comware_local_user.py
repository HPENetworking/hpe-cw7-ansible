#!/usr/bin/python

DOCUMENTATION = """
---

module: comware_local_user
short_description: Manage local_user
description:
    - Manage local_user
version_added: 1.8
category: Feature (RW)
author:hanyangyang
notes:
    - Before using ftp_dir , ensure it already exist in the device.
    - Local user group specify the user group , if the device has the group then do the config , 
        if not , create group and config
options:
    localusername:
        description:
            - Local user name
        required: True
        default: null
        choices: []
        aliases: []
    group:
        description:
            - User group name
        required: false
        default: null
        choices: []
        aliases: []
    server_ftp
        description:
            - enable or disable local user service-type ftp
        required: false
        default: null
        choices: ['true', 'false']
        aliases: []    
    server_http
        description:
            - enable or disable local user service-type http
        required: false
        default: null
        choices: ['true', 'false']
        aliases: []    
    server_https
        description:
            - enable or disable local user service-type https
        required: false
        default: null
        choices: ['true', 'false']
        aliases: []
    server_pad
        description:
            - enable or disable local user service-type pad
        required: false
        default: null
        choices: ['true', 'false']
        aliases: []
    server_ssh
        description:
            - enable or disable local user service-type ssh
        required: false
        default: null
        choices: ['true', 'false']
        aliases: []
    server_telnet
        description:
            - enable or disable local user service-type telnet
        required: false
        default: null
        choices: ['true', 'false']
        aliases: []      
    server_Terminal
        description:
            - enable or disable local user service-type Terminal
        required: false
        default: null
        choices: ['true', 'false']
        aliases: []
    ftp_dir:
        description:
            - Specify work directory of local user
        required: false
        default: null
        choices: []
        aliases: []
    local_user_level:
        description:
            - Specify local user work level
        required: false
        default: null
        choices: []
        aliases: []
    localspassword:
        description:
            - Password used to login to the local user
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
- Before using ftp_dir , ensure it already exist in the device.   e.g. flash:/
- comware_local_user: localusername=test server_ftp=True local_user_level=15 username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

"""

import socket

try:
    HAS_PYHP = True
    from pyhpecw7.comware import HPCOM7
    from pyhpecw7.features.local_user import Local_user
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
            localusername=dict(required=True),
            group=dict(type='str'),
            server_ftp=dict(choices=['true', 'false'],default='false'),
            server_http=dict(choices=['true', 'false'],default='false'),
            server_https=dict(choices=['true', 'false'],default='false'),
            server_pad=dict(choices=['true', 'false'],default='false'),
            server_ssh=dict(choices=['true', 'false'],default='false'),
            server_telnet=dict(choices=['true', 'false'],default='false'),
            server_Terminal=dict(choices=['true', 'false'],default='false'),
            ftp_dir=dict(type='str'),
            local_user_level=dict(type='str'),
            localspassword=dict(type='str'),
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
    localusername = module.params['localusername']
    server_ftp = module.params['server_ftp']
    server_http = module.params['server_http']
    server_https = module.params['server_https']
    server_pad = module.params['server_pad']
    server_ssh = module.params['server_ssh']
    server_telnet = module.params['server_telnet']
    server_Terminal = module.params['server_Terminal']
    local_user_level = module.params['local_user_level']
    group = module.params['group']

    changed = False
    proposed = dict((k, v) for k, v in module.params.items()
                    if v is not None and k not in filtered_keys)

    if server_ftp == 'True':
        if server_http or server_https or server_pad or \
            server_ssh or server_telnet or server_Terminal:
            safe_fail(module,msg="local user can't be this in ['http'\
                                'https','pad','ssh','telnet','terminal'] \
                                while ftp has been set")
    try:
        look_for_keys = module.params['look_for_keys']
        device.open(look_for_keys=look_for_keys)
    except ConnectionError as e:
        safe_fail(module, device, msg=str(e),
                  descr='Error opening connection to device.')

    try:
        local_user = Local_user(device,localusername)
    except PYHPError as e:
        safe_fail(module,device,descr='there is problem in setting localuser',
                  msg=str(e))

    try:
        local_user.param_check(**proposed)
    except PYHPError as e:
        safe_fail(module,device,descr='There was problem with the supplied parameters.',
                  msg=str(e))


    try:
        existing = local_user.get_config()
        existing_groups = local_user.get_group_info()
    except PYHPError as e:
        safe_fail(module, device, msg=str(e),
                  descr='Error getting existing config.')

    if state == 'present':
        if group in existing_groups or group == None:
            pass
        else:
            local_user.build_group(stage=True,group=group)
        delta = dict(set(proposed.items()).difference(
            existing.items()))
        if delta:
            if local_user_level:
                del proposed['local_user_level']
                local_user.build(stage=True, **proposed)
                delta_level = dict(localusername=localusername,\
                                   local_user_level=local_user_level)
                local_user.build_user_level(stage=True,**delta_level)
            else:
                local_user.build(stage=True, **proposed)

    elif state == 'default':
        if localusername:
            delta = dict(localusername=localusername)
            local_user.default(stage=True,**delta)

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
                end_state = local_user.get_config()
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
