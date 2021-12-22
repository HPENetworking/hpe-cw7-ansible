#!/usr/bin/python

DOCUMENTATION = '''

---



module: comware_config
short_description: Back uo current configuration to the specified file
description:
    - Back uo current configuration to the specified file
version_added: 1.8
category: System (RW)
author: liudongxue
notes:
    - This modules backup the config to specified file in specified flash. 
    -You can use the specified file for configuration distribution.
options:
    filefolder:
        description:
            - Full specified backup path on Comware v7 device, e.g. flash:/mypath/.
        required: false
        default: 
        choices: []
        aliases: []   
    arcstate:
        description:
            - The switch of backup
        required: false
        default: absent
        choices: ['absent', 'present']
        aliases: []
    filename:
        description:
            - Backup file
        required: false
        default: my_file
        choices: []
        aliases: []
    replacefile:
        description:
            - Rolling file
        required: false
        default: null
        choices: []
        aliases: []
    repswitch:
        description:
            - Configure rollback switch
        required: false
        default: null
        choices: ['false', 'true']
        aliases: []
    y_or_no:
        description:
            - Configure the switch to save the current configuration during rollback.
        required: false
        default: null
        choices: ['y', 'n']
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



# backup config to flash:/llld/ans.cfg (in flash)
- comware_config: filename=ans arcstate=present filefolder=flash:/llld/ username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
# rollback config to netconf.cfg and save the current configuration(in flash)
- comware_config: repswitch=true replacefile=netconf.cfg y_or_no=y username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
# rollback config to netconf.cfg and do not save the current configuration
comware_config: replacefile=netconf.cfg  repswitch=true y_or_no=n username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

'''



import socket
import os
import re
import time

try:
    HAS_PYHP = True
    from pyhpecw7.comware import HPCOM7
    from pyhpecw7.features.errors import *
    from pyhpecw7.features.file import File
    from pyhpecw7.features.file_copy import FileCopy
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

def view_backup_profile(profilelist,file_name):
    c =[]
    for v in profilelist:
        if file_name in v:
            c.append(v)
    return c
def config_replace_file(replace_file_list):
    listnum=len(replace_file_list)
    listnum=listnum-1
    return replace_file_list[listnum]
def filefolder(filefolder):
    if filefolder.find(':/')< 0 and filefolder!='':
        remote_dir = 'flash:/'
    elif filefolder.find(':/')> 0:
        remote_dir = filefolder.split(':/')[0]+':/'
    return remote_dir
def check_file_existing(file_lists, tname):
    for each in file_lists:
        each_filename = each.split(':/')[1].strip()
        if each_filename == tname:
            return True
    return False

def main():
    module = AnsibleModule(
        argument_spec=dict(
            filefolder=dict(required=False,),
            arcstate=dict(required=False, default='absent', choices=['absent', 'present']),
            filename=dict(required=False, default='my_file'),
            replacefile=dict(required=False),
            repswitch=dict(required=False, choices=['false', 'true']),
            y_or_no = dict(required=False, choices=['y', 'n']),
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
    filefolder = module.params['filefolder']
    arcstate = module.params['arcstate']
    filename = module.params['filename']
    repswitch = module.params['repswitch']
    replacefile = module.params['replacefile']
    y_or_no = module.params['y_or_no']
    changed = False
    try:
        look_for_keys = module.params['look_for_keys']
        device.open(look_for_keys=look_for_keys)
    except ConnectionError as e:
        safe_fail(module, device, msg=str(e),
                  descr='error opening connection to device')

    file_copy = FileCopy(device,'',filefolder)
    if not file_copy.remote_dir_exists:
        file_copy.create_remote_dir()
        filefolder = filefolder.strip('/')
    if filefolder == 'flash:/':
        filefolder = filefolder
    falsh_space=file_copy._get_flash_size()

    rollback_file = File(device, '')
    f_lists = rollback_file.get_rollback_file_lists()
    is_exist = False
    if replacefile:
        if replacefile[-4:] != '.cfg':
            module.fail_json(msg='filename should end with .cfg')
        is_exist = check_file_existing(f_lists, replacefile)
        if not is_exist:
            module.fail_json(msg='Rollback file does not exist')

    if falsh_space < 1000:
        module.fail_json(msg='Not enough flash space')
    if filename:
        if filename[-4:] == '.cfg':
            filename = filename.split('.cfg')[0].strip()
    if arcstate == 'present':
        cmdmand = ['archive configuration location'+' '+ filefolder + ' '+ 'filename-prefix' + ' ' + filename]
        device.stage_config(cmdmand, 'cli_config')
        cmdmand_1 = []
        cmds = 'archive configuration'
        cmdmand_1.append(cmds)
        cmdmand_1.append('y')
        device.stage_config(cmdmand_1, "cli_display")
    if filefolder =='flash:/' and arcstate == 'present' and repswitch== 'true':
        cmdmand = ['archive configuration location'+' '+ filefolder + ' '+ 'filename-prefix' + ' ' + filename]
        device.stage_config(cmdmand, 'cli_config')
        cmdmand_1 = []
        cmds = 'archive configuration'
        cmdmand_1.append(cmds)
        cmdmand_1.append('y')
        device.stage_config(cmdmand_1, "cli_display")        
        if view_backup_profile(f_lists,filename) and not replacefile:
            replacefilelist = view_backup_profile(f_lists,filename)
            if repswitch == 'true':
                refile=config_replace_file(replacefilelist)
                cmdmand = ['configuration replace file'+' '+ filefolder + refile]
                if y_or_no == 'y':
                    cmdmand.append('y')
                    cmdmand.append('y')
                else:
                    cmdmand.append('n')  
                device.stage_config(cmdmand, 'cli_config')
    if is_exist:
        if repswitch == 'true':
            cmdmand = ['configuration replace file flash:/' + replacefile]
            if y_or_no == 'y':
                cmdmand.append('y')
                cmdmand.append('y')
            else:
                cmdmand.append('n')
            device.stage_config(cmdmand, 'cli_config')
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
