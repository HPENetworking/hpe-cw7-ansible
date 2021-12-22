"""Manage IGMP on HPCOM7 devices.
author: liudongxue
"""

from pyhpecw7.utils.xml.lib import reverse_value_map
from pyhpecw7.features.errors import *
from pyhpecw7.features.errors import InterfaceCreateError, InterfaceTypeError,\
    InterfaceAbsentError, InterfaceParamsError, InterfaceVlanMustExist
from pyhpecw7.features.vlan import Vlan
from pyhpecw7.utils.xml.lib import *
from pyhpecw7.features.interface import Interface

class Igmp(object):
    """This class is used to build IGMP configurations on ``HPCOM7`` devices.

    Args:
        device (HPCOM7): connected instance of a
            ``phyp.comware.HPCOM7`` object.
        interface_name (str): The name of the interface.

    Attributes:
        device (HPCOM7): connected instance of a
            ``phyp.comware.HPCOM7`` object.
        interface_name (str): The name of the interface.
    """
    def __init__(self, device, interface_name):
        self._key_map = {
            'igstate': 'Enabled',
            'version': 'Version'
        }

        # used to map value values from our dictionary model
        # to expected XML tags and vice versa
        self._value_map = {
            'Enabled': {'true': 'enabled',
                        'false': 'disabled'},
            'Version': {'1': 'version1',
                        '2': 'version2',
                        '3': 'version3'} 
        }
        # # used to map value values from our dictionary model
        # # to expected XML tags and vice versa
        self._key_map_rule = {
            'mode': 'Mode'
        }

        # used to map value values from our dictionary model
        # to expected XML tags and vice versa
        self._value_map_rule = {
            'Mode': {'1': 'sm',
                     '2': 'dm'}
        }
        # xml tags
        self._iface_row_name = 'Interface'
        self._iface_index_name = 'IfIndex'
        self._r_key_map = dict(reversed(item) for item in self._key_map.items())
        self._r_value_map = reverse_value_map(self._r_key_map, self._value_map)

        self._r_key_map_rule = dict(reversed(item) for item in self._key_map_rule.items())
        self._r_value_map_rule = reverse_value_map(self._r_key_map_rule, self._value_map_rule)
        interface = Interface(device,interface_name) 
        self.device = device
        self.interface_name, self.iface_type, subiface_num = interface._iface_type(interface_name)
        # The interface index is needed for most interface NETCONF requests
        self.iface_index = interface._get_iface_index()
        self.is_ethernet, self.is_routed = interface._is_ethernet_is_routed()
        self.iface_exists = True if self.iface_index!='1' else False
    def build_igmp(self, stage = False, **params):
        if self.iface_exists and self.is_routed:
            params[self._iface_index_name] = self.iface_index
            EN = nc_element_maker()
            EC = config_element_maker()
            config = EN.config(
                EC.top(
                    EC.IGMP(
                        EC.Interfaces(
                            EC.Interface(
                                *config_params(params, self._key_map, value_map=self._r_value_map)
                            )
                        )
                    )
                )
            )
            if stage:
                return self.device.stage_config(config, 'edit_config')
            else:
                return self.device.edit_config(config)
        else:
            raise InterfaceAbsentError(self.interface_name)
    def remove_igmp(self, stage = False):
        operation = 'delete'
        EN = nc_element_maker()
        EC = config_element_maker()
        config = EN.config(
            EC.top(
                EC.IGMP(
                    EC.Interfaces(
                        EC.Interface(
                            EC.IfIndex(self.iface_index)
                        ),
                        **operation_kwarg(operation)
                    )
                )
            )
        )
        if stage:
            return self.device.stage_config(config, 'edit_config')
        else:
            return self.device.edit_config(config)
    def config_pim_mode(self, stage = False, **params):
        params[self._iface_index_name] = self.iface_index
        EN = nc_element_maker()
        EC = config_element_maker()
        config = EN.config(
            EC.top(
                EC.PIM(
                    EC.Ipv4Interfaces(
                        EC.Interface(
                            *config_params(params, self._key_map_rule, value_map=self._r_value_map_rule)
                        )
                    )
                )
            )
        )
        if stage:
            return self.device.stage_config(config, 'edit_config')
        else:
            return self.device.edit_config(config)
    def remove_pim_mode(self, stage = False):
        operation = 'delete'
        EN = nc_element_maker()
        EC = config_element_maker()
        config = EN.config(
            EC.top(
                EC.PIM(
                    EC.Ipv4Interfaces(
                        EC.Interface(
                            EC.IfIndex(self.iface_index)
                        ),
                        **operation_kwarg(operation)
                    )
                )
            )
        )
        if stage:
            return self.device.stage_config(config, 'edit_config')
        else:
            return self.device.edit_config(config)
    def  build_igmp_snooping(self, stage = False, snstate='disable'):
        EN = nc_element_maker()
        EC = config_element_maker()
        config = EN.config(
            EC.top(
                EC.IGMPSnooping(
                    EC.Configuration(
                        EC.Enabled(snstate)
                    )
                )
            )
        )
        if stage:
            return self.device.stage_config(config, 'edit_config')
        else:
            return self.device.edit_config(config)
