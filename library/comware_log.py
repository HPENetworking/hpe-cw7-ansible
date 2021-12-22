#!/usr/bin/python

DOCUMENTATION = """
---

module: comware_log
short_description: get the device diagnostic information and upload to file server
description:
    - get the device diagnostic information and upload to file server
version_added: 1.8
category: Feature (RW)
author: null
notes:
    - Getting device diagnostic information will take some time , here give 300s to get the information,
      if result goes to time out , check the timeout 300s first.
    - if state is present , you will get the diag file with .tar.gz , and it will upload to ansible 
      server.
    -  
options:
    service_dir:
        description:
            - the dir in server which you want to upload the diag file from device
        required: false
        default: null
        choices: []
        aliases: []
    diag_dir:
        description:
            - where the device diagnostic information storage , default is flash:/
        required: false
        default: 'flash:/'
        choices: []
        aliases: []
    ftpupload:
        description:
            - whether upload the diagnostic information to the service.
        required: false
        default: true
        choices: ['true','false']
        aliases: []
    servertype:
        description:
            - choose the diagnostic file upload server type.
        required: false
        default: null
        choices: ['ftp','scp']
        aliases: []
    server_hostname:
        description:
            - the remote server hostname e.g.192.168.1.199.
        required: false
        default: null
        choices: []
        aliases: []
    server_name:
        description:
            - the name to login in remote server.
        required: false
        default: null
        choices: []
        aliases: []
    server_pwd:
        description:
            - the password to login in remote server.
        required: false
        default: null
        choices: []
        aliases: []
    dst_dir:
        description:
            - remote dir where the file save.
        required: false
        default: null
        choices: []
        aliases: []
    state:
        description:
            - The state of operation
        required: false
        default: null
        choices: ['present', 'default', 'loadtoserver']
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
            - The Comware port used to connect to the switch
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

# e.g.ensure the dir exsits
      - name: get diagnostic information to the file server
        comware_log:  diag_dir=flash:/diaglog service_dir=/root/ansible-hpe-cw7-master/diaglog/ ftpupload=true 
        username={{ username }} password={{ password }} hostname={{ inventory_hostname }}     
              
      - name: delete diagnostic information in device
        comware_log:  state=loadtoserver servertype=ftp server_hostname=192.168.1.199 server_name=fc server_pwd=111111 
        diag_dir=flash:/diaglog service_dir=/root/ansible-hpe-cw7-master/diaglog/ dst_dir= 
        username={{ username }} password={{ password }} hostname={{ inventory_hostname }} 
                                       
      # - name: delete diagnostic information in device
        # comware_log:  state=loadtoserver servertype=scp server_hostname=192.168.1.185 server_name=h3c server_pwd=h3c 
        diag_dir=flash:/diaglog service_dir=/root/ansible-hpe-cw7-master/diaglog/ dst_dir=flash:/ 
        username={{ username }} password={{ password }} hostname={{ inventory_hostname }} 
        
      - name: delete diagnostic information in device
        comware_log:  diag_dir=flash:/diaglog state=default username={{ username }} password={{ password }} hostname={{ inventory_hostname }} 
        
"""

import socket
import time
import re
import paramiko
import hashlib
from scp import SCPClient

