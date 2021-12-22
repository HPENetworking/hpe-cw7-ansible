#!/usr/bin/python

DOCUMENTATION = """
---

module: comware_irf_members
short_description: Manage IRF membership configuration
description:
    - Manage IRF member configuration.
version_added: 1.8
category: Feature (RW)
notes:
    - This module should be used before the comware_irf_ports module.
    - The process is as follows 1) Use comware_irf_members to change
      the IRF member identity of the device, with the reboot=true
      flag, or reboot the device through some other means. 2) Use
      comware_irf_members to change priority, description, and domain,
      if desired. 3) Use the comware_irf_ports module to create IRF port
      to physical port bindings, and set activate=true to activate the
      IRF. If IRF neighbors are already configured, the IRF will be
      formed, some devices may reboot.
    - When state=absent, the interfaces in mad_exclude will be removed if present.
      Other parameters will be ignored.
options:
    member_id:
        description:
            - Current IRF member ID of the switch.
              If the switch has not been configured for IRF yet,
              this should be 1.
        required: true
        default: null
        choices: []
        aliases: []
    new_member_id:
        description:
            - The desired IRF member ID for the switch.
              The new member ID takes effect after a reboot.
        required: false
        default: null
        choices: []
        aliases: []
    auto_update:
        description:
            - Whether software autoupdate should be enabled for the fabric.
        required: false
        default: null
        choices: ['enable', 'disable']
        aliases: []
    domain_id:
        description:
            - The domain ID for the IRF fabric.
        required: false
        default: null
        choices: []
        aliases: []
    mad_exclude:
        description:
            - Interface or list of interfaces
              that should be excluded from shutting down
              in a recovery event.
        required: false
        default: null
        choices: []
        aliases: []
    priority:
        description:
            - The desired IRF priority for the switch.
        required: false
        default: null
        choices: []
        aliases: []
    descr:
        description:
            - The text description of the IRF member switch.
        required: false
        default: false
        choices: []
        aliases: []
    reboot:
        description:
            - Whether to reboot the switch after member id changes are made.
        required: true
        default: false
        choices: [true, false, yes, no]
        aliases: []
    state:
        description:
            - Desired state of the interfaces listed in mad_exclude
        required: false
        default: 'present'
        choices: ['present', 'absent']
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

  # irf members
  - comware_irf_members:
      member_id: 9
      state: present
      auto_update: disable
      mad_exclude:
        - FortyGigE9/0/30
        - FortyGigE9/0/23
        - FortyGigE9/0/24
      priority: 4
      descr: My description
      reboot: no
      username: "{{ username }}"
      password: "{{ password }}"
      hostname: "{{ inventory_hostname }}"

"""

import socket
from ncclient.operations.errors import TimeoutExpiredError

try:
    HAS_PYHP = True
    from pyhpecw7.comware import HPCOM7
    from pyhpecw7.features.irf import IrfMember
    from pyhpecw7.features.interface import Interface
    from pyhpecw7.features.reboot import Reboot
    from pyhpecw7.features.errors import *
    from pyhpecw7.errors import *
except ImportError as ie:
    HAS_PYHP = False


def convert_iface_list(device, iface_list):
    converted_list = []
    for iface_name in iface_list:
        iface = Interface(device, iface_name)
        converted_list.append(iface.interface_name)

    return converted_list


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
            member_id=dict(type='str',
                           required=True),
            new_member_id=dict(type='str'),
            auto_update=dict(choices=['enable', 'disable']),
            domain_id=dict(type='str'),
            mad_exclude=dict(),
            priority=dict(type='str'),
            descr=dict(),
            reboot=dict(type='bool',
                        choices=BOOLEANS,
                        required=True),
            state=dict(choices=['present', 'absent'],
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
        module.fail_json(
            msg='There was a problem loading from the pyhpecw7comware module')

    filtered_keys = ('hostname', 'username', 'password',
                     'port', 'CHECKMODE', 'look_for_keys')

    hostname = socket.gethostbyname(module.params['hostname'])
    username = module.params['username']
    password = module.params['password']
    port = module.params['port']

    device = HPCOM7(host=hostname, username=username,
                    password=password, port=port)

    member_id = module.params.pop('member_id')
    reboot = module.params.pop('reboot')
    state = module.params.get('state')

    changed = False

    try:
        look_for_keys = module.params['look_for_keys']
        device.open(look_for_keys=look_for_keys)
    except ConnectionError as e:
        safe_fail(module, device, msg=str(e))

    try:
        irfm = IrfMember(device)
        existing = irfm.get_config(member_id)
    except PYHPError as e:
        if isinstance(e, IRFMemberDoesntExistError):
            new_member_id = module.params.get('new_member_id')
            try:
                if new_member_id:
                    member_id = new_member_id
                    irfm = IrfMember(device)
                    existing = irfm.get_config(member_id)
                else:
                    safe_fail(module, device, msg=str(e))
            except PYHPError as e:
                safe_fail(module, device, msg=str(e))
        else:
            safe_fail(module, device, msg=str(e))

    proposed = dict((k, v) for k, v in module.params.items()
                    if v is not None and k not in filtered_keys)

    mad_exclude = proposed.pop('mad_exclude', [])
    if isinstance(mad_exclude, str):
        mad_exclude = [mad_exclude]

    if mad_exclude:
        try:
            mad_exclude = convert_iface_list(device, mad_exclude)
        except InterfaceError as ie:
            module.fail_json(msg=str(ie))

    existing_mad_exclude = existing.pop('mad_exclude', [])
    mad_delta = list(set(mad_exclude).difference(
        existing_mad_exclude))

    delta = dict(set(proposed.items()).difference(
        existing.items()))

    proposed['mad_exclude'] = mad_exclude
    existing['mad_exclude'] = existing_mad_exclude

    if state == 'present':
        if delta or mad_delta:
            try:
                irfm.build(
					stage=True,
                    member_id=member_id, mad_exclude=mad_delta, **delta)
            except PYHPError as e:
                safe_fail(module, device, msg=str(e),
                          descr='There was an error preparing the'
                          + ' IRF membership configuration.')
    elif state == 'absent':
        remove_mad = list(set(mad_exclude).intersection(
            existing_mad_exclude))
        irfm.remove_mad_exclude(remove_mad)

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
                end_state = irfm.get_config(member_id)
            except PYHPError as e:
                safe_fail(module, device, msg=str(e))
            changed = True

    results = {}
    results['proposed'] = proposed
    results['existing'] = existing
    results['commands'] = commands
    results['changed'] = changed
    results['end_state'] = end_state
    results['state'] = state

    new_member_id = proposed.get('new_member_id')
    mem_id_changed = False
    if new_member_id:
        mem_id_changed = proposed.get('new_member_id') != member_id
    
    if reboot and mem_id_changed:
        try:
            my_reboot = Reboot(device)
            my_reboot.build(reboot=True)
            changed = True
            device.execute()
        except PYHPError as e:
            if isinstance(e, NCTimeoutError)\
                    or isinstance(e, ConnectionClosedError):
                module.exit_json(**results)
            else:
                safe_fail(module, device, msg=str(e))

    safe_exit(module, device, **results)

from ansible.module_utils.basic import *
main()
