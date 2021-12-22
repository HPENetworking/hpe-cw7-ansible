"""Manage ISIS on HPCOM7 devices.
"""
# from pyhpecw7.features.errors import LengthOfStringError, VlanIDError
from pyhpecw7.utils.xml.lib import *


class Isis(object):
    """This class is used to get data and configure a specific VLAN.

    Args:
        device (HPCOM7): connected instance of a ``pyhpecw7.comware.HPCOM7``
            object.
        vlanid (str): VLAN ID

    Attributes:
        device (HPCOM7): connected instance of a ``pyhpecw7.comware.HPCOM7``
            object.
        vlanid (str): VLAN ID

    """
    def __init__(self, device, isisID=None):
        self.device = device
        if isisID:
            self.isisID = isisID

        # dictionary to XML tag mappings
        self.isis_key_map = {
            'isisID': 'Name'
        }

    def gen_top(self):
        E = data_element_maker()
        top = E.top(
            E.ISIS(
                E.Instances(
                    E.Instance()
                )
            )
        )
        return top

    def get_config(self):
        """Gets current configuration for a given VLAN ID

        Args:
            vlanid (str): REQUIRED - VLAN ID

        Returns:
            This returns a dictionary with the following
                k/v pairs:

                :vlanid (str): VLAN ID of the vlan requested
                :name (str): configured name of the vlan
                :descr (str): configured descr of the vlan

            It returns an empty dictionary if the vlan does not exist
        """
        top = self.gen_top()
        isis_id_ele = find_in_data('Instance', top)
        isis_id_ele.append(data_element_maker().Name(self.isisID))

        nc_get_reply = self.device.get(('subtree', top))
        isis_config = data_elem_to_dict(nc_get_reply.data_ele, self.isis_key_map)

        return isis_config

    def remove(self, stage=False):
        """Stage or execute XML object for VLAN removal and send to staging

        Args:
            stage (bool): whether to stage the command or execute immediately

        Returns:
            True if stage=True and successfully staged
            etree.Element XML response if immediate execution
        """
        config = self._build_config(state='absent')
        if stage:
            return self.device.stage_config(config, 'edit_config')
        else:
            return self.device.edit_config(config)

    def build(self, stage=False, **isis):
        """Stage or execute XML object for VLAN configuration and send to staging

        Args:
            stage (bool): whether to stage the command or execute immediately
            vlan: see Keyword Args

        Keyword Args:
            name (str): OPTIONAL - VLAN name
            descr (str): OPTOINAL - VLAN description

        Returns:
            True if stage=True and successfully staged
            etree.Element XML response if immediate execution
        """
        config = self._build_config(state='present', **isis)
        if stage:
            return self.device.stage_config(config, 'edit_config')
        else:
            return self.device.edit_config(config)

    def _build_config(self, state, **isis):
        """Build XML object for VLAN configuration

        Args:
            state (str): OPTIONAL must be "present" or "absent"
                DEFAULT is "present"
            vlan: see Keyword Args

            Keyword Args:
                name (str): OPTIONAL - VLAN name
                descr (str): OPTOINAL - VLAN description

        Returns:
            XML object for VLAN configuration
        """
        if state == 'present':
            operation = 'merge'
        elif state == 'absent':
            operation = 'delete'

        EC = nc_element_maker()
        E = config_element_maker()

        isis['isisID'] = self.isisID
        config = EC.config(
            E.top(
                E.ISIS(
                    E.Instances(
                        E.Instance(
                            *config_params(isis, self.isis_key_map)
                        )
                    ),
                    **operation_kwarg(operation)
                )
            )
        )

        return config

class ISis(object):
    def __init__(self, device, isisID, level, cost_style, spf_limit, preference, add_family, network):
        self.device = device
        self.isisID = isisID
        self.network = network
        self.level= level
        self.cost_style = cost_style
        self.spf_limit = spf_limit
        self.preference = preference
        self.add_family = add_family

    def _get_cmd(self, **isis):
        Network = isis.get('network')
        Level = isis.get('level')
        Cost_style = isis.get('cost_style')
        Spf_limit = isis.get('spf_limit')
        Preference = isis.get('preference')
        isisid = isis.get('isisID')
        ADD_family = isis.get('add_family')

        commands = []
        if isisid:
            cmd_1 = 'isis {0}'.format(isisid)
            if cmd_1:
                commands.append(cmd_1)

        if Level:
            cmd_2 = 'is-level' + ' {0}'.format(Level)
            if cmd_2:
                commands.append(cmd_2)

        if Cost_style:
            if Cost_style == 'compatible' or Cost_style == 'narrow-compatible':
                if Spf_limit:
                    if Spf_limit == 'true':
                        comds_2 = 'cost-style {0}'.format(Cost_style) + ' relax-spf-limit'
                    else:
                        comds_2 = 'cost-style {0}'.format(Cost_style)
            else:
                comds_2 = 'cost-style {0}'.format(Cost_style)
            commands.append(comds_2)

        if Preference:
            comds_3 = 'preference {0}'.format(Preference)
            commands.append(comds_3)
            comds_4 = 'address-family {0}'.format(ADD_family)
            commands.insert(-1, comds_4)

        if Network:
            comds_1 = 'network-entity {0}'.format(Network)
            if Preference:
                commands.append('quit')
                commands.append(comds_1)
            else:
                commands.append(comds_1)

        return commands

    def build(self, stage=False, **isis):
        return self._build_config(state='present', stage=stage, **isis)

    def _build_config(self, state, stage=False, **isis):
        isis['network'] = self.network
        isis['isisID'] = self.isisID
        isis['level'] = self.level
        isis['cost_style'] = self.cost_style
        isis['spf_limit'] = self.spf_limit
        isis['preference'] = self.preference
        isis['add_family'] = self.add_family

        c2 = True
        if state == 'present':
            get_cmd = self._get_cmd(**isis)
            if get_cmd:
                if stage:
                    c2 = self.device.stage_config(get_cmd, 'cli_config')
                else:
                    c2 = self.device.cli_config(get_cmd)
        if stage:
            return c2
        else:
            return [c2]