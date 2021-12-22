"""Manage interfaces on HPCOM7 devices.
"""

from pyhpecw7.utils.xml.lib import reverse_value_map
from pyhpecw7.features.errors import InterfaceCreateError, InterfaceTypeError,\
    InterfaceAbsentError, InterfaceParamsError, InterfaceVlanMustExist, StpParamsError
from pyhpecw7.features.interface import Interface
from pyhpecw7.utils.xml.lib import *


class Stp(object):
    """This class is used to get and handle stp config
    """
    def __init__(self, device, interface_name):
        self.device = device
        self.interface = Interface(device, interface_name)
        self.interface_name = self.interface.interface_name
        self._key_map = {
            'edgedport': 'EdgedPort',
            'loop': 'LoopProtect',
            'root': 'RootProtect',
            'tc_restriction': 'TcRestrict',
            'transimit_limit': 'TransmitHoldCount'
        }

    def get_default_config(self):
        defaults = {}
        defaults['edgedport'] = 'false'
        defaults['loop'] = 'false'
        defaults['root'] = 'false'
        defaults['tc_restriction'] = 'false'
        defaults['transimit_limit'] = '10'
        return defaults

    def get_config(self):
        E = data_element_maker()
        top = E.top(
            E.STP(
                E.Interfaces(
                    E.Interface(
                        E.IfIndex(self.interface.iface_index)
                    )
                )
            )
        )
        nc_get_reply = self.device.get(('subtree', top))
        reply_data = find_in_data('Interface', nc_get_reply.data_ele)
        if reply_data is None:
            return {}
        return data_elem_to_dict(reply_data, self._key_map)

    def build(self, stage=False, **params):
        return self._build_config(state='present',stage=stage,**params)

    def default(self, stage=False):
        return self._build_config(state='default', stage=stage)

    def _build_config(self, state, stage=False, **params):
        if state == 'present':
            EN = nc_element_maker()
            EC = config_element_maker()
            config = EN.config(
                EC.top(
                    EC.STP(
                        EC.Interfaces(
                            EC.Interface(
                                EC.IfIndex(self.interface.iface_index),
                                *config_params(params, self._key_map)
                            )
                        )
                    )
                )
            )
            if stage:
                return self.device.stage_config(config, 'edit_config')
            else:
                return self.device.edit_config(config)
        if state == 'default':
            defaults = self.get_default_config()
            EN = nc_element_maker()
            EC = config_element_maker()
            config = EN.config(
                EC.top(
                    EC.STP(
                        EC.Interfaces(
                            EC.Interface(
                                EC.IfIndex(self.interface.iface_index),
                                *config_params(defaults, self._key_map)
                            )
                        )
                    )
                )
            )
            if stage:
                return self.device.stage_config(config, 'edit_config')
            else:
                return self.device.edit_config(config)

        return False