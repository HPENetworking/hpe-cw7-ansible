#!/usr/bin/python

DOCUMENTATION = """
---

module: comware_netconf
short_description: Manage netconf log and xml function on Comware 7 devices.XML cfg not support enter xml view now,This is not normally done.
version_added: 1.0
author: gongqianyu
category: Feature (RW)
notes:
options:
    source:
        description:
            - NETCONF operation source requiring log output.Option 'all' means all source.
        required: False
        default: null
        choices: [all, agent, soap, web]
        aliases: []
    operation: 
        description:
            - Netconf operation option.If you chose protocol-operation,the opera_type option must be config.
        required: False
        default: null
        choices: [protocol-operation, row-operation, verbose] 
        aliases: []
    opera_type: 
        description:
            - Protocol-operation option.
        required: False
        default: null
        choices: [all, action, config, get, session, set, syntax, others] 
        aliases: []
    state:
        description:
            - Desired state for the interface configuration
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

  # netconf config
  - comware_netconf:
      source: all
      operation: protocol-operation
      opera_type: action
      username: "{{ username }}"
      password: "{{ password }}"
      hostname: "{{ inventory_hostname }}"

  # detele netconf config    
  - comware_netconf:
      source: all
      operation: protocol-operation
      opera_type: action
      username: "{{ username }}"
      password: "{{ password }}"
      hostname: "{{ inventory_hostname }}"
      state: absent

comware_netconf: soap=http ssh=enable username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
"""

import socket
try:
    HAS_PYHP = True
    from pyhpecw7.features.netconf import Netconf
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
            source=dict(required=False,choices=['all', 'agent', 'soap', 'web']),
            operation=dict(required=False, choices=['protocol-operation', 'row-operation', 'verbose']),
            opera_type = dict(required=False, choices=['all', 'action', 'config', 'get', 'session', 'set', 'syntax', 'others']),
            soap = dict(required=False, choices=['http', 'https']),
            ssh = dict(required=False, choices=['enable', 'disable'], default='disable'),
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
    source = module.params['source']
    soap = module.params['soap']
    ssh = module.params['ssh']
    operation = module.params['operation']
    opera_type = module.params['opera_type']
    state = module.params['state']
    args = dict(source=source, operation=operation, opera_type=opera_type, soap=soap, ssh=ssh)
    proposed = dict((k, v) for k, v in args.items() if v is not None)

    changed = False

    try:
        look_for_keys = module.params['look_for_keys']
        device.open(look_for_keys=look_for_keys)
    except ConnectionError as e:
        safe_fail(module, device, msg=str(e),
                  descr='error connecting to device')

    try:
        netConf = Netconf(device, source, operation, opera_type, soap, ssh)
    except PYHPError as e:
        safe_fail(module, device, msg=str(e))

    if state == 'present':
        netConf.build(stage=True)
    elif state == 'absent':
        netConf.remove(stage=True)

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
