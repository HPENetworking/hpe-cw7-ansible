#!/usr/bin/python

DOCUMENTATION = """
---

module: comware_vxlan_vsi
short_description: Manage mapping of an Ethernet Service to a VSI (VXLAN ID)
description:
  - Manage the mapping of an Ethernet Service to a VSI (VXLAN ID)
version_added: 1.8
category: Feature (RW)
notes:
  - VSI needs to be created before using this module (comware_vxlan)
  - encap and xconnect access_mode cannot be altered once set
    to change, use state=absent and re-configure
  - state=absent removes the service instance for specified interface if
    if it exists
  - This should be the last VXLAN module used after comware_vxlan_tunnel,
    and comware_vxlan.
options:
    vsi:
        description:
            - Name of the VSI
        required: false
        default: null
        choices: []
        aliases: []
    interface:
        description:
            - Layer 2 interface or bridged-interface
        required: true
        default: null
        choices: []
        aliases: []
    instance:
        description:
            - Service instance id
        required: true
        default: null
        choices: []
        aliases: []
    encap:
        description:
            - only-tagged also ensures s-vid
        required: false
        default: default
        choices: ['default', 'tagged', 'untagged', 'only-tagged', 's-vid']
        aliases: []
    vlanid:
        description:
            - If encap is set to only-tagged or s-vid, vlanid must be set.
        required: false
        default: null
        choices: []
        aliases: []
    access_mode:
        description:
            - Mapping Ethernet service instance to a VSI using Ethernet
              or VLAN mode (options for xconnect command)
        required: false
        default: vlan
        choices: ['ethernet', 'vlan']
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

# ensure the vsi is not mapped to the instance
- comware_vxlan_svc_instance: interface=Fo1/0/32 vsi=VSI_VXLAN_100 instance=100 state=absent username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

# ensure instance and vsi and configured with encap and access mode as specified
- comware_vxlan_svc_instance: interface=Fo1/0/32 vsi=VSI_VXLAN_100 instance=100 encap=default access_mode=vlan username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

# ensure instance and vsi and configured with encap and access mode as specified
- comware_vxlan_svc_instance: interface=Fo1/0/32 vsi=VSI_VXLAN_100 instance=100 encap=tagged access_mode=ethernet username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

# ensure instance and vsi and configured with encap and access mode as specified
- comware_vxlan_svc_instance: interface=Fo1/0/32 vsi=VSI_VXLAN_100 instance=100 encap=only-tagged vlanid=10 state=present username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

"""

import socket
try:
    HAS_PYHP = True
    from pyhpecw7.features.vxlan import L2EthService
    from pyhpecw7.features.l2vpn import L2VPN
    from pyhpecw7.features.interface import Interface
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


def checks(existing, proposed, module):
    if existing.get('encap') and proposed.get('encap'):
        if proposed.get('encap') != existing.get('encap'):
            module.fail_json(msg='cannot alter encap once set. remove '
                             + '\ninstance and re-add')
    if existing.get('access_mode') and proposed.get('access_mode'):
        if proposed.get('access_mode') != existing.get('access_mode'):
            module.fail_json(msg='cannot alter mode once set. remove '
                             + '\ninstance and re-add')


def main():
    module = AnsibleModule(
        argument_spec=dict(
            vsi=dict(required=True, type='str'),
            interface=dict(required=True, type='str'),
            instance=dict(required=True, type='str'),
            encap=dict(required=False, choices=['default', 'tagged',
                                                'untagged', 'only-tagged',
                                                's-vid'], default='default'),
            vlanid=dict(required=False, type='str'),
            access_mode=dict(required=False, choices=['ethernet', 'vlan'],
                             default='vlan'),
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

    vsi = module.params['vsi']
    interface = module.params['interface']
    instance = module.params['instance']
    encap = module.params['encap']
    vlanid = module.params['vlanid']
    access_mode = module.params['access_mode']

    state = module.params['state']

    if encap in ['only-tagged', 's-vid']:
        if not vlanid:
            safe_fail(module, device,
                      msg='vlanid must be set when using only-tagged'
                      + 'and s-vid as the encap')

    changed = False

    args = dict(encap=encap, vlanid=vlanid, access_mode=access_mode)
    proposed = dict((k, v) for k, v in args.items() if v is not None)

    try:
        look_for_keys = module.params['look_for_keys']
        device.open(look_for_keys=look_for_keys)
    except ConnectionError as e:
        safe_fail(module, device, msg=str(e),
                  descr='error opening device conn')

    try:
        l2vpn = L2VPN(device)
        is_l2vpn_enabled = l2vpn.get_config()
    except PYHPError as e:
        safe_fail(module, device, msg=str(e),
                  descr='L2VPN config check failed')

    if is_l2vpn_enabled == 'disabled':
        safe_fail(module, device, msg='l2vpn needs to be enabled.')

    try:
        intf = Interface(device, interface)
    except PYHPError as e:
        safe_fail(module, device, msg=str(e),
                  descr='could not instantiate interface')

    if intf.is_routed:
        safe_fail(module, device, msg='interface needs to be an L2 interface')

    try:
        eth = L2EthService(device, interface, instance, vsi)
    except PYHPError as e:
        safe_fail(module, device, msg=str(e),
                  descr='L2EthService failure')

    if not eth.vsi_exist():
        safe_fail(module, device, msg='VSI needs to be created before using'
                  + ' this module')
    try:
        existing = eth.get_config()
    except PYHPError as e:
        safe_fail(module, device, msg=str(e),
                  descr='error getting L2EthService config')

    # existing = {} when service instance doesn't exist on interface
    # keys: interface, instance, and index exist when an instance is
    # configured.  pretty much means, there won't be a delta at that point
    # keys: encap and optionally svid/cvid are added based when encap
    # command is issued on box

    # keys: vsi added when xconnect command exists on interface for
    # this instance

    delta = dict(set(proposed.items()).difference(
        existing.items()))

    if state == 'present':
        if existing:
            checks(existing, proposed, module)

        if delta or not existing:
            eth.build(stage=True, **delta)
    elif state == 'absent':
        if existing:
            eth.remove(stage=True)

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
                end_state = eth.get_config()
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
