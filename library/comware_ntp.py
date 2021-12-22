#!/usr/bin/python

DOCUMENTATION = """
---

module: comware_ntp
short_description: Configure the ntp issue to be applied to the device.
description:
    -Configure the ntp issue to be applied to the device.
version_added: 1.8
category: Feature (RW)
author: liudongxue
notes:
    - When configurating clients, IPv6 does not support.
    - The keyid is unsigned integer,and the value range is 1 to 4294967295.
    - The type of authkey is string,the length is 1 to 32 characters.
      The stratum is unsigned integer,and the value range is 1 to 15.
options:
    name:
        description:
            - Full name of the interface
        required: false
        default: null
        choices: []
        aliases: []
    ntpenable:
        description:
            - The status of NTP
        required: false
        default: false
        choices: ['true', 'false']
        aliases: []
    state:
        description:
            - Desired state for the interface configuration
        required: false
        default: present
        choices: ['present', 'absent']
        aliases: []
    ntpauthenable:
        description:
            - The status of NTP authentication
        required: false
        default: false
        choices: ['true', 'false']
        aliases: []
    stratum:
        description:
            -  The stratum level of the local clock
        required: false
        default: null
        choices: []
        aliases: []
    service:
        description:
            - The service of NTP 
        required: false
        default: null
        choices: ['ntp', 'sntp']
        aliases: []
    keyid:
        description:
            - The authentication-keys of NTP
        required: false
        default: null
        choices: []
        aliases: []
    authmode:
        description:
            - Authentication mode
        required: false
        default: null
        choices: ['md5', 'hmac_sha_1', 'hmac_sha_256', 'hmac_sha_384', 'hmac_sha_384']
        aliases: [] 
    authkey:
        description:
            - Authentication key
        required: false
        default: null
        choices: []
        aliases: [] 
    reliable:
        description:
            - Whether the key is a trusted key.
        required: false
        default: false
        choices: ['true', 'false']
        aliases: []
    ipadd:
        description:
            - Remote IPv4 or IPv6 address
        required: false
        default: null
        choices: []
        aliases: []
    addrtype:
        description:
            - Address type
        required: ipv4
        default: null
        choices: ['ipv4', 'ipv6']
        aliases: []
    del_rel_alone:
        description:
            - Whether delete trusted key alone
        required: false
        default: null
        choices: ['true', 'false']
        aliases: []
    del_auth_all:
        description:
            - Whether delete all trusted key configurations
        required: false
        default: null
        choices: ['true', 'false']
        aliases: []
    hostmode:
        description:
            - Client mode
        required: false
        default: null
        choices: ['symactive', 'client']
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

# configure NTP authentication 
- comware_ntp: service=ntp keyid=42 authmode=md5 authkey=anicekey reliable=true username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
# configure NTP reference clock
- comware_ntp: stratum=2 username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
# configure NTP client
- comware_ntp: service=ntp keyid=42 hostmode=client ipadd=10.1.1.1 name=hun1/2/2 username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
# delete trusted keys alone
- comware_ntp: state=absent del_rel_alone=true service=ntp keyid=42 reliable=false  username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
# delete all verfication keys
- comware_ntp: state=absent service=ntp keyid=42 del_auth_all=true  username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
"""

