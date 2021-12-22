#!/usr/bin/python

DOCUMENTATION = """
---

module: comware_syslog_global
short_description: Manage system log timestamps and  terminal logging level on Comware 7 devices
version_added: 1.0
author: gongqianyu
category: Feature (RW)
notes:
    - Before configuring this,the global syslog need to be enabled.
    - The timestamps default state is data, terminal logging level default is 6.
options:
    timestamps:
        description:
            - Configure the time stamp output format of log information sent to the console, monitoring terminal, 
               log buffer and log file direction.
        required: False
        default: date
        choices: [boot, date, none]
        aliases: []
    level:
        description:
            - Configure the minimum level of log information that the current terminal allows to output.
        required: False
        default: informational
        choices: [alert, critical, debugging, emergency, error, informational, notification, warning]
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

  # timestamps and level config
  - comware_syslog_global: timestamps=boot  level=debugging username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

  # Restore timestamps and level to default state    
  - comware_syslog_global:timestamps=boot level=debugging username={{ username }} password={{ password }} hostname={{ inventory_hostname }} state=absent

"""

import socket
try:
    HAS_PYHP = True
    from pyhpecw7.features.syslog_global import Syslog
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
            timestamps=dict(required=False,choices=['boot', 'date', 'none'], default='date'),
            level=dict(required=False, choices=['alert', 'critical', 'debugging', 'emergency', 'error', 'informational', 'notification', 'warning'], default='informational'),
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
    timestamps = module.params['timestamps']
    level = module.params['level']
    state = module.params['state']
    args = dict(timestamps=timestamps, level=level)
    proposed = dict((k, v) for k, v in args.items() if v is not None)

    changed = False

    try:
        look_for_keys = module.params['look_for_keys']
        device.open(look_for_keys=look_for_keys)
    except ConnectionError as e:
        safe_fail(module, device, msg=str(e),
                  descr='error connecting to device')

    try:
        sysLog = Syslog(device, timestamps, level)
    except PYHPError as e:
        safe_fail(module, device, msg=str(e))

    if state == 'present':
        sysLog.build(stage=True)
    elif state == 'absent':
        sysLog.remove(stage=True)

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
