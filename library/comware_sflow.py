#!/usr/bin/python


DOCUMENTATION = """
---

module: comware_sflow
short_description: Manage sflow attributes for Comware 7 devices
description:
    - Manage sflow attributes for Comware 7 devices
version_added: 1.0
category: Feature (RW)
options:
    collectorID:
        description:
            - the sflow collector id
        required: true
        default: null
        choices: []
        aliases: []
    addr:
        description:
            - the ipv4 or ipv6 address 
        required: true
        default: null
        choices: []
        aliases: []
    vpn:
        description:
            - Name to configure for the specified vpn-instance
        required: false
        default: null
        choices: []
        aliases: []
    descr:
        description:
            - Description for the collectorID.must be exit
        required: True
        default: CLI Collector
        choices: []
        aliases: []
    time_out:
        description:
            - the collector's parameter aging time
        required: false
        default: null
        choices: []
        aliases: []
    Port:
        description:
            -   UDP port
        required: false
        default: 6343
        choices: []
        aliases: []    
    data_size:
        description:
            - the sflow datagram max size
        required: false
        default: 1400
        choices: []
        aliases: []   
    agent_ip:
        description:
            - Configure the IP address of the sFlow agent.
        required: false
        default: null
        choices: []
        aliases: []     
    sourceIpv4IP:
        description:
            - Configure the source IPV4 address of the sFlow message.
        required: false
        default: null
        choices: []
        aliases: [] 
    sourceIpv6IP:
        description:
            - Configure the source IPV6 address of the sFlow message.
        required: false
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
    state:
        description:
            - Desired state of the vlan
        required: false
        default: present
        choices: ['present', 'absent']
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
# Basic  config
- comware_sflow: collectorID=1 vpn=1 addr=1.1.1.1 data_size=500 descr=netconf time_out=1200 username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

# delete config
- comware_sflow: collectorID=1 addr=1.1.1.1 state=absent username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

"""

