#!/usr/bin/python

DOCUMENTATION = """
---

module: comware_teleFlowGroup_global
short_description: Manage telemetry flow group agingtime on Comware 7 devices.The default value is Varies by device.
version_added: 1.0
author: gongqianyu
category: Feature (RW)
options:
    agtime:
        description:
            - elemetry flow group agingtime
        required: true
        default: null
        choices: []
        aliases: []
    state:
        description:
            - Desired state for the interface configuration
        required: false
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

  # telemetry Flow Group aging time config
  - comware_teteFlowGroup_global:
      agtime:20
      username: "{{ username }}"
      password: "{{ password }}"
      hostname: "{{ inventory_hostname }}"

 # config aging time into default state      
- comware_teteFlowGroup_global:
      agtime:20
      username: "{{ username }}"
      password: "{{ password }}"
      hostname: "{{ inventory_hostname }}"
      state: default

"""

import socket
try:
    HAS_PYHP = True
    from pyhpecw7.features.teleFlowGroup_global import Flowglobal
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
                agtime=dict(required=True, type='str'),
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

    username = module.params['username']
    password = module.params['password']
    port = module.params['port']
    hostname = socket.gethostbyname(module.params['hostname'])

    device_args = dict(host=hostname, username=username,
                       password=password, port=port)

    device = HPCOM7(**device_args)

    agtime = module.params['agtime']
    state = module.params['state']

    changed = False

    args = dict(agtime=agtime)
    proposed = dict((k, v) for k, v in args.items() if v is not None)

    try:
        look_for_keys = module.params['look_for_keys']
        device.open(look_for_keys=look_for_keys)
    except ConnectionError as e:
        safe_fail(module, device, msg=str(e),
                  descr='error connecting to device')

    try:
        FLOWGLOBAL = Flowglobal(device, module,agtime, state)
        FLOWGLOBAL.param_check(**proposed)
    except PYHPError as e:
        safe_fail(module, device, msg=str(e))

    try:
        existing = FLOWGLOBAL.get_config()
    except PYHPError as e:
        safe_fail(module, device, msg=str(e),
                  descr='error getting priority config')
    try:

        FlowGlobal = Flowglobal(device,module=module)
    except PYHPError as e:
        safe_fail(module, device, msg=str(e),
                  descr='Error initialzing Switchport object.')

    if state == 'present':
        delta = dict(set(proposed.items()).difference(
            existing.items()))
        if delta:
            FlowGlobal.build(state=state, stage=True, **delta)

    elif state == 'default':
            FlowGlobal.default(state=state, stage=True)

    commands = None
    end_state = existing

#if device state changed, ansible will be display result with 'changed', no change it will be ok.
    if device.staged:
        commands = device.staged_to_string()
        if module.check_mode:
            device.close()
            safe_exit(module, device, changed=True,
                      commands=commands)
        else:
            try:
                device.execute_staged()
                end_state = FlowGlobal.get_config()
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













