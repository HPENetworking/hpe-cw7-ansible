#!/usr/bin/python

DOCUMENTATION = """
---

module: comware_vxlan
short_description: Manage VXLAN to VSI mappings and Tunnel mappings to VXLAN
description:
    - Manage VXLAN to VSI mappings and Tunnel mappings to VXLAN
version_added: 1.8
category: Feature (RW)
notes:
    - VXLAN tunnels should be created before using this module.
    - state=absent removes the vsi and associated vxlan mapping if they both
      exist.
    - Remember that is a 1 to 1 mapping between vxlan IDs and VSIs
options:
    vxlan:
        description:
            - VXLAN that will be mapped to the VSI
        required: true
        default: null
        choices: []
        aliases: []
    vsi:
        description:
            - Name of the VSI
        required: true
        default: null
        choices: []
        aliases: []
    descr:
        description:
            - description of the VSI
        required: true
        default: null
        choices: []
        aliases: []
    tunnels:
        description:
            - Desired Tunnel interface ID or a list of IDs.
              Any tunnel not in the list will be removed if it exists
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

# ensure VXLAN and VSI do not exist
- comware_vxlan: vxlan=100 vsi=VSI_VXLAN_100 tunnels=20 state=absent username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

# ensure VXLAN 100 exists and is mapped to VSI VSI_VXLAN_100 with only tunnel interface 20
- comware_vxlan: vxlan=100 vsi=VSI_VXLAN_100 tunnels=20 username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

# ensure 3 tunnels mapped to the vxlan
- comware_vxlan:
    vxlan: 100
    vsi: VSI_VXLAN_100
    tunnels: ['20', '21', '22']
    username: "{{ username }}"
    password: "{{ password }}"
    hostname: "{{ inventory_hostname }}"

"""

import socket
try:
    HAS_PYHP = True
    from pyhpecw7.features.vxlan import Vxlan, Tunnel
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


def normalize_to_list(data):
    if isinstance(data, str) or isinstance(data, unicode):
        return [data]
    elif isinstance(data, list):
        return data
    else:
        return []


def checks(existing, proposed, module):
    if existing.get('vsi') and proposed.get('vsi'):
        if proposed.get('vsi') != existing.get('vsi'):
            safe_fail(module, msg='vxlan already assigned to another vsi.'
                      + '\nremove it first.', vsi=existing.get('vsi'))


def main():
    module = AnsibleModule(
        argument_spec=dict(
            vxlan=dict(required=True, type='str'),
            vsi=dict(required=True, type='str'),
            tunnels=dict(required=False),
            descr=dict(required=False),
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

    vxlan = module.params['vxlan']
    vsi = module.params['vsi']
    descr = module.params['descr']
    tunnels = normalize_to_list(module.params['tunnels'])
    state = module.params['state']
    changed = False

    args = dict(vxlan=vxlan, vsi=vsi, descr=descr)
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
        VXLAN = Vxlan(device, vxlan, vsi)
        existing = VXLAN.get_config()
    except PYHPError as e:
        safe_fail(module, device, msg=str(e), descr='could not obtain existing')

    if state == 'present':
        checks(existing, proposed, module)

    if 'tunnels' in existing.keys():
        existing_tunnels = existing.pop('tunnels')
    else:
        existing_tunnels = []

    delta = dict(set(proposed.items()).difference(
        existing.items()))
    tunnels_to_add = list(set(tunnels).difference(existing_tunnels))
    tunnels_to_remove = list(set(existing_tunnels).difference(tunnels))
    if tunnels_to_add:
        delta['tunnels_to_add'] = tunnels_to_add
        for each in tunnels_to_add:
            tun = Tunnel(device, each)
            exists = tun.get_config()
            if not exists:
                safe_fail(module, device, msg='tunnel needs to exist first'
                          + ' before \nbefore adding it to a vxlan',
                          tunnel=each)
    if tunnels_to_remove:
        delta['tunnels_to_remove'] = tunnels_to_remove

    if state == 'present':
        if not existing.get('vxlan'):
            VXLAN.create(stage=True)
        if delta:
            VXLAN.build(stage=True, **delta)
    elif state == 'absent':
        if existing:
            # existing is based off the VXLAN ID
            # if it's not mapped to any VSI, it's not considered
            # existing although the VSI may exist
            if existing.get('vsi') != vsi:
                safe_fail(module, device, msg='vsi/vxlan mapping must exist'
                          + ' on switch to remove it', current_vsi=existing.get('vsi'))
            else:
                VXLAN.remove_vsi(stage=True)

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
                end_state = VXLAN.get_config()
            except PYHPError as e:
                safe_fail(module, device, msg=str(e),
                          descr='failed during execution')
            changed = True

    if tunnels:
        proposed.update(tunnels=tunnels)
    if existing_tunnels:
        existing.update(tunnels=existing_tunnels)

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
