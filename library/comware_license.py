#!/usr/bin/python

DOCUMENTATION = """
---

module: comware_license
short_description: loading device license
description:
    - loading device license
version_added: 1.8
category: Feature (RW)
author: null
notes:
    - 
options:
    license:
        description:
            - the license file for the device
        required: True
        default: null
        choices: []
        aliases: []
    slot:
        description:
            - device slot number which the license loading.
        required: false
        default: null
        choices: []
        aliases: []
    license_chk:
        description:
            - check the license 
        required: false
        default: true
        choices: ['true','false']
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

# e.g.
- comware_license: license=210235A1U6H1840000012020012114082102563.ak slot=1 username={{ username }} password={{ password }} hostname={{ inventory_hostname }} 
"""

import socket

try:
    HAS_PYHP = True
    from pyhpecw7.comware import HPCOM7
    from pyhpecw7.features.license import License
    from pyhpecw7.features.errors import InterfaceError
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
            license=dict(required=True,type='str'),
            slot=dict(type='str'),
            license_chk=dict(choices=['true', 'false'],
                       default='true'),
            state=dict(choices=['present', 'default'],
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
                    password=password, port=port)
    state = module.params['state']
    license = module.params.get('license')
    license_chk = module.params.get('license_chk')
    changed = False
    proposed = dict((k, v) for k, v in module.params.items()
                    if v is not None and k not in filtered_keys)

    try:
        look_for_keys = module.params['look_for_keys']
        device.open(look_for_keys=look_for_keys)
    except ConnectionError as e:
        safe_fail(module, device, msg=str(e),
                  descr='Error opening connection to device.')

    if not module.params.get('slot'):
        safe_fail(module,msg='please assign slot number for loading license file')

    try:
        licenses = License(device,)
    except PYHPError as e:
        safe_fail(module,device,descr='there is problem in setting the device license',
                  msg=str(e))
    try:
        existing = licenses.get_config()
    except PYHPError as e:
        safe_fail(module, device, msg=str(e),
                  descr='Error getting existing config.')

    if state == 'present':
        if not existing:
            licenses.build(stage=True, **proposed)
        else:
            license_file = existing.get('license').split('/license/')[1]
            license_state = existing.get('license_state')
            if license_file == license and license_state == 'in use':
                pass
            else:
                licenses.build(stage=True, **proposed)
        if license_chk:
            current_license = licenses.get_config()
            if not current_license:
                safe_fail(module,msg='Invalid activation license file.')
            if current_license.get('license').split('/license/')[1] != license or \
                    current_license.get('license_state').lower() != 'in use' :
                safe_fail(module,msg='license is invalid')
    # elif state == 'default':
    #     licenses.default(stage=True, **proposed)

    commands = None
    end_state = existing

    if device.staged:
        commands = device.staged_to_string()
        if module.check_mode:
            safe_exit(module, device, changed=True,
                      commands=commands)
        else:
            try:
                device.execute_staged()
                end_state = licenses.get_config()
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
