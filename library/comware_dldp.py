#!/usr/bin/python

DOCUMENTATION = """
---

module: comware_dldp
short_description: Manage dldp authentication,interface,timeout and mode  on Comware 7 devices.
 author: gongqianyu                  
version_added: 1.0
category: Feature (RW)
notes:
    - To enable the dldp feature, the dldp feature must be enabled on both the global and the interface.
	- when config interface_enable,init_delay and port_shutdown,name must be exit.
options:
    global_enable:
        description:
            -  global dldp enable or disable
        required: False
        default: disable
        choices: [enable, disable]
        aliases: []
    auth_mode:
        description:
            -  Configure dldp authentication mode between current device and neighbor device.
        required: false
        default: null
        choices: [md5,none,simple]
        aliases: []     
    pwd_mode:
        description:
            -  Configure the dldp authentication password mode between the current device and the neighbor device.
        required: false
        default: null
        choices: [cipher, simple]
        aliases: []   
    pwd:
        description:
            -  Configure the dldp authentication password between the current device and the neighbor device
        required: false
        default: null
        choices: []
        aliases: []
  
    timeout:
        description:
            - Configure the sending interval of advertisement message(1~100)
        required: false
        default: 5
        choices: []
        aliases: []
    shutdown_mode:
        description:
            -  Global configuration of interface shutdown mode after dldp discovers unidirectional link.
        required: false
        default: auto
        choices: [auto ,hybrid ,manual]
        aliases: []
    name:
        description:
            -  The full name of the interface.
        required: false
        default: null
        choices: []
        aliases: []
    interface_enable:
        description:
            -  Enable dldp function on the interface.
        required: false
        default: null
        choices: [enable, disable]
        aliases: []
    init_delay:
        description:
            -  Delay time of dldp blocking interface from initial state to single pass state.(1~5)
        required: false
        default: null
        choices: []
        aliases: []

    port_shutdown:
        description:
            -  The interface shutdown mode after dldp discovers one-way link is configured on the interface.
        required: false
        default: null
        choices: [auto ,hybrid ,manual]
        aliases: [] 
    state:
        description:
            - Desired state for the interface configuration.
        required: false
        default: present
        choices: ['present', 'absent']
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
    look_for_keys:
        description:
            - Whether searching for discoverable private key files in ~/.ssh/
        required: false
        default: False
        choices: []
        aliases: []

"""

EXAMPLES = """

  - name: config dldp
        comware_dldp: global_enable=enable auth_mode=md5 shutdown_mode=auto pwd_mode=cipher pwd=123456 timeout=10 name=HundredGigE1/0/27 
                      interface_enable=disable state=present username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
  - name: delete dldp configuration
        comware_dldp: global_enable=enable auth_mode=md5 shutdown_mode=auto pwd_mode=cipher pwd=123456 timeout=10 name=HundredGigE1/0/27 
                      interface_enable=disable state=absent username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

"""

import socket
try:
    HAS_PYHP = True
    from pyhpecw7.features.dldp import Dldp
    from pyhpecw7.comware import HPCOM7
    from pyhpecw7.features.errors import *
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
            global_enable=dict(required=False,choices=['enable', 'disable']),
            auth_mode=dict(required=False, choices=['md5','none','simple']),
            pwd_mode=dict(required=False, choices=['cipher', 'simple']),
            pwd=dict(required=False),
            timeout=dict(required=False, default='5'),
            name=dict(required=False),
            interface_enable=dict(required=False, choices=['enable', 'disable']),
            init_delay=dict(required=False),
            shutdown_mode=dict(required=False, choices=['auto' ,'hybrid' ,'manual']),
            port_shutdown=dict(required=False, choices=['auto', 'hybrid', 'manual']),
            state=dict(choices=['present', 'absent'], default='present'),
            port=dict(default=830, type='int'),
            hostname=dict(required=True),
            username=dict(required=True),
            password=dict(required=False, default=None),
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
    global_enable = module.params['global_enable']
    auth_mode = module.params['auth_mode']
    pwd_mode = module.params['pwd_mode']
    pwd = module.params['pwd']
    timeout = module.params['timeout']
    name = module.params['name']
    interface_enable = module.params['interface_enable']
    init_delay = module.params['init_delay']
    shutdown_mode = module.params['shutdown_mode']
    port_shutdown = module.params['port_shutdown']
    state = module.params['state']
    args = dict(global_enable=global_enable, auth_mode=auth_mode, port_shutdown=port_shutdown, timeout=timeout, pwd_mode=pwd_mode, init_delay=init_delay, pwd=pwd, name=name, interface_enable=interface_enable, shutdown_mode=shutdown_mode)
    proposed = dict((k, v) for k, v in args.items() if v is not None)

    changed = False

    try:
        look_for_keys = module.params['look_for_keys']
        device.open(look_for_keys=look_for_keys)
    except ConnectionError as e:
        safe_fail(module, device, msg=str(e),
                  descr='error connecting to device')

    try:
        DLDP = Dldp(device, global_enable, auth_mode, timeout, pwd_mode, port_shutdown, init_delay, pwd, name, interface_enable, shutdown_mode)
    except PYHPError as e:
        safe_fail(module, device, msg=str(e))

    if state == 'present':
        DLDP.build(stage=True)
    elif state == 'absent':
        DLDP.remove(stage=True)

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
                          descr='error during execution')
            changed = True

    results = {}

    results['state'] = state
    results['commands'] = commands
    results['changed'] = changed
    results['proposed'] = proposed

    safe_exit(module, device, **results)

from ansible.module_utils.basic import *
main()
