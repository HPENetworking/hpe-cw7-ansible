#!/usr/bin/python


DOCUMENTATION = '''
---

module: comware_compare
short_description: Enter the configuration command and compare it with the expected result.
description:
    - when input command,you need  In single quotes.
version_added: 1.0
category: System (RW)
author: gongqianyu
notes:
    - This modules Enter the configuration command and compare it with the expected result.
      For convenience, put the expected result into a text, and enter the text path and name into the result parameter.
      if display ok,it is consistent.
options:
    cmd:
        description:
            - command.
        required: true
        default: null
        choices: []
        aliases: []
    result:
        description:
            -  text path and name into the result parameter which include expected result .
        required: true
        default: null
        choices: []
        aliases: []
    hostname:
        description:
            - IP Address or hostname of the Comware 7 device that has
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

'''
EXAMPLES = '''

# - name: compare 
#   comware_compare: cmd='dis curr conf | include ssh' result='/root/ansible-hpe-cw7-master/gqy/result.txt' 
                   username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
'''

import socket
import os
import time


try:
    HAS_PYHP = True
    from pyhpecw7.comware import HPCOM7
    from pyhpecw7.features.errors import *
    from pyhpecw7.features.compare import Compare
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
            cmd=dict(required=True),
            result=dict(required=True),
            port=dict(default=830, type='int'),
            hostname=dict(required=True),
            username=dict(required=True),
            password=dict(required=True),
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
    cmd = module.params['cmd']
    result = module.params['result']
    device_args = dict(host=hostname, username=username,
                       password=password, port=port)
    args = dict(cmd=cmd, result=result)
    device = HPCOM7(**device_args)
    proposed = dict((k, v) for k, v in args.items() if v is not None)


    changed = False
    commands = []
    try:
        look_for_keys = module.params['look_for_keys']
        device.open(look_for_keys=look_for_keys)
    except ConnectionError as e:
        safe_fail(module, device, msg=str(e),
                  descr='error opening connection to device')

    COMPARE = Compare(device, cmd, result)

    check = COMPARE.get_result()

    if check == False:
        module.fail_json(msg='compare result is Inconsistent!')

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
    results['commands'] = commands
    results['changed'] = changed
    results['proposed'] = proposed

    safe_exit(module, device, **results)


from ansible.module_utils.basic import *

main()
