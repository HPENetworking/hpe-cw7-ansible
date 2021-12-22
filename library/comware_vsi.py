#!/usr/bin/python

DOCUMENTATION = """
---

module: comware_vsi
short_description: Configure some command functions of vsi view
description:
    - Configure some command functions of vsi view
version_added: 1.8
category: Feature (RW)
notes:
    - l2vpn needs to enbled before config vsi view.
    - If you want to use vsi gateway interface, it must be exist , you can use interface module to create it.
    - when giving vsi and state is default , it will delete the given vsi config all.
options:
    vsi:
        description:
            - Name of the VSI
        required: true
        default: null
        choices: []
        aliases: []
    gateway_intf:
        description:
            - vsi view Gateway configuration interface 
        required: false
        default: null
        choices: []
        aliases: []
    gateway_subnet:
        description:
            - vsi view Gateway configuration subnet 
        required: false
        default: null
        choices: []
        aliases: []
    gateway_mask:
        description:
            - vsi view Gateway configuration subnet wild card mask
        required: false
        default: null
        choices: []
        aliases: []
    vxlan:
        description:
            - Specify a Virtual eXtensible LAN
        required: false
        default: null
        choices: []
        aliases: []
    encap:
        description:
            - Ethernet virtual private network module 
        required: false
        default: null
        choices: ['true', 'false']
        aliases: []
    rd:
        description:
            - Configure a route distinguisher
        required: false
        default: null
        choices: []
        aliases: []
    vpn_target_auto:
        description:
            - Configure route targets
        required: false
        default: null
        choices: ['both', 'export','import']
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
       # comware_vsi: vsi=vpna gateway_intf=Vsi-interface1 gateway_subnet=10.1.1.0 gateway_mask=0.0.0.255 vxlan=10 \
       encap=true rd=auto vpn_target_auto=both username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
       
     # - name:  delelte vsi configs
       # comware_vsi: vsi=vpna state=default username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

"""

import socket
try:
    HAS_PYHP = True
    from pyhpecw7.comware import HPCOM7
    from pyhpecw7.features.l2vpn import L2VPN
    from pyhpecw7.features.interface import Interface
    from pyhpecw7.utils.validate import valid_ip_network
    from pyhpecw7.features.vsi import Vsi
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
            vsi=dict(required=True, type='str'),
            gateway_intf=dict(type='str'),
            gateway_subnet=dict(type='str'),
            gateway_mask=dict(type='str'),
            vxlan=dict(type='str'),
            encap=dict(choices=['true', 'false']),
            rd=dict(type='str'),
            vpn_target_auto=dict(choices=['both', 'export','import']),
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
    vsi = module.params['vsi']
    gateway_intf = module.params['gateway_intf']
    gateway_subnet = module.params['gateway_subnet']
    gateway_mask = module.params['gateway_mask']
    encap = module.params['encap']
    rd = module.params['rd']
    vpn_target_auto = module.params['vpn_target_auto']

    device = HPCOM7(**device_args)
    changed = False

    proposed = dict((k, v) for k, v in module.params.items()
                    if v is not None and k not in filtered_keys)

    if state == 'present':
        if gateway_mask and gateway_subnet:
            if not valid_ip_network(ip_stringify(**module.params)):
                module.fail_json(msg='Not a valid IP address or mask.')

        if gateway_mask and not gateway_subnet:
            safe_fail(module,msg='gateway_subnet and gateway_mask need to exist together')

        if gateway_subnet and not gateway_mask:
            safe_fail(module,msg='gateway_subnet and gateway_mask need to exist together')

        if encap != 'true':
            if rd or vpn_target_auto:
                safe_fail(module,msg='RD and vpn target realized in evpn encapsulation vxlan view')

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

    if gateway_intf:
        try:
            interface = Interface(device,gateway_intf)
        except PYHPError as e:
            safe_fail(module,msg='Error occurred while checking interface {0}'.format(gateway_intf))

        if not interface.iface_exists:
            safe_fail(module,msg='The interface {0} is not exist'.format(gateway_intf))

    try:
        VSI = Vsi(device, vsi)
        existing = VSI.get_config()
    except PYHPError as e:
        safe_fail(module, device, msg=str(e), descr='could not obtain existing')

    try:
        VSI.param_check(**proposed)
    except PYHPError as e:
        safe_fail(module,device,
                  descr='There was problem with the supplied parameters.',
                  msg=str(e))

    if state == 'present':
        delta = proposed
        if delta:
            VSI.build(stage=True,**delta)

    elif state == 'default':
        delta = dict(vsi=vsi)
        if delta:
            VSI.remove(stage=True,**delta)

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
                end_state = VSI.get_config()
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
