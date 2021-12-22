#!/usr/bin/python

DOCUMENTATION = """
---

module: comware_netstream
short_description: Manage ip netstream,rate,timeout, max_entry,vxlan udp-port,and interface enable and ip netstream aggregation destination-prefix enable, 
                   netstream statistics output message destination address and destination UDP port number configurationon 
                   Comware 7 devices
version_added: 1.0
category: Feature (RW)
notes:
    - Before configuring netstream stream image, you need to enable the global netstream function.
    - The default state is not open global netstream function.If you want to config interface netstream enable,the name parameter
      must be exit.If you config netstream statistics output message,host and udp paramaters must be exit.
options:
    netstream:
        description:
            -  global netstream enable or disable
        required: true
        default: null
        choices: [enable, disabled]
        aliases: []
    rate:
        description:
            -  Configure output rate limit
        required: false
        default: null
        choices: []
        aliases: []     
    timeout:
        description:
            -  Active aging time of configuration flow
        required: false
        default: null
        choices: [max-entries, aging, disable-caching]
        aliases: []   
    max_enter:
        description:
            -  Active aging time of configuration flow
        required: false
        default: null
        choices: []
        aliases: []
    vxlan_udp:
        description:
            -  Enable vxlan message statistics function
        required: false
        default: null
        choices: []
        aliases: []    
    sampler:
        description:
            - Create a sampler.
        required: false
        default: null
        choices: []
        aliases: []
    mode:
        description:
            - Sampler mode.if config sampler,this parameter is must be exit.
        required: false
        default: null
        choices: ['fixed', 'random']
        aliases: []
    sampler_rate:
        description:
            - Sampler rate. if config sampler,this parameter is must be exit.
        required: false
        default: null
        choices: []
        aliases: []
    version:
        description:
            - Configure autonomous system options for netstream version.
        required: false
        default: 9
        choices: ['5','9','10']
        aliases: []
    BGP:
        description:
            - BGP next hop option.
        required: false
        default: null
        choices: ['origin-as','peer-as','bgp-nexthop']
        aliases: []
    inactive:
        description: 
            - Configure Inactive aging time of flow.(10~600).
        required: false
        default: null
        choices: []
        aliases: []
    source_intf:
        description: 
            - Configure the source interface of netstream statistical output message.
        required: false
        default: null
        choices: []
        aliases: []
    aggregation:
        description:
            - Enter netstream aggregation view and enable it
        required: false
        default: null
        choices: ['as','destination-prefix','prefix','prefix-port','protocol-port','source-prefix','tos-as','tos-bgp-nexthop','tos-destination-prefix','tos-prefix','tos-protocol-port','tos-source-prefix']
        aliases: []
    name:
        description:
            - Full name of the interface
        required: false
        default: null
        choices: []
        aliases: []
    interface_enable:
        description:
            - manage interface netstream enable.To config this, name parameter must be exit.
        required: false
        default: null
        choices: ['inbound', 'outbound']
        aliases: []
    interface_sampler:
        description:
            - manage interface sampler.
        required: false
        default: null
        choices: []
        aliases: []
    host:
        description:
            - Configure the destination address of netstream statistical output message.
        required: false
        default: null
        choices: []
        aliases: []
    udp:
        description:
            - Configure the destination UDP port number of netstream statistical output message.
        required: false
        default: null
        choices: []
        aliases: []
    vpn_name:
        description:
            - Specify the VPN to which the destination address of netstream statistical output message belongs.
        required: false
        default: null
        choices: []
        aliases: []
    state:
        description:
            - Desired state for the interface configuration.
        required: false
        default: present
        choices: ['present', 'absent']
        aliases: []
    port:
        description:
            - NETCONF port number
        required: false
        default: 830
        choices: []
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
    look_for_keys:
        description:
            - Whether searching for discoverable private key files in ~/.ssh/
        required: false
        default: False
        choices: []
        aliases: []

"""

