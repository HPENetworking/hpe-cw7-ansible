"""Manage VXLAN configurations on HPCOM7 devices.
"""
import re
from lxml import etree
from pyhpecw7.utils.xml.lib import *
from pyhpecw7.utils.templates import cli
from pyhpecw7.features.interface import Interface


class Vsi(object):
    """This class is used to config vsi
    """
    def __init__(self, device, vsi):

        self.device = device
        self.vsi = vsi

    def get_config(self):
        """Get running config for a tunnel interface

        Returns:
            A dictionary is returned with the following k/v pairs:
                src (str): source IP addr of tunnel
                dest (str): destination IP addr of tunnel
                mode (str): mode of tunnel

            If the tunnel does not exist, an empty dictionary is returned.

        """
        existing = []
        config = self.device.cli_display('display current-configuration | include vsi')
        vsi_config = config.split('\r\n')
        for line in vsi_config[1:]:
            if re.search(r'^vsi',line):
                vsi_name = line.split('vsi')[-1]
                existing.append(vsi_name)
        return existing

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
            commands.append(('undo vsi {0}').format(kvargs.get('vsi')))
        elif state == 'present':
            CMDS = {
                'gateway_intf':'gateway {0}',
                'gateway_subnet':'gateway subnet {0} {1}',
                'vxlan':'vxlan {0}',
                'encap':'evpn encapsulation vxlan',
                'rd':'route-distinguisher {0}',
                'vpn_target_auto':'vpn-target auto {0}',
            }
            gateway_intf = kvargs.get('gateway_intf')
            gateway_subnet = kvargs.get('gateway_subnet')
            gateway_mask = kvargs.get('gateway_mask')
            vxlan = kvargs.get('vxlan')
            encap = kvargs.get('encap')
            rd = kvargs.get('rd')
            vpn_target_auto = kvargs.get('vpn_target_auto')
            if gateway_intf:
                commands.append((CMDS.get('gateway_intf')).format(gateway_intf))
            if gateway_subnet:
                commands.append((CMDS.get('gateway_subnet')).format(gateway_subnet,gateway_mask))
            if vxlan:
                commands.append((CMDS.get('vxlan')).format(vxlan))
            if encap == 'true':
                commands.append(CMDS.get('encap'))
            if rd:
                commands.append((CMDS.get('rd')).format(rd))
            if vpn_target_auto:
                commands.append((CMDS.get('vpn_target_auto')).format(vpn_target_auto))

        if commands:
            commands.insert(0, 'vsi '+self.vsi)
            commands.append('\n')
            if stage:
                self.device.stage_config(commands, 'cli_config')
            else:
                self.device.cli_config(commands)

    def param_check(self, **params):
        """Checks given parameters
        """
        vxlan = params.get('vxlan')
        if vxlan:
            if int(vxlan) < 0 or int(vxlan) > 16777215:
                raise VsiParamsError(vxlan)