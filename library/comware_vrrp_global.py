#!/usr/bin/python


DOCUMENTATION = """
---

module: comware_vrrp_global
short_description: Manage VRRP global configuration mode
description:
    - Manage VRRP global configuration mode
version_added: 1.8
category: Feature (RW)
options:
    mode:
        description:
            - vrrp config mode for the switch
        required: true
        default: null
        choices: ['standard', 'load-balance']
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
EXAMPLES = """

# configure load-balance mode
- comware_vrrp_global: mode=load-balance username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

"""

import socket
try:
    HAS_PYHP = True
    from pyhpecw7.comware import HPCOM7
    from pyhpecw7.features.errors import *
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


def get_existing(device):
    rsp = device.cli_display('display vrrp verbose').split('\n')
    existing_mode = 'unknown'
    for line in rsp:
        if 'mode' in line:
            existing_mode = line.split(':')[-1].strip().lower()
            if existing_mode == 'load balance':
                existing_mode = 'load-balance'
    return existing_mode


def main():
    module = AnsibleModule(
        argument_spec=dict(
            mode=dict(required=True, choices=['load-balance', 'standard']),
            port=dict(default=830, type='int'),
            hostname=dict(required=True),
            username=dict(required=True),
            password=dict(required=False, default=None),
            look_for_keys=dict(default=False, type='bool'),
        ),
        supports_check_mode=True
    )
    if not HAS_PYHP:
        module.fail_json(msg='There was a problem loading from the pyhpecw7 '
                         + 'module.', error=str(ie))

    username = module.params['username']
    password = module.params['password']
    port = module.params['port']
    hostname = socket.gethostbyname(module.params['hostname'])

    device_args = dict(host=hostname, username=username,
                       password=password, port=port)

    device = HPCOM7(**device_args)

    mode = module.params['mode']

    changed = False
    delta = False

    try:
        look_for_keys = module.params['look_for_keys']
        device.open(look_for_keys=look_for_keys)
    except ConnectionError as e:
        safe_fail(module, device, msg=str(e),
                  descr='error opening connection' )

    try:
        existing = get_existing(device)
    except PYHPError as e:
        safe_fail(module, device, msg=str(e),
                  descr='error getting existing config')

    end_state = existing
    if existing != mode:
        delta = True

    if delta:
        if mode == 'load-balance':
            command = 'vrrp mode {0}'.format(mode)
        elif mode == 'standard':
            command = 'undo vrrp mode'
        device.stage_config(command, "cli_config")

    commands = None
    response = None

    if device.staged:
        commands = device.staged_to_string()
        if module.check_mode:
            device.close()
            safe_exit(module, device, changed=True,
                      commands=commands)
        else:
            try:
                response = device.execute_staged()
                end_state = get_existing(device)
            except PYHPError as e:
                safe_fail(module, device, msg=str(e),
                          descr='error during execution')

            changed = True

    results = {}
    results['proposed'] = mode
    results['existing'] = existing
    results['commands'] = commands
    results['changed'] = changed
    results['end_state'] = end_state
    results['response'] = response

    safe_exit(module, device, **results)

from ansible.module_utils.basic import *
main()