EXAMPLES = """

# netstream config
  - comware_netstream: netstream=enable rate=10 timeout=1 max_entry=2 vxlan_udp=8000 aggregation=prefix host=192.168.1.43 udp=29 state=present username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
# delete netstream config
  - comware_netstream: netstream=enable rate=10 timeout=1 max_entry=2 vxlan_udp=8000 aggregation=prefix host=192.168.1.43 udp=29 state=absent username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

"""

import socket
try:
    HAS_PYHP = True
    from pyhpecw7.features.netstream import Netstream
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
            netstream=dict(required=False,choices=['enable', 'disabled']),
            rate=dict(required=False),
            timeout=dict(required=False),
            max_entry=dict(required=False),
            vxlan_udp=dict(required=False),
            sampler=dict(required=False),
            mode=dict(required=False, choice=['fixed', 'random']),
            sampler_rate=dict(required=False),
            aggregation=dict(required=False, choice=['as','destination-prefix','prefix','prefix-port','protocol-port','source-prefix','tos-as','tos-bgp-nexthop','tos-destination-prefix','tos-prefix','tos-protocol-port','tos-source-prefix']),
            version=dict(required=False, choice=['5','9','10'], default='9'),
            BGP=dict(required=False, choice=['origin-as','peer-as','bgp-nexthop']),
            inactive=dict(required=False),
            source_intf=dict(required=False),
            name=dict(required=False),
            interface_enable=dict(required=False, choices=['inbound', 'outbound']),
            interface_sampler=dict(required=False),
            host=dict(required=False),
            udp=dict(required=False),
            vpn_name=dict(required=False),
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
    netstream = module.params['netstream']
    interface_sampler = module.params['interface_sampler']
    sampler = module.params['sampler']
    mode = module.params['mode']
    sampler_rate = module.params['sampler_rate']
    rate = module.params['rate']
    timeout = module.params['timeout']
    max_entry = module.params['max_entry']
    vxlan_udp = module.params['vxlan_udp']
    aggregation = module.params['aggregation']
    version = module.params['version']
    BGP = module.params['BGP']
    inactive = module.params['inactive']
    source_intf = module.params['source_intf']
    name = module.params['name']
    interface_enable = module.params['interface_enable']
    host = module.params['host']
    udp = module.params['udp']
    vpn_name = module.params['vpn_name']
    state = module.params['state']
    args = dict(netstream=netstream, rate=rate, timeout=timeout, max_entry=max_entry, vxlan_udp=vxlan_udp, sampler=sampler, mode=mode, sampler_rate=sampler_rate, interface_sampler=interface_sampler, aggregation=aggregation, version=version, BGP=BGP, inactive=inactive, source_intf=source_intf, name=name, interface_enable=interface_enable, host=host, udp=udp, vpn_name=vpn_name)
    proposed = dict((k, v) for k, v in args.items() if v is not None)

    changed = False

    try:
        look_for_keys = module.params['look_for_keys']
        device.open(look_for_keys=look_for_keys)
    except ConnectionError as e:
        safe_fail(module, device, msg=str(e),
                  descr='error connecting to device')

    try:
        netStream = Netstream(device, netstream, rate, timeout, max_entry, vxlan_udp, sampler, mode, sampler_rate, interface_sampler, aggregation, version, BGP, inactive, source_intf, name, interface_enable, host, udp, vpn_name)
    except PYHPError as e:
        safe_fail(module, device, msg=str(e))

    if state == 'present':
        netStream.build(stage=True)
    elif state == 'absent':
        netStream.remove(stage=True)

    commands = None

    if device.staged:
        commands = device.staged_to_string()
        if module.check_mode:
            safe_exit(module, device, changed=True,
                      commands=commands)
        else:
            try:
                device.execute_staged()
            except PYHPError as e:
                safe_fail(module, device, msg=str(e),
                          descr='error during execution')
            changed = True

    results = {}

    results['state'] = state
    results['commands'] = commands
    results['changed'] = changed
    results['proposed'] = proposed

    safe_exit(module, device, **results)

from ansible.module_utils.basic import *
main()
