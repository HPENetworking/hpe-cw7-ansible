"""Manage L2VPN on HPCOM7 devices.
"""

from pyhpecw7.utils.xml.lib import *


class L2VPN(object):
    """Enable/Disable L2VPN globally on a HP Comware 7 switch.

    Args:
        device (HPCOM7): connected instance of a ``pyhpecw7.comware.HPCOM7``
            object.

    Attributes:
        device (HPCOM7): connected instance of a ``pyhpecw7.comware.HPCOM7``
            object.

    """
    def __init__(self, device):
        self.device = device

    def get_config(self):
        """Get current L2VPN global configuration state.
        """
        KEYMAP = {
            'enable': 'Enable',
            'vsi_supported': 'SupportVsiInterface'
        }

        VALUE_MAP = {
            'Enable': {
                'true': 'enabled',
                'false': 'disabled'
            }
        }

        E = data_element_maker()
        top = E.top(
            E.L2VPN(
                E.Base()
            )
        )

        nc_get_reply = self.device.get(('subtree', top))
        return_l2vpn = data_elem_to_dict(nc_get_reply.data_ele, KEYMAP, value_map=VALUE_MAP)

        return return_l2vpn.get('enable')

    def enable(self, stage=False):
        """Stage or execute a config object to enable L2VPN

        Args:
            stage (bool): whether to stage the commands or execute
                immediately

        Returns:
            True if stage=True and successfully staged
            etree.Element XML response if immediate execution
        """
        config = self._build_config(state='enabled')
        if stage:
            return self.device.stage_config(config, 'edit_config')
        else:
            return self.device.edit_config(config)

    def disable(self, stage=False):
        """Stage or execute a config object to disable L2VPN

        Args:
            stage (bool): whether to stage the commands or execute
                immediately

        Returns:
            True if stage=True and successfully staged
            etree.Element XML response if immediate execution
        """
        config = self._build_config(state='disabled')
        if stage:
            return self.device.stage_config(config, 'edit_config')
        else:
            return self.device.edit_config(config)

    def _build_config(self, state):
        """Build config object to configure L2VPN global features

        Args:
            state (str): must be "enabled" or "disabled" and is the desired
                state of the L2VPN global feature

        Returns:
            etree.Element config object to configure L2VPN global features
        """
        if state == 'enabled':
            value = 'true'
        elif state == 'disabled':
            value = 'false'

        EN = nc_element_maker()
        EC = config_element_maker()

        config = EN.config(
            EC.top(
                EC.L2VPN(
                    EC.Base(
                        EC.Enable(value),
                        **operation_kwarg('merge')
                    )
                )
            )
        )

        return config

    def config(self,stage=False):
        commands = []
        commands.append('l2vpn enable')

        if commands:
            commands.append('\n')
            if stage:
                self.device.stage_config(commands, 'cli_config')
            else:
                self.device.cli_config(commands)