#!/usr/bin/python

DOCUMENTATION = """
---

module: comware_command
short_description: Execute CLI commands on Comware 7 devices
description:
    - Execute CLI commands on Comware 7 devices
version_added: 1.8
author: liudongxue
category: Feature (RW)
notes:
    - This module is not idempotent
options:
    type:
        description:
            - State whether the commands are display (user view)
              or configure (system view) commands.  Display and
              show are the same thing.
        required: true
        default: null
        choices: ['display', 'config', 'show']
        aliases: []
    command:
        description:
            - String (single command) or list of commands to be
              executed on the device.  Sending a list requires
              YAML format to be used in the playbook.
        required: true
        default: null
        choices: []
        aliases: []
    file_txt:
        description:
            - Text file on server.
              Include file path and file name.
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
    look_for_keys:
        description:
            - Whether searching for discoverable private key files in ~/.ssh/
        required: false
        default: False
        choices: []
        aliases: []
    

"""

EXAMPLES = """

# display vlan 10 passing in a string
- comware_command: command='display vlan 5' type=display username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

# execute command by using file
- comware_command: file_txt=/root/ansible-hpe-cw7-master/test.txt type=config username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

# display vlans passing in a list
- comware_command:
    command:
      - display vlan 10
      - display vlan 5
    type: display
    username: "{{ username }}"
    password: "{{ password }}"
    hostname: "{{ inventory_hostname }}"

# passing in config commands as a list
- comware_command:
    command:
      - vlan 5
      - name web_vlan
    type: config
    username: "{{ username }}"
    password: "{{ password }}"
    hostname: "{{ inventory_hostname }}"

"""

import socket
import sys
import os

try:
    HAS_PYHP = True
    from pyhpecw7.comware import HPCOM7
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
def file_list(file):
    fp=open(str(file),'rb')
    txt=fp.read()
    txt_list = txt.split('\r\n')
    commandlist=[x for x in txt_list if x!='']
    return commandlist

def main():
    module = AnsibleModule(
        argument_spec=dict(
            type=dict(required=True, choices=['display', 'show', 'config']),
            command=dict(required=False, type='list'),
            file_txt=dict(required=False, type='str'),
            port=dict(default=830, type='int'),
            hostname=dict(required=True),
            username=dict(required=True),
            password=dict(required=False, default=None),
            look_for_keys=dict(default=False, type='bool'),
        ),
        supports_check_mode=True
    )

    if not HAS_PYHP:
        safe_fail(module, msg='There was a problem loading from the pyhpecw7 '
                  + 'module.', error=str(ie), path=str(sys.path))

    username = module.params['username']
    password = module.params['password']
    port = module.params['port']
    hostname = socket.gethostbyname(module.params['hostname'])

    device_args = dict(host=hostname, username=username,
                       password=password, port=port)

    device = HPCOM7(**device_args)

    ctype = module.params['type']
    command = module.params['command']
    file_txt = module.params['file_txt']
    if file_txt:
        command=file_list(file_txt)
    changed = False

    proposed = dict(type=ctype, command=command)

    try:
        look_for_keys = module.params['look_for_keys']
        device.open(look_for_keys=look_for_keys)
    except ConnectionError as e:
        safe_fail(module, device, msg=str(e),
                  descr='error during device open')

    
    response = None
    if isinstance(command, list):
        config_string = ';'.join(command)

    else:
        config_string = command
    
    if module.check_mode:
        safe_exit(module, device, changed=True,
                  config_string=config_string)

    try:
        if ctype in ['show', 'display']:
            response = device.cli_display(command)
        elif ctype in ['config']:
            response = device.cli_config(command)
    except PYHPError as e:
        safe_fail(module, device, msg=str(e),
                  descr='error during execution')

    res_by_line = response.split('\n')

    changed = True

    results = {}
    results['proposed'] = proposed
    results['config_string'] = config_string
    results['changed'] = changed
    results['end_state'] = 'N/A for this module.'
    results['response'] = res_by_line

    safe_exit(module, device, **results)

from ansible.module_utils.basic import *
main()
