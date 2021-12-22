"""Manage interfaces on HPCOM7 devices.
"""
import re
from pyhpecw7.features.errors import BgpParamsError,InstanceParamsError,GroupParamsError,PeerParamsError,\
BgpMissParamsError
from pyhpecw7.features.interface import Interface
from pyhpecw7.utils.xml.lib import *


class Bgp(object):
    """This class is used to get and handle stp config
    """
    def __init__(self,device,bgp_as,instance=None):
        self.device = device
        self.bgp_as = bgp_as
        self.instance = instance

    def get_config(self):
        existing = []
        config = self.device.cli_display('display current-configuration | include bgp')
        bgp_info = config.split('\r\n')
        for line in bgp_info[1:]:
            if re.search(r'^bgp',line):
                bgp_name = line.split('bgp')[-1].strip(' ')
                existing.append(bgp_name)
        return existing

    def get_group_info(self,group):
        command = 'display current-configuration | include "group {0}"'.format(group)
        config = self.device.cli_display(command)
        group_info = config.split('\r\n')
        if len(group_info)>2:
            return True
        else:
            return False

    def remove_bgp(self, stage=False,**kvargs):
        commands = []
        bgp_as = kvargs.get('bgp_as')
        instance = kvargs.get('instance')
        if instance:
            commands.append('undo bgp {0} instance {1}'.format(bgp_as,instance))
        else:
            commands.append('undo bgp {0}'.format(bgp_as))
        commands.append('\n')
        if stage:
            return self.device.stage_config(commands, 'cli_config')
        else:
            return self.device.cli_config(commands)

    def build_bgp_group(self, stage=False, **kvargs):
        commands = []
        CMDS = {
            'bgp_as':'bgp {0}',
            'instance':'bgp {0} instance {1}',
            'group':'group {0}',
            'group_type':'group {0} {1}',
            'peer_connect_intf': 'peer {0} connect-interface {1}',
            'peer_in_group': 'peer {0} group {1}',
            'address_family': 'address-family {0}',
            'evpn': 'address-family {0} evpn',
            'policy_vpn_target_T': 'policy vpn-target',
            'policy_vpn_target_F': 'undo policy vpn-target',
            'reflect_client': 'peer {0} reflect-client',
            'peer_group_state': 'peer {0} enable',
        }
        bgp_as = kvargs.get('bgp_as')
        instance = kvargs.get('instance')
        group = kvargs.get('group')
        group_type = kvargs.get('group_type')
        peer = kvargs.get('peer')
        peer_connect_intf = kvargs.get('peer_connect_intf')
        peer_in_group = kvargs.get('peer_in_group')
        address_family = kvargs.get('address_family')
        evpn = kvargs.get('evpn')
        policy_vpn_target = kvargs.get('policy_vpn_target')
        reflect_client = kvargs.get('reflect_client')
        peer_group_state = kvargs.get('peer_group_state')

        if bgp_as and instance == None:
            commands.append((CMDS.get('bgp_as')).format(bgp_as))
        if bgp_as and instance:
            commands.append((CMDS.get('instance')).format(bgp_as,instance))
        if group and group_type == None:
            commands.append((CMDS.get('group')).format(group))
        if group and group_type:
            commands.append((CMDS.get('group_type')).format(group, group_type))
        if peer_connect_intf:
            commands.append((CMDS.get('peer_connect_intf')).format(peer, peer_connect_intf))
        if peer_in_group:
            commands.append((CMDS.get('peer_in_group')).format(peer, peer_in_group))
        if address_family and evpn == 'false':
            commands.append((CMDS.get('address_family')).format(address_family))
        if address_family and evpn == 'true':
            commands.append((CMDS.get('evpn')).format(address_family,evpn))
        if policy_vpn_target == 'enable':
            commands.append((CMDS.get('policy_vpn_target_T')))
        if policy_vpn_target == 'disable':
            commands.append((CMDS.get('policy_vpn_target_F')))
        if peer_group_state == 'true':
            commands.append((CMDS.get('peer_group_state')).format(peer))
        if reflect_client == 'true':
            commands.append((CMDS.get('reflect_client')).format(peer))
        commands.append('\n')

        if stage:
            return self.device.stage_config(commands, 'cli_config')
        else:
            return self.device.cli_config(commands)

    def param_check(self, **params):
        """Checks given parameters
        """
        bgp_as = params.get('bgp_as')
        instance = params.get('instance')
        group = params.get('group')
        peer = params.get('peer')
        peer_connect_intf = params.get('peer_connect_intf')
        evpn = params.get('evpn')
        address_family = params.get('address_family')

        if bgp_as:
            if int(bgp_as) < 1 or int(bgp_as) >4294967295:
                raise  BgpParamsError(bgp_as)

        if instance:
            if len(instance) > 31:
                raise InstanceParamsError(instance)

        if group:
            if len(group) > 47:
                raise GroupParamsError(group)

        if peer:
            if len(peer) > 47:
                raise PeerParamsError(peer)

        if peer_connect_intf:
            if peer == None:
                raise BgpMissParamsError(peer)

        if evpn == 'true':
            if address_family == None:
                raise BgpMissParamsError(address_family)