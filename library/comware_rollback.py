#!/usr/bin/python


DOCUMENTATION = '''
---

module: comware_rollback
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
    filename:
        description:
            - Name of file that will be used when rollback the conifg to flash.
        required: false
        default: startup.cfg
        choices: []
        aliases: []
    comparefile:
        description:
            - Name of file that will be used when compared with filename file. 
              if not set, no compared action executed.
        required: false
        default: null
        choices: []
        aliases: []
    clean:
        description:
            - delete the rollback point
        required: false
        default: false
        choices: ['true','false']
        aliases: []
    diff_file:
        description:
            - File that will be used to store the diffs.  Relative path is
              location of ansible playbook. If not set, no diffs are saved.
        required: false
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

# rollback config to myfile.cfg (in flash)
- comware_rollback: filename=myfile.cfg username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

# rollback config to startup.cfg (in flash)
- comware_rollback: username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

# delete rollback point 123.cfg (in flash)
- comware_rollback: filename=123.cfg clean=true username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

# files compared
- comware_rollback: filename=123.cfg comparefile=test.cfg username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
  diff_file='/root/ansible-hpe-cw7-master/diffs.diff'
'''

import socket
import os

try:
    HAS_PYHP = True
    from pyhpecw7.comware import HPCOM7
    from pyhpecw7.features.errors import *
    from pyhpecw7.features.file import File
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


def check_file_existing(file_lists, tname):
    for each in file_lists:
        each_filename = each.split(':/')[1].strip()
        if each_filename == tname:
            return True
    return False

def write_diffs(diff_file, diffs, full_diffs):

    with open(diff_file, 'w+') as diff:
        diff.write("#######################################\n")
        diff.write('########## SUMMARY OF DIFFS ###########\n')
        diff.write("#######################################\n")
        diff.write('\n\n')
        diff.write('\n'.join(diffs))
        diff.write('\n\n\n')
        diff.write("#######################################\n")
        diff.write('FULL DIFFS AS RETURNED BACK FROM SWITCH\n')
        diff.write("#######################################\n")
        diff.write('\n\n')
        diff.write('\n'.join(full_diffs))
        diff.write('\n')

def main():
    module = AnsibleModule(
        argument_spec=dict(
            filename=dict(required=False, default='startup.cfg'),
            clean=dict(required=False, default='false', choices=['true', 'false']),
            diff_file=dict(required=False, type='str'),
            comparefile=dict(required=False, default=None),
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

    device_args = dict(host=hostname, username=username,
                       password=password, port=port)

    device = HPCOM7(**device_args)

    filename = module.params['filename']
    comparefile = module.params['comparefile']
    diff_file = module.params['diff_file']
    clean = module.params['clean']
    if "/" in filename:
        module.fail_json(msg="specify only filename")
    if filename[-4:] != '.cfg':
        module.fail_json(msg='filename should end with .cfg')

    changed = False
    commands = ''
    try:
        look_for_keys = module.params['look_for_keys']
        device.open(look_for_keys=look_for_keys)
    except ConnectionError as e:
        safe_fail(module, device, msg=str(e),
                  descr='error opening connection to device')

    rollback_file = File(device, filename, comparefile)
    f_lists = rollback_file.get_rollback_file_lists()
    if not check_file_existing(f_lists, filename):
        module.fail_json(msg='file {0} not in the flash,please check the name of the rollback file'.format(filename))

    if comparefile and diff_file:
        if "/" in comparefile:
            module.fail_json(msg="specify only comparefile")
        if filename[-4:] != '.cfg':
            module.fail_json(msg='comparefile should end with .cfg')
        if not check_file_existing(f_lists, comparefile):
            module.fail_json(
                msg='file {0} not in the flash,please check the name of the rollback file'.format(comparefile))

        diffs, full_diffs = rollback_file.compare_rollback_files()
        write_diffs(diff_file, diffs, full_diffs)

    else:
        diffs = 'None.  diff_file param not set in playbook'

    if clean == 'false':
        device.stage_config('{0}'.format(filename), "rollback")
    elif clean == 'true':
        cmdmand = []
        cmd = 'delete /unreserved flash:/{0}'.format(filename)
        cmdmand.append(cmd)
        cmdmand.append('y')
        device.stage_config(cmdmand, "cli_display")

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

    safe_exit(module, device, **results)


from ansible.module_utils.basic import *

main()
