#!/usr/bin/python

DOCUMENTATION = """
---

module: comware_vsi_intf
short_description: Configure some functions of vsi-interface
description:
    - Configure some functions of vsi-interface
version_added: 1.8
category: Feature (RW)
notes:
    - l2vpn needs to enbled before config vsi view.
    - vsi_intf must be vsi interface type , the module is only used for config vsi interface.
    - If you want to bind a interface with VPN instance, the VPN instance must be already exist.
options:
    vsi_intf:
        description:
            - The vsi interface view to config
        required: true
        default: null
        choices: []
        aliases: []
    binding:
        description:
            - Bind the interface with a VPN instance
        required: false
        default: null
        choices: []
        aliases: []
    macaddr:
        description:
            - config MAC address information
        required: false
        default: null
        choices: []
        aliases: []
    local_proxy:
        description:
            - Enable local proxy ARP or ND function
        required: false
        default: null
        choices: ['nd', 'arp']
        aliases: []
    distribute_gateway:
        description:
            - Specify the VSI interface as a distributed gateway
        required: false
        default: null
        choices: ['local']
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
     # - name:  config vsi
       # comware_vsi_intf: vsi_intf=Vsi-interface1 binding=vpna macaddr=201a-101a-40fa  local_proxy=arp \
       distribute_gateway=local username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

"""

import socket
try:
    HAS_PYHP = True
    from pyhpecw7.comware import HPCOM7
    from pyhpecw7.features.l2vpn import L2VPN
    from pyhpecw7.features.interface import Interface
    from pyhpecw7.utils.validate import valid_ip_network
    from pyhpecw7.features.vsi_intf import Vsi
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

def ip_stringify(**kwargs):
    return kwargs.get('gateway_subnet') + '/' + kwargs.get('gateway_mask')

def checks(existing, proposed, module):
    if existing.get('vsi') and proposed.get('vsi'):
        if proposed.get('vsi') != existing.get('vsi'):
            safe_fail(module, msg='vxlan already assigned to another vsi.'
                      + '\nremove it first.', vsi=existing.get('vsi'))


def main():
    module = AnsibleModule(
        argument_spec=dict(
            vsi_intf=dict(required=True, type='str'),
            binding=dict(type='str'),
            macaddr=dict(type='str'),
            local_proxy=dict(choices=['nd', 'arp']),
            distribute_gateway=dict(choices=['local']),
            state=dict(choices=['present', 'default'], default='present'),
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

    filtered_keys = ('state', 'hostname', 'username', 'password',
                     'port', 'CHECKMODE', 'name', 'look_for_keys')

    username = module.params['username']
    password = module.params['password']
    port = module.params['port']
    hostname = socket.gethostbyname(module.params['hostname'])
    device_args = dict(host=hostname, username=username,
                       password=password, port=port)
    state = module.params['state']
    vsi_intf = module.params['vsi_intf']
    binding = module.params['binding']

    device = HPCOM7(**device_args)
    changed = False

    proposed = dict((k, v) for k, v in module.params.items()
                    if v is not None and k not in filtered_keys)

    try:
        look_for_keys = module.params['look_for_keys']
        device.open(look_for_keys=look_for_keys)
    except ConnectionError as e:
        safe_fail(module, device, msg=str(e), descr='error opening device conn')

    try:
        vsi_interface = Interface(device,vsi_intf)
    except PYHPError as e:
        safe_fail(module, device, msg=str(e), descr='could not obtain existing')

    if vsi_interface._iface_type(vsi_intf)[1] != 'Vsi-interface':
        safe_fail(module,msg='This module is used for config vsi interface '+
                             ', Other port types can be processed using the interface module')

    try:
        l2vpn = L2VPN(device)
        is_l2vpn_enabled = l2vpn.get_config()
    except PYHPError as e:
        safe_fail(module, device, msg=str(e), descr='L2VPN check failed')

    if is_l2vpn_enabled == 'disabled':
        safe_fail(module, device, msg='l2vpn needs to be enabled.')

    try:
        interface = Vsi(device, vsi_intf)
        existing = interface.get_config()
    except PYHPError as e:
        safe_fail(module, device, msg=str(e), descr='could not obtain existing')

    if binding not in interface.get_vpn_config():
        safe_fail(module,msg='The vpn-intance you provided does not exist, please create it first')

    try:
        interface.param_check(**proposed)
    except PYHPError as e:
        safe_fail(module,device,
                  descr='There was problem with the supplied parameters.',
                  msg=str(e))

    if state == 'present':
        delta = proposed
        if delta:
            interface.build(stage=True,**delta)

    elif state == 'default':
        delta = dict(vsi=vsi)
        if delta:
            interface.remove(stage=True,**delta)

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
                end_state = interface.get_config()
            except PYHPError as e:
                safe_fail(module, device, msg=str(e),
                          descr='failed during execution')
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
