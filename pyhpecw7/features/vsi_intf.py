"""Manage VXLAN configurations on HPCOM7 devices.
"""
import re
from lxml import etree
from pyhpecw7.utils.xml.lib import *
from pyhpecw7.utils.templates import cli
from pyhpecw7.features.interface import Interface
from pyhpecw7.features.errors import MacaddrFormatError,MacaddrParamsError


class Vsi(object):
    """This class is used to config vsi
    """
    def __init__(self, device, interface):

        self.device = device
        self.interface = interface
        self.intf_command = 'interface {0}'.format(interface)

    def get_config(self):
        pass

    def get_vpn_config(self):
        existing_vpn = []
        config = self.device.cli_display('display current-configuration | include vpn-instance')
        vpn_config = config.split('\r\n')
        for line in vpn_config[1:]:
            if len(line) > 2:
                vpn = line.split('vpn-instance')[1].strip(' ')
                existing_vpn.append(vpn)
        return existing_vpn

    def build(self, stage=False, **kvargs):
        """Stage or execute config object to create/update tunnel

        Args:
            stage (bool): whether to stage the command or execute immediately

        Returns:
            True if stage=True and successfully staged
            CLI response strings if immediate execution
        """
        return self._build_config(state='present', stage=stage, **kvargs)

    def remove(self, stage=False, **kvargs):
        """Build config object to remove tunnel interface

        Args:
            stage (bool): whether to stage the command or execute immediately

        Returns:
            True if stage=True and successfully staged
            CLI response strings if immediate execution
        """
        return self._build_config(state='default', stage=stage, **kvargs)

    def _build_config(self, state, stage=False, **kvargs):
        """Build CLI commands to configure/create VXLAN tunnel interfaces

        Args:
            state (str): must be "absent" or "present"
            kvargs: see Keyword Args
            stage (bool): whether to stage the command or execute immediately

        Keyword Args:
            src (str): OPTIONAL - source IP addr of tunnel
            dest (str): OPTIONAL - destination IP addr of tunnel
            global_src (str): OPTIONAL - global src IP addr for tunnels

        Returns:
            True if stage=True and successfully staged
            CLI response strings if immediate execution
        """
        commands = []
        if state == 'default':
            commands.append(('undo interface {0}').format(self.interface))
        elif state == 'present':
            CMDS = {
                'binding':'ip binding vpn-instance {0}',
                'macaddr':'mac-address {0}',
                'local_proxy':'local-proxy-{0} enable',
                'distribute_gateway':'distributed-gateway {0}',
            }
            binding = kvargs.get('binding')
            macaddr = kvargs.get('macaddr')
            local_proxy = kvargs.get('local_proxy')
            distribute_gateway = kvargs.get('distribute_gateway')

            if binding:
                commands.append((CMDS.get('binding')).format(binding))
            if macaddr:
                commands.append((CMDS.get('macaddr')).format(macaddr))
            if local_proxy:
                commands.append((CMDS.get('local_proxy')).format(local_proxy))
            if distribute_gateway:
                commands.append((CMDS.get('distribute_gateway')).format(distribute_gateway))
        if commands:
            commands.insert(0, self.intf_command)
            commands.append('\n')
            if stage:
                self.device.stage_config(commands, 'cli_config')
            else:
                self.device.cli_config(commands)

    def param_check(self, **params):
        """Checks given parameters
        """
        macaddr = params.get('macaddr')
        if macaddr:
            res_mac = re.search(r'-',macaddr)
            if not res_mac:
                raise MacaddrFormatError(macaddr)

            mac_num = re.sub('-','',macaddr)
            for num in mac_num:
                patten = '^[\d|A-F|a-f]*$'
                res = re.search(patten, num)
                if not res:
                    raise MacaddrParamsError(macaddr)

