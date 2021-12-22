#!/usr/bin/python

DOCUMENTATION = """
---

module: comware_bfd
short_description: Management configuration bfd function
description:
    - Manage bfd config
version_added: 1.8
category: Feature (RW)
author:null
notes:
    - This module is currently only used to enable BFD session flapping suppression , 
      other functions depend on other protocols and are not yet available.
    - Bfd dampening maximum delay and initial delay are required , also the second interval.
    - The initial interval and second interval must be shorter than the maximum interval.
    - Maximum , initial and second interval are required in 1-3600 seconds. 
    
options:
    damp_max_wait_time:
        description:
            - Configure the maximum dampening timer interval
        required: false
        default: null
        choices: []
        aliases: []
    damp_init_wait_time:
        description:
            - Configure the initial dampening timer interval
        required: false
        default: null
        choices: []
        aliases: []
    secondary:
        description:
            - Configure the second dampening timer interval
        required: false
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
            - The Comware port used to connect to the switch
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
EXAMPLE = """
     - name:  config bfd 
       comware_bfd: damp_max_wait_time=100 damp_init_wait_time=10 secondary=8 \
       username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
     - name:  delete bfd related
       comware_bfd: damp_max_wait_time=100 damp_init_wait_time=10 secondary=8 state=default \
       username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
"""

import socket

try:
    HAS_PYHP = True
    from pyhpecw7.comware import HPCOM7
    from pyhpecw7.features.bfd import Bfd
    from pyhpecw7.features.errors import InterfaceError
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
            damp_max_wait_time=dict(type='str'),
            damp_init_wait_time=dict(type='str'),
            secondary=dict(type='str'),
            state=dict(choices=['present', 'default'],
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
        safe_fail(module, msg='There was a problem loading from the pyhpecw7 '
                  + 'module.', error=str(ie))

    filtered_keys = ('state', 'hostname', 'username', 'password',
                     'port', 'CHECKMODE', 'name', 'look_for_keys')

    hostname = socket.gethostbyname(module.params['hostname'])
    username = module.params['username']
    password = module.params['password']
    port = module.params['port']
    device = HPCOM7(host=hostname, username=username,
                    password=password, port=port)
    state = module.params['state']
    damp_max_wait_time = module.params['damp_max_wait_time']
    changed = False
    proposed = dict((k, v) for k, v in module.params.items()
                    if v is not None and k not in filtered_keys)

    try:
        look_for_keys = module.params['look_for_keys']
        device.open(look_for_keys=look_for_keys)
    except ConnectionError as e:
        safe_fail(module, device, msg=str(e),
                  descr='Error opening connection to device.')
    if damp_max_wait_time:
        if not module.params.get('damp_init_wait_time'):
            safe_fail(module,msg='damp_init_wait_time is required for bfd dampening config')
        else:
            if not module.params['secondary']:
                safe_fail(module,msg='secondary is required for bfd dampening config')
    try:
        bfd = Bfd(device,)
    except PYHPError as e:
        safe_fail(module,device,descr='there is problem in setting localuser',
                  msg=str(e))
    try:
        existing = bfd.get_config()
    except PYHPError as e:
        safe_fail(module, device, msg=str(e),
                  descr='Error getting existing config.')

    if state == 'present':
        if existing:
            delta = dict(set(proposed.items()).difference(
                existing.items()))
        else:
            delta = proposed
        if delta:
            bfd.build(stage=True, **delta)

    elif state == 'default':
        bfd.default(stage=True,)

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
                end_state = bfd.get_config()
            except PYHPError as e:
                safe_fail(module, device, msg=str(e),
                          descr='Error on device execution.')
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
