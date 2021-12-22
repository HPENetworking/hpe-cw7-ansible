#!/usr/bin/python

DOCUMENTATION = """
---

module: comware_lldp
short_description: Manage lacp fast-Interval, tx-interval,hold-multplier on Comware 7 devices
author: gongqianyu
description:
    - the default fast Interval is 1 and tx-interval is 30,hold-multplier is 4.Using this module ,you must be use comware_lldp_global to enable global
     
version_added: 1.0
category: Feature (RW)
options:
    fast_intervalId:
        description:
            - lldp fast Interval
        required: false
        default: null
        choices: []
        aliases: []
    tx_intervalId:
        description:
            - lldp fast Interval
        required: false
        default: null
        choices: []
        aliases: []
    multiplierlId:
        description:
            - lldp hold-muliplierlid
        required: false
        default: null
        choices: []
        aliases: []
    state:
        description:
            - Desired state for the interface configuration
        required: true
        default: present
        choices: ['present', 'default']
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

  # lldp config
  - comware_lldp:
      fast_intervalId:8
      tx_intervalId:4
      multiplierId:8
      username: "{{ username }}"
      password: "{{ password }}"
      hostname: "{{ inventory_hostname }}"
      state: present
	  
# config fast-Interval and tx-interval into default state
  - comware_lldp:
      fast_intervalId:5
      tx_intervalId:4
      username: "{{ username }}"
      password: "{{ password }}"
      hostname: "{{ inventory_hostname }}"
      state: default
"""

import socket
try:
    HAS_PYHP = True
    from pyhpecw7.features.lldp import Lldp
    from pyhpecw7.comware import HPCOM7
    from pyhpecw7.features.errors import *
    from pyhpecw7.errors import PYHPError
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
                fast_intervalId=dict(required=False, type='str'),
                tx_intervalId=dict(required=False, type='str'),
                multiplierId=dict(required=False, type='str'),
                state=dict(choices=['present', 'default'], default=None),
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

    fast_intervalId = module.params['fast_intervalId']
    tx_intervalId = module.params['tx_intervalId']
    multiplierId = module.params['multiplierId']
    state = module.params['state']

    changed = False

    args = dict(fast_intervalId=fast_intervalId, tx_intervalId=tx_intervalId, multiplierId=multiplierId)
    proposed = dict((k, v) for k, v in args.items() if v is not None)

    try:
        look_for_keys = module.params['look_for_keys']
        device.open(look_for_keys=look_for_keys)
    except ConnectionError as e:
        safe_fail(module, device, msg=str(e),
                  descr='error connecting to device')

    try:
        LLDP = Lldp(device,module,fast_intervalId, tx_intervalId, multiplierId, state)
        LLDP.param_check(**proposed)
    except PYHPError as e:
        safe_fail(module, device, msg=str(e))

    try:
        existing = LLDP.get_config()
    except PYHPError as e:
        safe_fail(module, device, msg=str(e),
                  descr='error getting priority config')
    try:

        LLdp = Lldp(device,module=module)
    except PYHPError as e:
        safe_fail(module, device, msg=str(e),
                  descr='Error initialzing Switchport object.')


    if state == 'present':
        delta = dict(set(proposed.items()).difference(
            existing.items()))
        if delta:
            LLdp.build(state=state, stage=True, **delta)

    elif state == 'default':
            LLdp.default(state=state, stage=True)

    commands = None
    end_state = existing

    try:

        device.execute_staged()
        end_state = LLdp.get_config()

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













