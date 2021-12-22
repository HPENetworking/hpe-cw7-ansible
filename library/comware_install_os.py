#!/usr/bin/python

DOCUMENTATION = """
---

module: comware_install_os
short_description: Copy (if necessary) and install
    a new operating system on Comware v7 device
description:
    - Offers ability to copy and install a new operating system on Comware v7
      devices.  Supports using .ipe or .bin system and boot packages.
version_added: 1.8
category: System (RW)
notes:
    - The parameters ipe_package and boot/system are
      mutually exclusive.
    - If the files are not currently on the device,
      they will be transfered to the device.
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
    remote_dir:
        description:
            - The remote directory into which the file(s) would be copied.
              See default.
        required: false
        default: flash:/
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
    reboot:
        description:
            - Determine if the reboot should take place
              after device startup software image is configured
        required: true
        default: null
        choices: ['true', 'false', 'yes', 'no']
        aliases: []
    delay:
        description:
            - If reboot is set to yes, this is the delay in minutes
              to wait before rebooting.
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

# Basic Install OS IPE
- comware_install_os: ipe_package=/usr/5900_5920_5930-CMW710-E2415.ipe reboot=true username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

# Basic Install OS Boot/Sys
- comware_install_os: reboot=yes boot=/usr/5930-cmw710-boot-e2415.bin system=/usr/5930-cmw710-system-e2415.bin username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

"""

import socket
import os
import re

try:
    HAS_PYHP = True
    from pyhpecw7.comware import HPCOM7
    from pyhpecw7.features.file_copy import FileCopy
    from pyhpecw7.features.install_os import InstallOs
    from pyhpecw7.features.reboot import Reboot
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
            ipe_package=dict(),
            boot=dict(),
            system=dict(),
            remote_dir=dict(default='flash:/'),
            delete_ipe=dict(choices=BOOLEANS,
                            type='bool',
                            default=False),
            reboot=dict(required=True,
                        choices=BOOLEANS,
                        type='bool'),
            delay=dict(type='str'),
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

    ipe_package = module.params.get('ipe_package')
    boot = module.params.get('boot')
    system = module.params.get('system')

    if ipe_package:
        if boot or system:
            module.fail_json(
                msg='ipe_package and boot/system parameters are mutually exclusive')
    else:
        if not (boot and system):
            module.fail_json(
                msg='boot and system parameters must be provided if ipe_package is not')

    hostname = socket.gethostbyname(module.params['hostname'])
    username = module.params['username']
    password = module.params['password']
    port = module.params['port']

    device = HPCOM7(host=hostname, username=username,
                    password=password, port=port, timeout=1200)

    changed = False

    reboot = module.params.get('reboot')
    delay = module.params.get('delay')
    already_set = False
    transfered = False

    try:
        look_for_keys = module.params['look_for_keys']
        device.open(look_for_keys=look_for_keys)
    except ConnectionError as e:
        safe_fail(module, device, msg=str(e),
                  descr='Error opening connection to device.')

    try:
        ios = InstallOs(device)
        existing = ios.get_config()
    except PYHPError:
        safe_fail(module, device, msg=str(e),
                  descr='Error getting current config.')

    existing_boot = existing['startup-primary']['boot']
    existing_system = existing['startup-primary']['system']
    remote_dir = module.params['remote_dir']

    if ipe_package:
        ipe_basename = os.path.basename(ipe_package)
        ipe_boot_sys = re.split('-|\.', ipe_basename)[-3:-1]
        if ipe_boot_sys:
            if ipe_boot_sys[0].lower() in existing_boot.lower()\
                    and ipe_boot_sys[0].lower() in existing_system.lower()\
                    and ipe_boot_sys[1].lower() in existing_boot.lower()\
                    and ipe_boot_sys[1].lower() in existing_system.lower():
                already_set = True

        ipe_dst = remote_dir + ipe_basename
        try:
            # preps transfer and checks if source file exists
            ipe_file_copy = FileCopy(device, ipe_package, ipe_dst)
        except PYHPError as fe:
            safe_fail(module, device, msg=str(fe),
                      descr='Error preparing IPE file transfer.')

        if not ipe_file_copy.file_already_exists():
            try:
                ipe_file_copy.transfer_file(look_for_keys=look_for_keys)
                transfered = True
            except PYHPError as fe:
                safe_fail(module, device, msg=str(fe),
                          descr='Error transfering IPE file.')

        if not already_set:
            delete_ipe = module.params.get('delete_ipe')
            ios.build(
                'ipe', ipe=ipe_file_copy.dst, delete_ipe=delete_ipe, stage=True)
    elif boot:
        boot_basename = os.path.basename(boot)
        system_basename = os.path.basename(system)
        if boot_basename in existing_boot\
                and system_basename in existing_system:
            already_set = True

        boot_dst = remote_dir + boot_basename
        try:
            # preps transfer and checks if source file exists
            boot_file_copy = FileCopy(device, boot, boot_dst)
        except PYHPError as fe:
            safe_fail(module, device, msg=str(fe),
                      descr='Error preparing boot file transfer.')

        system_dst = remote_dir + system_basename
        try:
            # preps transfer and checks if source file exists
            system_file_copy = FileCopy(device, system, system_dst)
        except PYHPError as fe:
            safe_fail(module, device, msg=str(fe),
                      descr='Error preparing system file transfer.')

        if not boot_file_copy.file_already_exists():
            try:
                boot_file_copy.transfer_file(look_for_keys=look_for_keys)
                transfered = True
            except PYHPError as fe:
                safe_fail(module, device, msg=str(fe),
                          descr='Error transfering boot file.')

        if not system_file_copy.file_already_exists():
            try:
                system_file_copy.transfer_file(look_for_keys=look_for_keys)
                transfered = True
            except PYHPError as fe:
                safe_fail(module, device, msg=str(fe),
                          descr='Error transfering system file.')

        if not already_set:
            ios.build(
                'bootsys', boot=boot_file_copy.dst,
                system=system_file_copy.dst, stage=True)

    commands = None
    end_state = existing

    reboot_attempt = 'no'
    if device.staged or transfered:
        if reboot and delay:
            reboot_attempt = 'yes'
            os_reboot = Reboot(device)
            os_reboot.build(stage=True, reboot=True, delay=delay)
        commands = device.staged_to_string()
        if module.check_mode:
            safe_exit(module, device, changed=True,
                      commands=commands,
                      transfered=transfered,
                      end_state=end_state)
        else:
            try:
                device.execute_staged()
                end_state = ios.get_config()
            except PYHPError as e:
                safe_fail(module, device, msg=str(e),
                          descr='Error executing commands.')
            changed = True

    results = {}
    results['commands'] = commands
    results['transfered'] = transfered
    results['changed'] = changed
    results['end_state'] = end_state

    if reboot and not delay:
        reboot_attempt = 'yes'
        try:
            device.reboot()
            changed = True

            # for some reason,
            # this is needed to activate the reboot
            try:
                device.close()
            except PYHPError:
                pass
        except PYHPError as e:
            safe_fail(module, device, msg=str(e),
                      descr='Error rebooting the device.')

    results['reboot_attempt'] = reboot_attempt
    safe_exit(module, device, **results)

from ansible.module_utils.basic import *
main()
