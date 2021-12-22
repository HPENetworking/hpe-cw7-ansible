#!/usr/bin/python

DOCUMENTATION = """
---

module: comware_lacp
short_description: Manage lacp system priority, system mac on Comware 7 devices
version_added: 1.0
author: gongqianyu
category: Feature (RW)
options:
    priorityID:
        description:
            - lacp priority,default is 32768
        required: false
        default: null
        choices: []
        aliases: []
    sysmac:
        description:
            - lacp system mac address
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

  # lacp config
  - comware_lacp:
      priorityID:8
      sysmac:2-2-2
      username: "{{ username }}"
      password: "{{ password }}"
      hostname: "{{ inventory_hostname }}"
      state: present

"""

import socket
try:
    HAS_PYHP = True
    from pyhpecw7.features.lacp import Lacp
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
                priorityID=dict(required=False, type='str'),
                sysmac=dict(required=False, type='str'),
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

    device = HPCOM7(host=hostname, username=username,
                    password=password, port=port)

    priorityID = module.params['priorityID']
    sysmac = module.params['sysmac']
    state = module.params['state']

    changed = False
    args = dict(priorityID=priorityID, sysmac=sysmac)
    proposed = dict((k, v) for k, v in args.items() if v is not None)

    try:
        look_for_keys = module.params['look_for_keys']
        device.open(look_for_keys=look_for_keys)
    except ConnectionError as e:
        safe_fail(module, device, msg=str(e),
                  descr='error connecting to device')

    try:
        LACP = Lacp(device,priorityID)

    except PYHPError as e:
        safe_fail(module, device, msg=str(e))


    if state == 'present':

        if module.params.get('priorityID'):
               LACP.build(stage=True)
        if module.params.get('sysmac'):
            LACP.build_time(stage=True, sysmac=sysmac)

    elif state == 'default':

            if module.params.get('priorityID'):
                   LACP.remove(stage=True)
            if module.params.get('sysmac'):
                LACP.build_time_absent(stage=True, sysmac=sysmac)

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
    results['proposed'] = proposed
    results['state'] = state
    results['commands'] = commands
    results['changed'] = changed

    safe_exit(module, device, **results)

from ansible.module_utils.basic import *
main()













