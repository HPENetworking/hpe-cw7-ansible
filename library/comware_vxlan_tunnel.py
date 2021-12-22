#!/usr/bin/python

DOCUMENTATION = """
---

module: comware_vxlan_tunnel
short_description: Manage VXLAN tunnels on Comware 7 devices
description:
    - Manage VXLAN tunnels on Comware 7 devices
version_added: 1.8
category: Feature (RW)
notes:
  - state=absent removes the tunnel interface if it exists
  - state=absent can also remove non-vxlan tunnel interfaces
options:
    tunnel:
        description:
            - Tunnel interface identifier
        required: true
        default: null
        choices: []
        aliases: []
    global_src:
        description:
            - Global source address for VXLAN tunnels
        required: false
        default: null
        choices: []
        aliases: []
    src:
        description:
            - Source address or interface for the tunnel
        required: false
        default: null
        choices: []
        aliases: []
    dest:
        description:
            - Destination address for the tunnel
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

# ensure tunnel interface 20 exists for vxlan and configures a global source address (although it's not used here)
- comware_vxlan_tunnel: tunnel=20 global_src=10.10.10.10 src=10.1.1.1 dest=10.1.1.2 username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

# ensure tunnel interface 21
- comware_vxlan_tunnel: tunnel=21 src=10.1.1.1 dest=10.1.1.2 username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

# ensure tunnel interface 21 does not exist (does not have to be a vxlan tunnel)
- comware_vxlan_tunnel: tunnel=21 state=absent username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

"""

import socket
try:
    HAS_PYHP = True
    from pyhpecw7.features.vxlan import Tunnel
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
            tunnel=dict(required=True, type='str'),
            src=dict(required=False, type='str'),
            dest=dict(required=False, type='str'),
            global_src=dict(required=False, type='str'),
            state=dict(choices=['present', 'absent'], default='present'),
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

    tunnel = module.params['tunnel']
    src = module.params['src']
    dest = module.params['dest']
    global_src = module.params['global_src']

    state = module.params['state']

    changed = False

    args = dict(src=src, dest=dest)
    proposed = dict((k, v) for k, v in args.items() if v is not None)

    try:
        look_for_keys = module.params['look_for_keys']
        device.open(look_for_keys=look_for_keys)
    except ConnectionError as e:
        safe_fail(module, device, msg=str(e), descr='error opening device conn')

    try:
        l2vpn = L2VPN(device)
        is_l2vpn_enabled = l2vpn.get_config()
    except PYHPError as e:
        safe_fail(module, device, msg=str(e), descr='L2VPN check failed')

    if is_l2vpn_enabled == 'disabled':
        safe_fail(module, device, msg='l2vpn needs to be enabled.')

    try:
        tun = Tunnel(device, tunnel)
        existing = tun.get_config()
    except PYHPError as e:
        safe_fail(module, device, msg=str(e), descr='could not get tunnel config')

    if state == 'present':
        if existing.get('mode') and existing.get('mode') != 'vxlan':
            safe_fail(module, device, msg='tunnel interface exists but is not a '
                      + 'vxlan \ntunnel interface. remove and re-add.')

    delta = dict(set(proposed.items()).difference(
        existing.items()))

    try:
        existing_gsrc = tun.get_global_source()
    except PYHPError as e:
        safe_fail(module, device, msg=str(e),
                  descr='could not get existing global src')

    if global_src:
        if existing_gsrc != global_src:
            delta['global_src'] = global_src
    if state == 'present':
        if delta or not existing:
            tun.build(stage=True, **delta)
    elif state == 'absent':
        if existing:
            tun.remove(stage=True)

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
                end_state = tun.get_config()
            except PYHPError as e:
                safe_fail(module, device, msg=str(e),
                          descr='error during execution')
            end_state['global_src'] = tun.get_global_source()
            changed = True

    proposed['global_src'] = global_src
    existing['global_src'] = existing_gsrc

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
