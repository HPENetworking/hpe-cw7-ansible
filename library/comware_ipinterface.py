#!/usr/bin/python

DOCUMENTATION = """
---
module: comware_ipinterface
short_description: Manage IPv4/IPv6 addresses on interfaces
description:
    - Manage IPv4/IPv6 addresses on interfaces
version_added: 1.8
category: Feature (RW)
notes:
    - If the interface is not configured to be a layer 3 port,
      the module will fail and the user should use the interface
      module to convert the interface with type=routed
    - If state=absent, the specified IP address will be removed from the interface.
      If the existing IP address doesn't match the specified,
      the existing will not be removed.
options:
    name:
        description:
            - Full name of the interface
        required: true
        default: null
        choices: []
        aliases: []
    addr:
        description:
            - The IPv4 or IPv6 address of the interface
        required: true
        default: null
        choices: []
        aliases: []
    mask:
        description:
            - The network mask, in dotted decimal or prefix length notation.
              If using IPv6, only prefix length is supported.
        required: true
        default: null
        choices: []
        aliases: []
    version:
        description:
            - v4 for IPv4, v6 for IPv6
        required: false
        default: v4
        choices: [v4, v6]
        aliases: []
    state:
        description:
            - Desired state of the switchport
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

# Basic IPv4 config
- comware_ipinterface: name=FortyGigE1/0/3 addr=192.168.3.5 mask=255.255.255.0 username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

# Basic IPv6 config
- comware_ipinterface: version=v6 name=FortyGigE1/0/3 addr=2001:DB8::1 mask=10 username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

"""

import socket

try:
    HAS_PYHP = True
    from pyhpecw7.comware import HPCOM7
    from pyhpecw7.features.ipinterface import IpInterface
    from pyhpecw7.utils.validate import valid_ip_network
    from pyhpecw7.utils.network import ipaddr
    from pyhpecw7.errors import *
except ImportError as ie:
    HAS_PYHP = False


def compare_ips(net1, net2):
    x = ipaddr.IPNetwork(net1)
    y = ipaddr.IPNetwork(net2)
    return x.ip == y.ip\
        and x.prefixlen == y.prefixlen


def ip_stringify(**kwargs):
    return kwargs.get('addr') + '/' + kwargs.get('mask')


def get_existing(ip_int, addr, mask):
    existing_list = ip_int.get_config()

    for each in existing_list:
        if each:
            if compare_ips(
                    ip_stringify(**each), ip_stringify(addr=addr, mask=mask)):
                return each

    return {}


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
            name=dict(required=True),
            addr=dict(required=True),
            mask=dict(required=True, type='str'),
            version=dict(choices=['v4', 'v6'],
                         default='v4'),
            state=dict(choices=['present', 'absent'],
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
        module.fail_json(
            msg='There was a problem loading from the pyhpecw7 module')

    filtered_keys = ('state', 'hostname', 'username', 'password',
                     'port', 'CHECKMODE', 'name', 'version', 'look_for_keys')

    hostname = socket.gethostbyname(module.params['hostname'])
    username = module.params['username']
    password = module.params['password']
    port = module.params['port']

    device = HPCOM7(host=hostname, username=username,
                    password=password, port=port)

    name = module.params['name']
    state = module.params['state']
    version = module.params['version']
    addr = module.params['addr']
    mask = module.params['mask']
    changed = False

    if not valid_ip_network(ip_stringify(**module.params)):
        module.fail_json(msg='Not a valid IP address or mask.')

    try:
        look_for_keys = module.params['look_for_keys']
        device.open(look_for_keys=look_for_keys)
    except ConnectionError as e:
        safe_fail(module, device,
                  descr='There was an error opening'
                  + ' the connection to the device.',
                  msg=str(e))

    try:
        ip_int = IpInterface(device, name, version)
    except PYHPError as e:
        safe_fail(module, device,
                  descr='There was an error initializing'
                  + ' the IpInterface class.',
                  msg=str(e))

    if not ip_int.interface.iface_exists:
        safe_fail(module, device, msg='Please use the interface module ' +
                  'to create the {0} interface.'.format(ip_int.interface_name))

    # Make sure interface is routed
    if not ip_int.is_routed:
        safe_fail(module, device, msg='Please use the interface module ' +
                  'to make {0} a routed interface.'.format(ip_int.interface_name))

    try:
        existing = get_existing(ip_int, addr, mask)
    except PYHPError as e:
        safe_fail(module,
                  device,
                  descr='Error getting the existing configuration.',
                  msg=str(e))

    proposed = dict((k, v) for k, v in module.params.items()
                    if v is not None and k not in filtered_keys)

    if existing:
        ips_are_same = compare_ips(
            ip_stringify(**existing), ip_stringify(**proposed))
    else:
        ips_are_same = False

    if state == 'present':
        if not ips_are_same:
            ip_int.build(stage=True, **proposed)
    elif state == 'absent':
        if ips_are_same:
            ip_int.remove(stage=True, **existing)

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
                end_state = get_existing(ip_int, addr, mask)
            except PYHPError as e:
                safe_fail(module,
                          device,
                          descr='Error during command execution.',
                          msg=str(e))
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
