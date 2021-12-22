#!/usr/bin/python


DOCUMENTATION = '''
---

module: comware_patch
short_description: Rollback the running configuration
description:
    - Rollback theconfiguration to the file
version_added: 1.8
category: System (RW)
author: wangliang
notes:
    - This modules rollback the config to startup.cfg, or the supplied
      filename, in flash. It is not
      changing the config file to load on next boot.
options:
    patchname:
        description:
            - Name of patch that will be used .
        required: false
        default: null
        choices: []
        aliases: []
    activate:
        description:
            - active patch or not.
        required: false
        default: null
        choices: ['false', 'true']
        aliases: []
    check_result:
        description:check patch active success or not .
        required: false
        default: false
        choices: ['true','false']
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

      - name: copy version from ansible server into switch.
        comware_file_copy: file=/root/ansible-hpe-cw7-master/gqy/s6820-cmw710-system-weak-patch-f6205p05h16.bin remote_path=flash:/s6820-cmw710-system-weak-patch-f6205p05h16.bin username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

      - name: check bin is exit or not and active it.
        comware_patch: patchname=patch.bin activate=true username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
        async: 60
        poll: 0

      - name: check patch is active or not 
        comware_patch: patchname=s6805-cmw710-boot-r6607.bin check_result=true username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

'''

import socket
import os
import time


try:
    HAS_PYHP = True
    from pyhpecw7.comware import HPCOM7
    from pyhpecw7.features.errors import *
    from pyhpecw7.features.patch import Patch
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
            patchname=dict(required=True),
            activate=dict(required=False, choices=['true', 'false']),
            check_result=dict(required=False, choices=['true', 'false']),
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
    patchname = module.params['patchname']
    activate = module.params['activate']
    check_result = module.params['check_result']
    device_args = dict(host=hostname, username=username,
                       password=password, port=port, timeout=90)
    args = dict(patchname=patchname, activate=activate, check_result=check_result)
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

    check_file = Patch(device, patchname)

    check = check_file.get_file_lists()

    if check == False:
        module.fail_json(msg='file {0} not in the flash,please check the name of the patch file'.format(patchname))

    if activate == 'true':
        active = check_file.build(stage=True)
        if active == False:
            module.fail_json(msg='activate fail!')

    if check_result == 'true':
        # time.sleep(40)
        Result = check_file.Check_result()
        if Result == False:
            module.fail_json(msg='activate failed!')

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
