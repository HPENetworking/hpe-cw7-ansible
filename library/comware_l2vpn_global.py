#!/usr/bin/python

DOCUMENTATION = """
---

module: comware_l2vpn_global
short_description: Manage global config state for L2VPN
description:
    - Enable or Disable L2VPN on a HP Comware 7 device
version_added: 1.8
category: Feature (RW)
options:
    state:
        description:
            - Desired state for l2vpn global configuration
        required: true
        default: null
        choices: ['enabled', 'disabled']
        aliases: []
    hostname:
        description:
            - IP Address or hostname of the Comware 7 device that has
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

# enable l2vpn globally
- comware_l2vpn_global: state=enabled username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

"""

import socket
try:
    HAS_PYHP = True
    from pyhpecw7.features.l2vpn import L2VPN
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


def main():

    module = AnsibleModule(
        argument_spec=dict(
            state=dict(choices=['enabled', 'disabled'], required=True),
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

    state = module.params['state']

    changed = False

    try:
        look_for_keys = module.params['look_for_keys']
        device.open(look_for_keys=look_for_keys)
    except ConnectionError as e:
        safe_fail(module, device, msg=str(e),
                  descr='error opening connection to device')

    try:
        l2vpn = L2VPN(device)
        existing = l2vpn.get_config()
    except PYHPError as e:
        safe_fail(module, device, msg=str(e),
                  descr='error getting existing config')

    if existing != state:
        if state == 'enabled':
            l2vpn.config(stage=True)
        elif state == 'disabled':
            l2vpn.disable(stage=True)

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
                end_state = l2vpn.get_config()
            except PYHPError as e:
                safe_fail(module, device, msg=str(e),
                          descr='error during execution')
            changed = True

    results = {}
    results['proposed'] = state
    results['existing'] = existing
    results['commands'] = commands
    results['changed'] = changed
    results['end_state'] = end_state

    safe_exit(module, device, **results)

from ansible.module_utils.basic import *
main()