import socket
try:
    HAS_PYHP = True
    from pyhpecw7.features.sflow import Sflow
    from pyhpecw7.features.sflow import SFlow
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
            collectorID=dict(required=False, type='str'),
            addr=dict(required=False),
            vpn=dict(required=False),
            descr=dict(required=False),
            data_size=dict(required=False),
            time_out=dict(required=False),
            sourceIpv4IP=dict(required=False),
            sourceIpv6IP=dict(required=False),
            agent_ip=dict(required=False),
            Port=dict(required=False),
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

    collectorID = module.params['collectorID']
    addr = module.params['addr']
    descr = module.params['descr']
    vpn = module.params['vpn']
    state = module.params['state']
    data_size = module.params['data_size']
    time_out = module.params['time_out']
    Port = module.params['Port']
    sourceIpv4IP = module.params['sourceIpv4IP']
    sourceIpv6IP = module.params['sourceIpv6IP']
    agent_ip = module.params['agent_ip']
    
    changed = False

    args = dict(collectorID=collectorID, addr=addr, descr=descr, vpn=vpn, time_out=time_out, data_size=data_size, Port=Port, sourceIpv4IP=sourceIpv4IP, sourceIpv6IP=sourceIpv6IP, agent_ip=agent_ip)
    proposed = dict((k, v) for k, v in args.items() if v is not None)

    results = {}
    results['proposed'] = proposed

    try:
        look_for_keys = module.params['look_for_keys']
        device.open(look_for_keys=look_for_keys)
    except ConnectionError as e:
        safe_fail(module, device, msg=str(e))

    try:
        if collectorID and (sourceIpv4IP or sourceIpv6IP or agent_ip):
            sflow = Sflow(device, collectorID)
            sFlow = SFlow(device, sourceIpv4IP, sourceIpv6IP, agent_ip)
        elif sourceIpv4IP or sourceIpv6IP or agent_ip and not collectorID:

            sFlow = SFlow(device, sourceIpv4IP, sourceIpv6IP, agent_ip)
        else:

            sflow = Sflow(device, collectorID)
            sflow.param_check(**proposed)
    except PYHPError as e:
        safe_fail(module, device, msg=str(e))

    try:
        if collectorID and (sourceIpv4IP or sourceIpv6IP or agent_ip) :
            existing = sflow.get_config()
            existing_1 = sFlow.get_config()
        elif sourceIpv4IP or sourceIpv6IP or agent_ip and not collectorID:

            existing_1 = sFlow.get_config()

        else:

            existing = sflow.get_config()

    except PYHPError as e:
        safe_fail(module, device, msg=str(e),
                  descr='error getting vlan config')
    sFlow = SFlow(device, sourceIpv4IP, sourceIpv6IP, agent_ip) 
    # sFlow.remove(stage=True)
    if collectorID and (sourceIpv4IP or sourceIpv6IP or agent_ip):
        end_state = existing

    if state == 'present':

        if collectorID and (sourceIpv4IP or sourceIpv6IP or agent_ip):


            delta = dict(set(proposed.items()).difference(existing.items()))
            delta_1 = dict(set(proposed.items()).difference(existing_1.items()))
            if delta:
                sflow.build(stage=True, **delta)
            if delta_1:
                sFlow.build(stage=True, **delta_1)

        elif sourceIpv4IP or sourceIpv6IP or agent_ip and not collectorID:
            if agent_ip:
                sFlow.debug(stage=True)
            delta_1 = dict(set(proposed.items()).difference(existing_1.items()))
            if delta_1:
                sFlow.build(stage=True, **delta_1)
            if delta_1:
                sFlow.build(stage=True, **delta_1)

        else:

            delta = dict(set(proposed.items()).difference(existing.items()))
            if delta:
                sflow.build(stage=True, **delta)

    elif state == 'absent':
        if sourceIpv4IP or sourceIpv6IP or agent_ip and not collectorID:
            sFlow.remove(stage=True)

        elif collectorID and (sourceIpv4IP or sourceIpv6IP or agent_ip):

            if existing:
                sflow.remove(stage=True)
            if existing_1:
                sFlow.remove(stage=True)
        else:

            if existing:
                sflow.remove(stage=True)


    if sourceIpv4IP or sourceIpv6IP or agent_ip and not collectorID:
        end_state_1 = existing_1

    commands = None

    if device.staged:

        commands = device.staged_to_string()
        if module.check_mode:
            device.close()
            safe_exit(module, device, changed=True,
                      commands=commands)
        else:
            try:
                device.execute_staged()

                if collectorID and (sourceIpv4IP or sourceIpv6IP or agent_ip):
                    end_state = sflow.get_config()
                    end_state_1 = sFlow.get_config()


                    results['existing'] = existing
                    results['end_state_1'] = end_state_1
                    results['existing_1'] = existing_1
                    results['end_state'] = end_state

                elif sourceIpv4IP or sourceIpv6IP or agent_ip and not collectorID:
                    end_state_1 = sFlow.get_config()

                    results['end_state_1'] = end_state_1

                else:

                    end_state = sflow.get_config()
                    results['end_state'] = end_state
            except PYHPError as e:
                safe_fail(module, device, msg=str(e),
                          descr='error during execution')
            changed = True




    results['state'] = state
    results['commands'] = commands
    results['changed'] = changed
    # if collectorID and (sourceIpv4IP or sourceIpv6IP or agent_ip):
    #     results['existing'] = existing
    #     results['end_state_1'] = end_state_1
    #     results['existing_1'] = existing_1
    # elif sourceIpv4IP or sourceIpv6IP or agent_ip and not collectorID:
    #     results['end_state_1'] = end_state_1
    # else:
    #     results['end_state'] = end_state
    safe_exit(module, device, **results)

from ansible.module_utils.basic import *
main()
