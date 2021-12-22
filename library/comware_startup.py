#!/usr/bin/python

DOCUMENTATION = """
---

module: comware_startup
short_description: config the next restart file or ipe .   patch function not available,please use patch module
description:
    - Offers ability to config the restart file or config image or patch for the device.  
      Supports using .ipe or .bin system and boot packages.
version_added: 1.8
category: System (RW)
author: wangliang
notes:
    - The parameters ipe_package and boot/system are
      mutually exclusive.
    - makesure the files are already existing on the device.
options:
    ipe_package:
        description:
            - File (including abs path path) of the local ipe package.
        required: false
        default: null
        choices: []
        aliases: []
    boot:
        description:
            - File (including abs path) of the local boot package (.bin)
        required: false
        default: null
        choices: []
        aliases: []
    system:
        description:
            - File (including abs path) of the local system package (.bin)
        required: false
        default: null
        choices: []
        aliases: []
    patch:
        description:
            - File (including abs path) of the local patch package (.bin)
        required: false
        default: null
        choices: []
        aliases: []
    delete_ipe:
        description:
            - If ipe_package is used,
              this specifies whether the .ipe file is deleted from the device
              after it is unpacked.
        required: false
        deafult: false
        choices: ['true', 'false', 'yes', 'no']
        aliases: []
    nextstartupfile:
        description:
            - Name of file that will be used for the next start.
        required: false
        default: null
        choices: []
        aliases: []
    filename:
        description:
            - Name of file that will be show content.
        required: false
        default: null
        choices: []
        aliases: []
    show_file:
        description:
            - File that will be used to store the config file content.  Relative path is
              location of ansible playbook. If not set, no file saved.
        required: false
        default: null
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

"""
EXAMPLE = """

#Basic Install OS Bootsys
  comware_startup:
    boot='flash:/s9850_6850-cmw710-boot-r6555p01.bin'
    system='flash:/s9850_6850-cmw710-system-r6555p01.bin'
    patch='flash:/s9850_6850-cmw710-system-patch-r6555p01h31.bin'
    username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
      
#Basic Install OS IPE
  comware_startup: 
    ipe_package='flash:/s9850-h3c.ipe'
    username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
         
#Config next startup file
  comware_startup: 
    nextstartupfile='flash:/123.cfg'
    username={{ username }} password={{ password }} hostname={{ inventory_hostname }} 
      
#Show content for the existing config file
  comware_startup: filename='flash:/123.cfg' show_file='/root/ansible-hpe-cw7-master/123.cfg' username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
"""

import socket
import os
import re

try:
    HAS_PYHP = True
    from pyhpecw7.comware import HPCOM7
    from pyhpecw7.features.file import File
    from pyhpecw7.features.set_startup import SetStartup
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

def write_content(show_file, content):

    with open(show_file, 'w+') as diff:
        diff.write("#######################################\n")
        diff.write('####### CONTENT OF CONFIG FILE ########\n')
        diff.write("#######################################\n")
        diff.write('\n\n')
        diff.write('\n'.join(content))
        diff.write('\n')

def check_file_existing(file_lists, tname):
    for each in file_lists:
        if each == tname:
            return True
    return False

