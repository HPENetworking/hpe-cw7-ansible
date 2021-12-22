#!/usr/bin/python


DOCUMENTATION = """
---

module: comware_vrrp
short_description: Manage VRRP configurations on a Comware v7 device
description:
    - Manage VRRP configurations on a Comware v7 device
author:hanyangyang
version_added: 1.0
category: Feature (RW)
notes:
    - When state is set to absent, the vrrp group for a specific
      interface will be removed (if it exists)
    - When state is set to shutdown, the vrrp group for a specific
      interface will be shutdown. undoshutdown reverses this operation
    - When sending a text password, the module is not idempotent
      because a hash is calculated on the switch. sending a cipher
      that matches the one configured is idempotent.
options:
    vrid:
        description:
            - VRRP group ID number
        required: true
        default: null
        choices: []
        aliases: []
    interface:
        description:
            - Full name of the Layer 3 interface
        required: true
        default: null
        choices: []
        aliases: []
    vip:
        description:
            - Virtual IP to assign within the group
        required: false
        default: null
        choices: []
        aliases: []
    priority:
        description:
            - VRRP priority for the device
        required: false
        default: null
        choices: []
        aliases: []
    preempt:
        description:
            - Determine preempt mode for the device
        required: false
        default: null
        choices: ['true', 'false']
        aliases: []
    auth_mode:
        description:
            - authentication mode for vrrp
        required: false
        default: null
        choices: ['simple', 'md5']
        aliases: []
    key_type:
        description:
            - Type of key, i.e. cipher or clear text
        required: false
        default: null
        choices: ['cipher', 'plain']
        aliases: []
    key:
        description:
            - cipher or clear text string
        required: false
        default: null
        choices: []
        aliases: []
    delay:
        description:
            - Configure preemption delay time
        required: false
        default: null
        choices: []
        aliases: []
    track:
        description:
            - Configure the track entry specified for monitoring.
        required: false
        default: null
        choices: []
        aliases: []
    switch:
        description:
            - when the status of the monitored track item changes to negative, 
              if the router is in backup status in the backup group, it will immediately switch to master router
        required: false
        default: null
        choices: []
        aliases: []
    state:
        description:
            - Desired state for the interface configuration
        required: false
        default: present
        choices: ['present', 'absent', 'shutdown', 'undoshutdown']
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

# ensure vrid and vrip are configured
- comware_vrrp: vrid=100 vip=100.100.100.1 interface=Vlan-interface100 username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

# ensure vrid 100 is shutdown
- comware_vrrp: vrid=100 interface=vlan100 state=shutdown username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

# simple auth w/  plain text key
- comware_vrrp: vrid=100 interface=vlan100 auth_mode=simple key_type=plain key=testkey username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

# md5 auth w/ cipher
- comware_vrrp: vrid=100 interface=vlan100 auth_mode=md5 key_type=cipher key='$c$3$d+Pc2DO3clxSA2tC6pe3UBzDEDl1dkE+voI=' username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

# ensure vrid 100 on vlan 100 is removed
- comware_vrrp: vrid=100 interface=vlan100 state=absent username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

# auth mode simple                                                                                                                                                                         
- comware_vrrp: vrid=100 vip=100.100.100.1 interface=HundredGigE1/0/27 auth_mode=simple key_type=cipher key=123456  username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

# vrrp delay track & switch                                                                                                                                                                       
- comware_vrrp: vrid=100 vip=100.100.100.1 interface=HundredGigE1/0/27 delay=20  track=1024 switch=10.10.10.1  username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
"""