import socket
import re
try:
    HAS_PYHP = True
    from pyhpecw7.comware import HPCOM7
    from pyhpecw7.features.interface import Interface
    from pyhpecw7.features.errors import *
    from pyhpecw7.errors import *
    from pyhpecw7.features.ntp import Ntp
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
            name=dict(required=False),
            ntpenable=dict(choices=['true', 'false'],),
            ntpauthenable=dict(choices=['true', 'false'],),
            state=dict(choices=['present', 'absent'],
                       default='present'),
            stratum=dict(type='str'),
            service=dict(choices=['ntp', 'sntp']),
            keyid=dict(type='str'),
            authmode=dict(choices=['md5', 'hmac_sha_1', 'hmac_sha_256', 'hmac_sha_384', 'hmac_sha_384']),
            authkey=dict(type='str'),
            reliable=dict(choices=['true', 'false'],
                       default='false'),
            ipadd=dict(type='str'),
            addrtype=dict(choices=['ipv4', 'ipv6'],
                          default='ipv4'),
            del_rel_alone=dict(choices=['true', 'false']),
            del_auth_all=dict(choices=['true', 'false']),
            hostmode=dict(choices=['symactive', 'client']),
            hostname=dict(required=True),
            username=dict(required=True),
            password=dict(required=False, default=None),
            port=dict(type='int', default=830),
            look_for_keys=dict(default=False, type='bool')
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
                    password=password, port=port)

    state = module.params['state']
    name = module.params['name']
    ntpenable = str(module.params['ntpenable'])
    ntpauthenable= module.params['ntpauthenable']
    stratum =  module.params['stratum']
    service=module.params['service']
    keyid = str(module.params['keyid'])
    authmode = module.params['authmode']
    authkey = module.params['authkey']
    reliable = module.params['reliable']
    ipadd = str(module.params['ipadd'])
    addrtype = module.params['addrtype']
    hostmode = module.params['hostmode']
    del_rel_alone = module.params['del_rel_alone']
    del_auth_all = module.params['del_auth_all']
    changed = False

    proposed = dict((k, v) for k, v in module.params.items()
                    if v is not None and k not in filtered_keys)

    try:
        look_for_keys = module.params['look_for_keys']
        device.open(look_for_keys=look_for_keys)
    except ConnectionError as e:
        safe_fail(module, device, msg=str(e),
                  descr='Error opening connection to device.')

    
    if module.params.get('name'):
        name = module.params.get('name')
        try:
            interface = Interface(device, name)
            name_exist =True
        except PYHPError as e:
            safe_fail(module,
                      device,
                      descr='There was problem recognizing that interface.',
                      msg=str(e))
        if name_exist:
            is_ethernet, is_routed = interface._is_ethernet_is_routed()
            if is_ethernet:
                module.fail_json(msg='The interface mode must be routing.'
                                     '\nPlease configure type first by itself,'
                                     '\nthen run again.')                
    else:
        name = ''
        try:
            interface = Interface(device, name)
        except PYHPError as e:
            safe_fail(module,
                      device,
                      descr='There was problem recognizing that interface.',
                      msg=str(e))
    if state =='present':
        if module.params.get('ipadd'):
            ipadd = module.params.get('ipadd')
            if not module.params.get('service') or not module.params.get('hostmode')\
                        or not module.params.get('keyid'):
                module.fail_json(msg='The \'ipadd\' parameter must be compatible with:'
                                     '\nservice, hostmode, keyid.'
                                     '\nPlease configure type first by itself,'
                                     '\nthen run again.')
        if module.params.get('authmode'):
            authmode = module.params.get('authmode')
            if not module.params.get('service') or not module.params.get('keyid')\
                        or not module.params.get('authkey') or not module.params.get('reliable'):
                module.fail_json(msg='The \'authmode\' parameter must be compatible with:'
                                     '\nservice, hostmode, keyid, reliable.'
                                     '\nPlease configure type first by itself,'
                                     '\nthen run again.')
        if module.params.get('stratum'):
            stratum = module.params.get('stratum')
            int_stratum = int(stratum)
            if int_stratum >15 or int_stratum <1:
                module.fail_json(msg='The value range of parameter \'stratum\' must be 1 to 15.'
                                     '\nPlease reconfigure,'
                                     '\nthen run again.') 
    if state =='absent':
        if module.params.get('ipadd'):
            ipadd = module.params.get('ipadd')
            if not module.params.get('service') or not module.params.get('hostmode'):
                module.fail_json(msg='The \'ipadd\' parameter must be compatible with:'
                                     '\nservice, hostmode.'
                                     '\nPlease configure type first by itself,'
                                     '\nthen run again.')
        if del_auth_all == 'true':
            if not module.params.get('service') or not module.params.get('keyid'):
                module.fail_json(msg='The \'del_auth_all\' parameter must be compatible with:'
                                     '\nservice, keyid.'
                                     '\nPlease configure type first by itself,'
                                     '\nthen run again.')
        if del_rel_alone == 'true':
            if not module.params.get('service') or not module.params.get('keyid'):
                module.fail_json(msg='The \'del_rel_alone\' parameter must be compatible with:'
                                     '\nservice, keyid.'
                                     '\nPlease configure type first by itself,'
                                     '\nthen run again.')        
  
    ntp = Ntp(device,name)

    if state == 'present':
        if ntpenable == 'true' or ntpauthenable == 'true':
            ntp.enable_ntp(stage = True, ntpenable=ntpenable,ntpauthenable=ntpauthenable)
        if module.params.get('stratum'):
            ntp.comfigue_refclock_master(stage = True, stratum=stratum)
        if module.params.get('ipadd'):
            args = dict(service = str(module.params.get('service')), addrtype=str(module.params.get('addrtype')), hostmode=str(module.params.get('hostmode')))
            ntp.confiure_ntp_client(stage=True, ipadd=ipadd, keyid=keyid, **args)
        if module.params.get('authmode'):
            args = dict(service = str(module.params.get('service')), authmode=str(module.params.get('authmode')))
            ntp.create_authentication(stage=True, keyid=keyid, authkey=authkey, reliable=reliable, **args)
    if state == 'absent':
        if ntpenable == 'false' or ntpauthenable == 'false':
            ntp.enable_ntp(stage = True, ntpenable=ntpenable,ntpauthenable=ntpauthenable)
        if module.params.get('stratum'):
            ntp.remove_refclock_master(stage = True)
        if module.params.get('ipadd'):
            args = dict(service = str(module.params.get('service')), addrtype=str(module.params.get('addrtype')), hostmode=str(module.params.get('hostmode')))
            ntp.remove_ntp_client(stage=True, ipadd=ipadd, **args)
        if del_auth_all == 'true':
            args = dict(service = str(module.params.get('service')))
            ntp.remove_authentication(stage=True, keyid=keyid, **args)   
        if del_rel_alone == 'true' and reliable == 'false':
            args = dict(service = str(module.params.get('service')))
            ntp.remove_auth_reliable(stage=True, keyid=keyid, reliable=reliable, **args)
    existing = True
    commands = None
    end_state = True

    if device.staged:
        commands = device.staged_to_string()
        if module.check_mode:
            safe_exit(module, device, changed=True,
                      commands=commands)
        else:
            try:
                device.execute_staged()
                #end_state = interface.get_config()
            except PYHPError as e:
                safe_fail(module, device, msg=str(e),
                          descr='Error on device execution.')
            changed = True

    results = {}
    results['proposed'] = proposed
    results['existing'] = existing
    results['state'] = state
    results['commands'] = commands
    results['changed'] = changed
    results['end_state'] = end_state

    safe_exit(module, device, **results)

from ansible.module_utils.basic import *
main()
