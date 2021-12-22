#!/usr/bin/python

DOCUMENTATION = """
---

module: comware_irf_ports
short_description: Manage IRF port creation and removal for Comware v7 devices
description:
    - Manage IRF port creation and removal for Comware v7 devices
version_added: 1.8
category: Feature (RW)
notes:
    - This module is meant to be run after the comware_irf_members module.
    - The process is as follows 1) Use comware_irf_members to change
      the IRF member identity of the device, with the reboot=true
      flag, or reboot the device through some other means. 2) Use
      comware_irf_members to change priority, description, and domain,
      if desired. 3) Use the comware_irf_ports module to create IRF port
      to physical port bindings, and set activate=true to activate the
      IRF. If IRF neighbors are already configured, the IRF will be
      formed, some devices may reboot.
    - Any physical interfaces not in an interface list (irf_p1 or irf_p2) will
      be removed from the IRF port. An empty list removes all interfaces.
    - If an IRF is succesfully created, the non-master members will no longer
      be accessible through their management interfaces.
options:
    member_id:
        description:
            - IRF member id for switch (must be unique).
              IRF member ids can be configured with the comware_irf_members module.
        required: true
        default: null
        choices: []
        aliases: []
    irf_p1:
        description:
            - Physical Interface or List of Physical Interfaces that will be
              bound to IRF port 1. Any physical interfaces not in the list will
              be removed from the IRF port. An empty list removes all interfaces.
        required: true
        default: null
        choices: []
        aliases: []
    irf_p2:
        description:
            - Physical Interface or List of Physical Interfaces that will be
              bound to IRF port 2. Any physical interfaces not in the list will
              be removed from the IRF port. An empty list removes all interfaces.
        required: true
        default: null
        choices: []
        aliases: []
    filename:
        description:
            - Where to save the current configuration. Default is startup.cfg.
        required: false
        default: startup.cfg
        choices: []
        aliases: []
    activate:
        description:
            - activate the IRF after the configuration is initially performed
        required: false
        default: true
        choices: ['true', 'false', 'yes', 'no']
        aliases: []
    removal_override:
        description:
            - When set to true, allows the removal of physical ports from IRF port(s).
              Removing physical ports may have adverse effects and be disallowed by the switch.
              Disconnecting all IRF ports could lead to a split-brain scenario.
        required: false
        default: false
        choices: ['true', 'false', 'yes', 'no']
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

   # irf ports
   - comware_irf_ports:
      member_id: 1
      irf_p1:
        - FortyGigE1/0/1
        - FortyGigE1/0/3
      irf_p2: FortyGigE1/0/2
      username: "{{ username }}"
      password: "{{ password }}"
      hostname: "{{ inventory_hostname }}"
      removal_override: yes

"""
import socket

try:
    HAS_PYHP = True
    from pyhpecw7.comware import HPCOM7
    from pyhpecw7.features.irf import *
    from pyhpecw7.features.interface import Interface
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
            irf_p1=dict(required=True, type='list'),
            irf_p2=dict(required=True, type='list'),
            filename=dict(default='startup.cfg'),
            activate=dict(type='bool',
                          choices=BOOLEANS,
                          default='true'),
            removal_override=dict(type='bool',
                                  choices=BOOLEANS,
                                  default='false'),
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
                     'port', 'CHECKMODE', 'member_id', 'look_for_keys')

    hostname = socket.gethostbyname(module.params['hostname'])
    username = module.params['username']
    password = module.params['password']
    port = module.params['port']

    device = HPCOM7(host=hostname, username=username,
                    password=password, port=port)

    member_id = module.params.get('member_id')
    changed = False

    try:
        look_for_keys = module.params['look_for_keys']
        device.open(look_for_keys=look_for_keys)
    except ConnectionError as e:
        safe_fail(module, device, msg=str(e),
                  descr='Error opening connection to device.')

    try:
        irf_mem = IrfMember(device)
        irf_mem.get_config(member_id)
    except PYHPError as e:
        module.fail_json(msg=str(e))

    try:
        irf_ports = IrfPort(device)
        existing_full = irf_ports.get_config()
    except PYHPError as e:
        safe_fail(module, device, msg=str(e),
                  descr='Error getting current configuration.')

    existing = existing_full.get(member_id, {})

    proposed = dict((k, v) for k, v in module.params.items()
                    if v is not None and k not in filtered_keys)

    irf_p1 = proposed.get('irf_p1')
    if isinstance(irf_p1, str):
        irf_p1 = [irf_p1]

    if not irf_p1:
        irf_p1 = []

    irf_p2 = proposed.get('irf_p2')
    if isinstance(irf_p2, str):
        irf_p2 = [irf_p2]

    if not irf_p2:
        irf_p2 = []

    try:
        irf_p1 = convert_iface_list(device, irf_p1)
        irf_p2 = convert_iface_list(device, irf_p2)
    except PYHPError as ie:
        safe_fail(module, device, msg=str(ie),
                  descr='Error recognizing physical interface.')

    old_p1 = existing.get('irf_p1', [])
    old_p2 = existing.get('irf_p2', [])
    filename = proposed.pop('filename')
    activate = proposed.pop('activate')
    delta = False

    if set(irf_p1) != set(old_p1):
        delta = True

    if set(irf_p2) != set(old_p2):
        delta = True

    removal_list = []
    for item in old_p1:
        if item not in irf_p1:
            removal_list.append(item)

    for item in old_p2:
        if item not in irf_p2:
            removal_list.append(item)

    removal_override = proposed.get('removal_override')

    if removal_list and not removal_override:
        safe_fail(module, device, msg='You are trying to remove interfaces ' +
                  '{0}\n'.format(removal_list) +
                  'Removal may have adverse effects.\n' +
                  'Set removal_override=true to override.')

    if delta:
        try:
            irf_ports.build(member_id,
                            old_p1=old_p1,
                            old_p2=old_p2,
                            irf_p1=irf_p1,
                            irf_p2=irf_p2,
                            filename=filename,
                            activate=activate)
        except PYHPError as e:
            safe_fail(module, device, msg=str(e),
                      descr='Error preparing IRF port config.')

    commands = None
    end_state = existing

    results = {}
    results['proposed'] = proposed
    results['existing'] = existing
    results['commands'] = commands
    results['changed'] = changed
    results['end_state'] = end_state

    if device.staged:
        commands = device.staged_to_string()
        if module.check_mode:
            safe_exit(module, device, changed=True,
                      commands=commands)
        else:
            try:
                device.execute_staged()
                end_state = irf_ports.get_config()
                changed = True
                results['changed'] = changed
                results['end_state'] = end_state
            except PYHPError as e:
                if isinstance(e, NCTimeoutError)\
                        or isinstance(e, ConnectionClosedError):
                    changed = True
                    results['changed'] = changed
                    module.exit_json(**results)
                else:
                    safe_fail(module, device, msg=str(e),
                              descr='Error executing commands.'
                              + 'Please make sure member id is correct.')

    safe_exit(module, device, **results)

from ansible.module_utils.basic import *
main()
