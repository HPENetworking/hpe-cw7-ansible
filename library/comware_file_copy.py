#!/usr/bin/python

DOCUMENTATION = """
---

module: comware_file_copy
short_description: Copy a local file to a remote Comware v7 device
description:
    - Copy a local file to a remote Comware v7 device
version_added: 1.8
category: System (RW)
author: liudongxue
notes:
    - If the remote directory doesn't exist, it will be automatically
      created.
    - If you want to use FTP, you need to enable the FTP function on the device,
      e.g.
        [Sysname] local-user h3c class manage
        [Sysname-luser-manage-h3c] service-type ftp
        [Sysname] ftp server enable
      You can configure it using the 'comware_local_user.py' and 'comware_ftp.py' modules first.
options:
    file:
        description:
            - File (including absolute path of local file) that will be sent
              to the device
        required: true
        default: null
        choices: []
        aliases: []
    remote_path:
        description:
            - Full file path on remote Comware v7 device, e.g. flash:/myfile.
              If no directory is included in remote_path, flash will be prepended.
              If remote_path is omitted, flash will be prepended to the source file name.
        required: false
        default: flash:/<file>
        choices: []
        aliases: []
    ftpupload:
        description:
            - If you want to upload by FTP, change the params to true
        required: false
        default: false
        choices: ['true', 'false']
        aliases: []
    ftpdownload:
        description:
            - If you want to download by FTP, change the params to true
        required: false
        default: false
        choices: ['true', 'false']
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

EXAMPLES = """

# copy file
- comware_file_copy: file=/usr/smallfile remote_path=flash:/otherfile 
  username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
  
- comware_file_copy: file=/root/ansible-hpe-cw7-master/hp-vlans.yml remote_path=flash:/ldx/hp-vlans.yml 
  ftpupload=true username={{ username }} password={{ password }}   hostname={{ inventory_hostname }}
  
# name: use FTP to download files to the server--module 1.3
  comware_file_copy: file=/root/ansible-hpe-cw7-master/11.txt remote_path=flash:/llld/11.txt ftpdownload=true username={{ username }} password={{ password }}   hostname={{ inventory_hostname }}
  """
import socket

try:
    HAS_PYHP = True
    from pyhpecw7.comware import HPCOM7
    from pyhpecw7.features.file_copy import FileCopy
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
            file=dict(required=True),
            remote_path=dict(),
            ftpupload=dict(required=False, default='false', choices=['true', 'false']),
            ftpdownload=dict(required=False, default='false', choices=['true', 'false']),
            hostname=dict(required=True),
            username=dict(required=True),
            password=dict(required=False, default=None),
            port=dict(type='int', default=830),
            look_for_keys=dict(default=False, type='bool'),
        ),
        supports_check_mode=False
    )

    if not HAS_PYHP:
        safe_fail(module, msg='There was a problem loading from the pyhpecw7 '
                  + 'module.', error=str(ie))

    hostname = socket.gethostbyname(module.params['hostname'])
    username = module.params['username']
    password = module.params['password']
    port = module.params['port']

    device = HPCOM7(host=hostname, username=username,
                    password=password, port=port, timeout=1200)

    src = module.params.get('file')
    dst = module.params.get('remote_path')
    ftpupload = module.params.get('ftpupload')
    ftpdownload = module.params.get('ftpdownload')
    changed = False

    try:
        look_for_keys = module.params['look_for_keys']
        device.open(look_for_keys=look_for_keys)
    except ConnectionError as e:
        safe_fail(module, device, msg=str(e),
                  descr='Error opening connection to device.')

    #file_copy.ftp_file(hostname='192.168.1.143', username='h3c', password='h3c')
    try:
        file_copy = FileCopy(device, src, dst)
        if ftpdownload=='false':
            if not file_copy.file_already_exists():
                if not file_copy.remote_dir_exists:
                    file_copy.create_remote_dir()
                if ftpupload== 'true':
                    file_copy.ftp_file()
                else:
                    file_copy.transfer_file(look_for_keys=look_for_keys)
        else :
            if file_copy.remote_dir_exists:
                file_copy.ftp_downloadfile()
            else:
                safe_fail(module,msg='The remote path not exists , please check it')
        changed = True
        
    except PYHPError as fe:
        safe_fail(module, device, msg=str(fe),
                  descr='Error transferring file.')

    results = {}
    results['source_file'] = file_copy.src
    results['destination_file'] = file_copy.dst
    results['changed'] = changed

    safe_exit(module, device, **results)

from ansible.module_utils.basic import *
main()
