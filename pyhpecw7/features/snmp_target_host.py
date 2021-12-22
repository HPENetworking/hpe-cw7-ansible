"""Manage interfaces on HPCOM7 devices.
"""

from pyhpecw7.utils.xml.lib import reverse_value_map
from pyhpecw7.features.errors import *
from pyhpecw7.features.errors import InterfaceCreateError, InterfaceTypeError,\
    InterfaceAbsentError, InterfaceParamsError, InterfaceVlanMustExist
from pyhpecw7.utils.xml.lib import *

class SnmpTargetHost(object):
    """This class is used to get data and configure a specific snmp target host.
    """
    def __init__(self, device, target_type=None, server_address=None, usm_user_name=None):
        self.device = device
        if usm_user_name:
            self.usm_user_name = usm_user_name
        if target_type:
            self.target_type = target_type
        if server_address:
            self.server_address = server_address

        # dictionary to XML tag mappings
        self.target_host_key_map = {
            'target_type': 'TargetType',
            'usm_user_name': 'SecurityName',
            'server_address': 'Address',
            'vpnname': 'VRF',
            'sercurity_model': 'SecurityMode',
            'security_level': 'SecurityLevel'
        }

        self.R_target_host_key_map = dict(reversed(item) for item in self.target_host_key_map.items())
        self.value_map = {
            'TargetType': {
                '1': 'inform',
                '2': 'trap'
                },
            'SecurityMode': {
                '1': 'v1',
                '2': 'v2c',
                '3': 'v3'
                },
            'SecurityLevel': {
                '1': 'NoAuthNoPriv',
                '2': 'authentication',
                '3': 'privacy'
                }
            }
        self.R_value_map = reverse_value_map(
            self.R_target_host_key_map, self.value_map)

    def gen_top(self):
        E = data_element_maker()
        top = E.SNMP(
            E.TargetHosts(
                E.UdpHost(
                )
            )
        )

        return top

    def get_group_list(self):
        """Get a list of Address that exist on the switch.

        Returns:
            It returns a list of Address as strings.
        """
        top = self.gen_top()
        nc_get_reply = self.device.get(('subtree', top))
        host_xml = findall_in_data('Address', nc_get_reply.data_ele)
        hosts = [host.text for host in host_xml]

        return hosts

    def get_config(self):
        """Gets current configuration for a given Security Name
        """
        top = self.gen_top()
        user_comm_ele = find_in_data('UdpHost', top)
        user_comm_ele.append(data_element_maker().SecurityName(self.usm_user_name))
        nc_get_reply = self.device.get(('subtree', top))
        snmp_target_host_config = data_elem_to_dict(nc_get_reply.data_ele, self.target_host_key_map, value_map=self.value_map)
        return snmp_target_host_config

    def target_host_build(self, stage=True, **targethost):

        targethost['usm_user_name'] = self.usm_user_name
        targethost['target_type'] = self.target_type
        targethost['server_address'] = self.server_address
        usm_user_name = targethost.get('usm_user_name')
        target_type = targethost.get('target_type')
        server_address = targethost.get('server_address')
        sercurity_model = targethost.get('sercurity_model')
        security_level = targethost.get('security_level')
        vpnname = targethost.get('vpnname')

        commands = []
        if vpnname:
            cmd ='snmp-agent target-host {0} address udp-domain {1} vpn-instance {2} params securityname {3}'.format(
                target_type, server_address, vpnname, usm_user_name)
            if sercurity_model:
                cmd = cmd + ' {0}'.format(sercurity_model)
                if sercurity_model == 'v3' and security_level != 'noAuthNoPriv':
                    cmd = cmd + ' {0}'.format(security_level)
            commands.append(cmd)
        else:
            cmd ='snmp-agent target-host {0} address udp-domain {1} params securityname {2}'.format(
                target_type, server_address, usm_user_name)
            if sercurity_model:
                cmd = cmd + ' {0}'.format(sercurity_model)
                if sercurity_model == 'v3' and security_level != 'noAuthNoPriv':
                    cmd = cmd + ' {0}'.format(security_level)
            commands.append(cmd)

        if commands:
            if stage:
                return self.device.stage_config(commands, 'cli_config')
            else:
                return self.device.cli_config(commands)

    def target_host_remove(self, stage=True, **targethost):

        targethost['usm_user_name'] = self.usm_user_name
        targethost['target_type'] = self.target_type
        targethost['server_address'] = self.server_address
        usm_user_name = targethost.get('usm_user_name')
        target_type = targethost.get('target_type')
        server_address = targethost.get('server_address')
        vpnname = targethost.get('vpnname')

        commands = []
        cmd = 'undo snmp-agent target-host {0} address udp-domain {1} params securityname {2}'.format(
            target_type, server_address, usm_user_name)
        if vpnname:
            cmd = cmd + ' vpn-instance {0}'.format(vpnname)
        commands.append(cmd)

        if commands:
            if stage:
                return self.device.stage_config(commands, 'cli_config')
            else:
                return self.device.cli_config(commands)