try:
    HAS_PYHP = True
    from pyhpecw7.comware import HPCOM7
    from pyhpecw7.features.file_copy import FileCopy
    from pyhpecw7.features.errors import InterfaceError
    from ftplib import FTP
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
            service_dir=dict(type='str'),
            diag_dir=dict(type='str',default='flash:/'),
            ftpupload=dict(required=False, default='true', choices=['true', 'false']),
            servertype=dict(required=False,choices=['ftp','scp']),
            server_hostname=dict(type='str'),
            server_name=dict(type='str'),
            server_pwd=dict(type='str'),
            dst_dir=dict(type='str'),
            state=dict(choices=['present', 'default', 'loadtoserver'],
                       default='present'),
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

    filtered_keys = ('state', 'hostname', 'username', 'password',
                     'port', 'CHECKMODE', 'name', 'look_for_keys')

    hostname = socket.gethostbyname(module.params['hostname'])
    username = module.params['username']
    password = module.params['password']
    port = module.params['port']
    device = HPCOM7(host=hostname, username=username,
                    password=password, port=port,timeout=300)
    state = module.params['state']
    diag_dir = module.params['diag_dir']
    service_dir = module.params.get('service_dir')
    ftpupload = module.params.get('ftpupload')
    server_hostname = module.params.get('server_hostname')
    server_name = module.params.get('server_name')
    server_pwd = module.params.get('server_pwd')
    dst_dir = module.params.get('dst_dir')
    changed = False
    proposed = dict((k, v) for k, v in module.params.items()
                    if v is not None and k not in filtered_keys)

    try:
        look_for_keys = module.params['look_for_keys']
        device.open(look_for_keys=look_for_keys)
    except ConnectionError as e:
        safe_fail(module, device, msg=str(e),
                  descr='Error opening connection to device.')

    if module.params.get('diag_dir'):
        res = re.search(r'^flash:/',diag_dir)
        if not res:
            safe_fail(module,msg='please check diagnose dir ')
        res1 = re.search(r'\/$',diag_dir)
        if not res1:
            diag_dir = diag_dir+'/'

    if module.params.get('service_dir'):
        res2 = re.search(r'\/$',service_dir)
        if not res2:
            service_dir = service_dir+'/'

    if module.params.get('state') == 'loadtoserver':
        if not module.params.get('servertype'):
            safe_fail(module,msg='please choose server type to upload log')

    if state == 'present':
        timenow = time.localtime()
        timeinfo = str(timenow.tm_year) + str(timenow.tm_mon).zfill(2) + str(timenow.tm_mday).zfill(2) + \
                   str(timenow.tm_hour).zfill(2) + str(timenow.tm_min).zfill(2) + str(timenow.tm_sec).zfill(2)
        log_file_name = 'diag_H3C_'+timeinfo+'.tar.gz'
        src = service_dir + log_file_name
        dst = diag_dir + log_file_name
        file_copy = FileCopy(device, src, dst)
        if not file_copy.remote_dir_exists:
            file_copy.create_remote_dir()
            cmd = ['dis diagnostic-information '+diag_dir+log_file_name]
        else:
            cmd = ['dis diagnostic-information '+diag_dir+log_file_name]
        device.cli_display(cmd)
        command = ['dir' + ' ' + diag_dir]
        diaglog = device.cli_display(command)
        changed = True
        regex = re.compile(r'diag.*.tar.gz')
        existlog = regex.findall(diaglog)
        if module.params.get('service_dir'):
            if log_file_name in existlog:
                diag_name = existlog[-1]
                file = diag_dir+diag_name
                service_file = service_dir+diag_name
                if ftpupload.lower() == 'true':
                    ssh = paramiko.SSHClient()
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    ssh.connect(hostname=hostname, username=username, password=password,look_for_keys=False)
                    scp = SCPClient(ssh.get_transport())
                    scp.get(file,service_file)
                    changed = True
            else:
                safe_fail(module,msg='can not get diagnostic information , please check the diag dir ')

    elif state == 'loadtoserver':
        command = ['dir' + ' ' + diag_dir]
        diaglog = device.cli_display(command)
        regex = re.compile(r'diag.*.tar.gz')
        existlog = regex.findall(diaglog)
        if not existlog:
            safe_fail(module,msg='can not find file')
        src = service_dir+existlog[-1]
        dst = dst_dir+existlog[-1]
        if src:
            if module.params.get('servertype') == 'ftp':
                server_ftp = FileCopy(device,src,dst)
                server_ftp.ftp_file(hostname=server_hostname,
                                    username=server_name,
                                    password=server_pwd)
                changed = True
            if module.params.get('servertype') == 'scp':
                server_scp = FileCopy(device,src,dst)
                server_scp.transfer_file(hostname=server_hostname,
                                         username=server_name,
                                         password=server_pwd)
                changed = True

    elif state == 'default':
        cmd = ['delete /unreserved'+' '+diag_dir+'diag*.tar.gz']
        device.cli_display(cmd)
        changed = True


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
                          descr='Error on device execution.')
            changed = True

    results = {}
    results['proposed'] = proposed
    results['commands'] = commands
    results['changed'] = changed

    safe_exit(module, device, **results)

from ansible.module_utils.basic import *
main()
