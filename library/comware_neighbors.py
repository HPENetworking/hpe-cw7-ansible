#!/usr/bin/python

DOCUMENTATION = """
---

module: comware_neighbors
short_description: Retrieve active LLDP neighbors (read-only)
description:
    - Retrieve active LLDP neighbors (read-only)
version_added: 1.8
category: Read-Only
options:
    neigh_type:
        description:
            - type of neighbors
        required: false
        default: lldp
        choices: ['lldp', 'cdp']
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

EXAMPLES = '''

# get lldp neighbors
- comware_neighbors: username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

'''

import socket
try:
    HAS_PYHP = True
    from pyhpecw7.features.neighbor import Neighbors
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
            neigh_type=dict(default='lldp', choices=['cdp', 'lldp']),
            port=dict(default=830, type='int'),
            hostname=dict(required=True),
            username=dict(required=True),
            password=dict(required=False, default=None),
            look_for_keys=dict(default=False, type='bool'),
        ),
        supports_check_mode=False
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

    neigh_type = module.params['neigh_type']

    try:
        look_for_keys = module.params['look_for_keys']
        device.open(look_for_keys=look_for_keys)
    except ConnectionError as e:
        safe_fail(module, device, msg=str(e),
                  descr='error opening conn to device')

    try:
        neighbors = Neighbors(device)
    except PYHPError as e:
        safe_fail(module, device, msg=str(e),
                  descr='error getting neighbor info')

    response = getattr(neighbors, neigh_type)

    results = dict(neighbors=response)
    safe_exit(module, device, **results)

from ansible.module_utils.basic import *
main()
