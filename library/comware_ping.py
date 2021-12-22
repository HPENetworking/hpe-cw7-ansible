#!/usr/bin/python

DOCUMENTATION = """
---

module: comware_ping
short_description: Ping remote destinations *from* the Comware 7 switch
description:
    - Ping remote destinations *from* the Comware 7 device.  Really helpful
      for reachability testing.
version_added: 1.8
category: Read-Only
options:
    host:
        description:
            - IP or name (resolvable by the switch) that you want to ping
        required: true
        default: null
        choices: []
        aliases: []
    vrf:
        description:
            - VRF instance pings should be sourced from
        required: false
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

# test reachability to 8.8.8.8
- comware_ping: host=8.8.8.8 username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

"""

import socket
try:
    HAS_PYHP = True
    from pyhpecw7.features.ping import Ping
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
            host=dict(required=True, type='str'),
            vrf=dict(required=False, type='str'),
            v6=dict(default=False, choices=BOOLEANS, type='bool'),
            port=dict(default=830, type='int'),
            hostname=dict(required=True),
            username=dict(required=True),
            password=dict(required=False, default=None),
            look_for_keys=dict(default=False, type='bool'),
        ),
        supports_check_mode=False
    )

    if not HAS_PYHP:
        safe_fail(module, msg='There was a problem loading from the pyhpecw7 '
                  + 'module.', error=str(ie))

    username = module.params['username']
    password = module.params['password']
    port = module.params['port']
    hostname = socket.gethostbyname(module.params['hostname'])

    device_args = dict(host=hostname, username=username,
                       password=password, port=port)

    device = HPCOM7(**device_args)

    host = module.params['host']
    vrf = module.params['vrf']
    v6 = module.params['v6']

    try:
        look_for_keys = module.params['look_for_keys']
        device.open(look_for_keys=look_for_keys)
    except ConnectionError as e:
        safe_fail(module, device, msg=str(e),
                  descr='error connecting to device')

    try:
        ping = Ping(device, host, vrf=vrf, v6=v6)
    except InvalidIPAddress as iie:
        safe_fail(module, device, msg=str(iie))
    except PYHPError as e:
        safe_fail(module, device, msg=str(e))

    response = ping.response

    results = dict(response=response)
    safe_exit(module, device, **results)

from ansible.module_utils.basic import *
main()