def main():
    module = AnsibleModule(
        argument_spec=dict(
            ipe_package=dict(),
            boot=dict(),
            system=dict(),
            patch=dict(),
            nextstartupfile=dict(required=False, default=None),
            filename=dict(required=False, default=None),
            show_file=dict(required=False, type='str'),
            delete_ipe=dict(choices=BOOLEANS,
                            type='bool',
                            default=False),
            hostname=dict(required=True),
            username=dict(required=True),
            password=dict(required=True, default=None),
            port=dict(type='int', default=830),
            look_for_keys=dict(default=False, type='bool'),
        ),
        supports_check_mode=True
    )

    if not HAS_PYHP:
        safe_fail(module, msg='There was a problem loading from the pyhpecw7 '
                  + 'module.', error=str(ie))

    ipe_package = module.params.get('ipe_package')
    boot = module.params.get('boot')
    system = module.params.get('system')
    patch = module.params.get('patch')
    nextstartupfile = module.params.get('nextstartupfile')
    filename = module.params.get('filename')
    show_file = module.params['show_file']
    hostname = socket.gethostbyname(module.params['hostname'])
    username = module.params['username']
    password = module.params['password']
    port = module.params['port']

    device = HPCOM7(host=hostname, username=username,
                    password=password, port=port, timeout=1200)

    changed = False
    commands = ''

    if ipe_package or boot:
        if ipe_package:
            if boot or system:
                module.fail_json(
                    msg='ipe_package and boot/system parameters are mutually exclusive')
        else:
            if not (boot and system):
                module.fail_json(
                    msg='boot and system parameters must be provided if ipe_package is not')

        already_set = False

        try:
            look_for_keys = module.params['look_for_keys']
            device.open(look_for_keys=look_for_keys)
        except ConnectionError as e:
            safe_fail(module, device, msg=str(e),
                      descr='Error opening connection to device.')

        try:
            ios = SetStartup(device)
            existing = ios.get_reboot_config()
        except PYHPError:
            safe_fail(module, device, msg=str(e),
                      descr='Error getting current config.')

        existing_boot = existing['startup-primary']['boot']
        existing_system = existing['startup-primary']['system']
        existing_patch = existing['startup-primary']['patch']
        if patch:
            patch_basename = os.path.basename(patch)
            if ipe_package:
                ipe_basename = os.path.basename(ipe_package)
                ipe_boot_sys = re.split('-|\.', ipe_basename)[-3:-1]
                patch_boot_sys = re.split('-|\.', patch_basename)[-3:-1]
                if ipe_boot_sys:
                    if ipe_boot_sys[0].lower() in existing_boot.lower()\
                            and ipe_boot_sys[0].lower() in existing_system.lower()\
                            and ipe_boot_sys[1].lower() in existing_boot.lower()\
                            and ipe_boot_sys[1].lower() in existing_system.lower()\
                            and patch_boot_sys[0].lower() in existing_patch.lower()\
                            and patch_boot_sys[1].lower() in existing_patch.lower():
                        already_set = True

                if not already_set:
                    delete_ipe = module.params.get('delete_ipe')
                    ios.build(
                        'ipe', patch=patch, ipe=ipe_package, delete_ipe=delete_ipe, stage=True)
            elif boot:
                boot_basename = os.path.basename(boot)
                system_basename = os.path.basename(system)
                if boot_basename in existing_boot\
                        and system_basename in existing_system\
                        and patch_basename in existing_patch:
                    already_set = True

                if not already_set:
                    ios.build(
                        'bootsys', patch=patch, boot=boot, system=system, stage=True)
        else:
            if ipe_package:
                ipe_basename = os.path.basename(ipe_package)
                ipe_boot_sys = re.split('-|\.', ipe_basename)[-3:-1]
                if ipe_boot_sys:
                    if ipe_boot_sys[0].lower() in existing_boot.lower() \
                            and ipe_boot_sys[0].lower() in existing_system.lower() \
                            and ipe_boot_sys[1].lower() in existing_boot.lower() \
                            and ipe_boot_sys[1].lower() in existing_system.lower() :
                        already_set = True

                if not already_set:
                    delete_ipe = module.params.get('delete_ipe')
                    ios.build(
                        'ipe', ipe=ipe_package, delete_ipe=delete_ipe, stage=True)
            elif boot:
                boot_basename = os.path.basename(boot)
                system_basename = os.path.basename(system)
                if boot_basename in existing_boot \
                        and system_basename in existing_system:
                    already_set = True

                if not already_set:
                    ios.build(
                        'bootsys', boot=boot, system=system, stage=True)

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
                              descr='Error executing commands.')
                changed = True

    if nextstartupfile:
        try:
            look_for_keys = module.params['look_for_keys']
            device.open(look_for_keys=look_for_keys)
        except ConnectionError as e:
            safe_fail(module, device, msg=str(e),
                      descr='error opening connection to device')

        startup_file = File(device, filename=nextstartupfile)
        f_lists = startup_file.get_rollback_file_lists()
        if "flash:/" not in nextstartupfile:
            module.fail_json(msg="please make sure the file is the full path in the flash")
        if nextstartupfile[-4:] != '.cfg':
            module.fail_json(msg='filename should end with .cfg')
        if not check_file_existing(f_lists, nextstartupfile):
            module.fail_json(
                msg='file {0} not in the flash,please check the name of the startup file'.format(nextstartupfile))
        try:
            startup_file.build_startupfile(nextstartupfile)
        except PYHPError as e:
            safe_fail(module, device, msg=str(e),
                      descr='Failed to set startup file.')
        changed = True

    if filename and show_file:
        try:
            look_for_keys = module.params['look_for_keys']
            device.open(look_for_keys=look_for_keys)
        except ConnectionError as e:
            safe_fail(module, device, msg=str(e),
                      descr='error opening connection to device')

        config_file = File(device, filename=filename)
        f_lists = config_file.get_rollback_file_lists()
        if "flash:/" not in filename:
            module.fail_json(msg="please make sure the file is the full path in the flash")
        if filename[-4:] != '.cfg':
            module.fail_json(msg='filename should end with .cfg')
        if not check_file_existing(f_lists, filename):
            module.fail_json(
                msg='file {0} not in the flash,please check the name of the startup file'.format(filename))
        try:
            filecontent = config_file.get_file_content()
            write_content(show_file, filecontent)
        except PYHPError as e:
            safe_fail(module, device, msg=str(e),
                      descr='Failed to get content for the file.')

        changed = True


    results = {}
    results['commands'] = commands
    results['changed'] = changed

    safe_exit(module, device, **results)

from ansible.module_utils.basic import *
main()