import socket
try:
    HAS_PYHP = True
    from pyhpecw7.features.vrrp import VRRP
    from pyhpecw7.features.interface import Interface
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
            vrid=dict(required=True, type='str'),
            interface=dict(required=True),
            vip=dict(required=False),
            priority=dict(required=False, type='str'),
            auth_mode=dict(required=False, choices=['simple', 'md5']),
            key_type=dict(required=False, choices=['cipher', 'plain']),
            key=dict(required=False, type='str'),
            preempt=dict(required=False, choices=['yes', 'no']),
            delay=dict(required=False,type='str'),
            track=dict(required=False, type='str'),
            switch=dict(required=False),
            state=dict(choices=['present', 'absent', 'shutdown',
                                'undoshutdown'],
                       default='present'),
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

    vrid = module.params['vrid']
    interface = module.params['interface'].lower()
    vip = module.params['vip']
    priority = module.params['priority']
    preempt = module.params['preempt']
    auth_mode = module.params['auth_mode']
    key_type = module.params['key_type']
    key = module.params['key']
    delay = module.params['delay']
    track = module.params['track']
    switch = module.params['switch']

    if auth_mode:
        if not key_type or not key:
            module.fail_json(msg='params key_type and key are required')
    if key_type or key:
        if not auth_mode:
            module.fail_json(msg='auth_mode is required when setting auth')
    if delay:
        if int(delay) < 0 or int(delay) > 180000:
            safe_fail(module,msg='error delay time give')
    if track:
        if int(track) <1 or int(track) > 1024:
            safe_fail(module,msg='error track entry NUM give')
    if track:
        if not switch:
            module.fail_json(msg='params switch is requied')
    if switch:
        if not track:
            module.fail_json(msg='track is required when setting switch')

    state = module.params['state']

    changed = False

    args = dict(vrid=vrid, priority=priority, preempt=preempt,
                vip=vip, interface=interface, auth_mode=auth_mode,
                key_type=key_type, key=key, delay=delay, track=track,
                switch=switch)

    proposed = dict((k, v) for k, v in args.items() if v is not None)
    try:
        look_for_keys = module.params['look_for_keys']
        device.open(look_for_keys=look_for_keys)
    except ConnectionError as e:
        safe_fail(module, device, msg=str(e),
                  descr='error opening device conn')

    try:
        vrrp = VRRP(device, interface, vrid)
        vrrp_interface = Interface(device, interface)
    except PYHPError as e:
        safe_fail(module, device, msg=str(e))

    if not vrrp_interface.iface_exists:
        safe_fail(module, device, msg='interface does not exist.')
    is_eth, is_rtd = vrrp_interface._is_ethernet_is_routed()
    if not is_rtd:
        safe_fail(module, device,
                  msg='interface needs to be a layer 3 interface')

    try:
        existing = vrrp.get_config()
    except PYHPError as e:
        safe_fail(module, device, msg=str(e),
                  descr='could not get existing config')
    if state == 'present':
        delta = dict(set(proposed.items()).difference(
            existing.items()))
        if delta or auth_mode or \
                existing.get('admin') == 'down':
            delta['vrid'] = vrid
            if delta.get('key'):
                delta['auth_mode'] = auth_mode
                delta['key_type'] = key_type
            vrrp.build(stage=True, state=state, **delta)
    elif state == 'absent':
        if existing:
            vrrp.remove(stage=True)
    elif state == 'shutdown':
        if existing.get('admin') == 'Up':
            vrrp.shutdown(stage=True)
    elif state == 'undoshutdown':
        print(existing)
        raise IOError
        if existing.get('admin') == 'Down':
            vrrp.undoshutdown(stage=True)

    commands = None
    end_state = existing
    response = None

    if device.staged:
        commands = device.staged_to_string()
        if module.check_mode:
            device.close()
            safe_exit(module, device, changed=True,
                      commands=commands)
        else:
            try:
                response = device.execute_staged()
                end_state = vrrp.get_config()
            except PYHPError as e:
                safe_fail(module, device, msg=str(e),
                          descr='error during execution')
            changed = True

    results = {}
    results['proposed'] = proposed
    results['existing'] = existing
    results['state'] = state
    results['commands'] = commands
    results['changed'] = changed
    results['end_state'] = end_state
    results['response'] = response

    safe_exit(module, device, **results)

from ansible.module_utils.basic import *
main()
