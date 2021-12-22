#!/usr/bin/python

DOCUMENTATION = """
---

module: comware_install_config
short_description: Activate a new current-running config in realtime
description:
    - Activate a new current-running config in realtime
version_added: 1.8
category: System (RW)
notes:
    - Check mode copies config file to device and still generates diffs
    - diff_file must be specified to write diffs to a file, otherwise,
      only summarized diffs are returned from the module
    - commit_changes must be true to apply changes
    - this module does an automatic backup of the existing config
      to the filename flash:/safety_file.cfg
    - this module does an auto save to flash:/startup.cfg upon completion
    - config_file MUST be a valid FULL config file for a given device.
options:
    config_file:
        description:
            - File that will be sent to the device.  Relative path is
              location of Ansible playbook.  Recommended to use
              absolute path.
        required: true
        default: null
        choices: []
        aliases: []
    commit_changes:
        description:
            - Used to determine the action to take after transferring the
              config to the switch.  Either activate using the rollback
              feature or load on next-reboot.
        required: true
        default: null
        choices: ['true', 'false']
        aliases: []
    diff_file:
        description:
            - File that will be used to store the diffs.  Relative path is
              location of ansible playbook. If not set, no diffs are saved.
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

# install config file that will be the new running config
- comware_install_config:
    config_file='/root/ansible-hpe-cw7-master/gqy/123.cfg'
    diff_file='/root/ansible-hpe-cw7-master/gqy/diffs.diff'
    commit_changes=true
    username={{ username }}
    password={{ password }}
    hostname={{ inventory_hostname }}

"""

import socket
import os
try:
    HAS_PYHP = True
    from pyhpecw7.features.config import Config
    from pyhpecw7.features.file_copy import FileCopy
    from pyhpecw7.comware import HPCOM7
    from pyhpecw7.features.errors import *
    from pyhpecw7.errors import *
except ImportError as ie:
    HAS_PYHP = False


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
            config_file=dict(required=True, type='str'),
            diff_file=dict(required=False, type='str'),
            commit_changes=dict(required=True, choices=BOOLEANS, type='bool'),
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
                  + 'module.', error=str(ie))

    username = module.params['username']
    password = module.params['password']
    port = module.params['port']
    hostname = socket.gethostbyname(module.params['hostname'])

    device_args = dict(host=hostname, username=username,
                       password=password, port=port)

    device = HPCOM7(timeout=60, **device_args)

    config_file = module.params['config_file']
    diff_file = module.params['diff_file']
    commit_changes = module.params['commit_changes']

    changed = False

    if os.path.isfile(config_file):
        file_exists = True
    else:
        safe_fail(module, msg='Cannot find/access config_file:\n{0}'.format(
            config_file))

    try:
        look_for_keys = module.params['look_for_keys']
        device.open(look_for_keys=look_for_keys)
    except ConnectionError as e:
        safe_fail(module, device, msg=str(e),
                  descr='error opening connection to device')

    if file_exists:
        basename = os.path.basename(config_file)
        try:
            copy = FileCopy(device,
                            src=config_file,
                            dst='flash:/{0}'.format(basename))
            copy.transfer_file(look_for_keys=look_for_keys)
            cfg = Config(device, config_file)
        except PYHPError as fe:
            safe_fail(module, device, msg=str(fe),
                      descr='file transfer error')

    if diff_file:
        diffs, full_diffs = cfg.compare_config()
        write_diffs(diff_file, diffs, full_diffs)
    else:
        diffs = 'None.  diff_file param not set in playbook'

    cfg.build(stage=True)

    active_files = {}
    if device.staged:
        active_files = dict(backup='flash:/safety_file.cfg',
                            startup='flash:/startup.cfg',
                            config_applied='flash:/' + basename)
        if module.check_mode:
            safe_exit(module, device, changed=True,
                      active_files=active_files,
                      diffs=diffs,
                      diff_file=diff_file,
                      config_file=config_file)
        else:
            if commit_changes:
                try:
                    switch_response = device.execute_staged()
                    # TODO: check of "ok" or errors?
                except NCError as err:
                    if err.tag == 'operation-failed':
                        safe_fail(module, device, msg='Config replace operation'
                                  + ' failed.\nValidate the config'
                                  + ' file being applied.')
                except PYHPError as e:
                    safe_fail(module, device, msg=str(e),
                              descr='error during execution')

                changed = True

    results = {}
    results['changed'] = changed
    results['active_files'] = active_files
    results['commit_changes'] = commit_changes
    results['diff_file'] = diff_file
    results['config_file'] = config_file

    safe_exit(module, device, **results)

from ansible.module_utils.basic import *
main()
