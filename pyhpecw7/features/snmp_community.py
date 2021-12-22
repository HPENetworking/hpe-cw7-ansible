"""Manage interfaces on HPCOM7 devices.
"""

from pyhpecw7.utils.xml.lib import reverse_value_map
from pyhpecw7.features.errors import *
from pyhpecw7.features.errors import InterfaceCreateError, InterfaceTypeError,\
    InterfaceAbsentError, InterfaceParamsError, InterfaceVlanMustExist
from pyhpecw7.utils.xml.lib import *

class SnmpCommunity(object):
    """This class is used to get data and configure a specific snmp community .

    Args:
        device (HPCOM7): connected instance of a ``pyhpecw7.comware.HPCOM7``
            object.
        community_name (str): community name

    Attributes:
        device (HPCOM7): connected instance of a ``pyhpecw7.comware.HPCOM7``
            object.
        community_name (str): community name

    """
    def __init__(self, device, community_name=None):
        self.device = device
        if community_name:
            self.community_name = community_name

        # dictionary to XML tag mappings
        self.community_key_map = {
            'community_name': 'Name',
            'access_right': 'Type',
            'community_mib_view': 'MIBView',
            'acl_number': "IPv4BasicACL.Number"
        }

        self.R_community_key_map = dict(reversed(item) for item in self.community_key_map.items())
        self.type_value_map = {
            'Type': {
                '0': 'read',
                '1': 'write'
            }
        }
        self.R_type_value_map = reverse_value_map(
            self.R_community_key_map, self.type_value_map)

    def gen_top(self):
        E = data_element_maker()
        top = E.SNMP(
            E.Communities(
                E.Community(
                )
            )
        )

        return top

    def get_community_list(self):
        """Get a list of community names that exist on the switch.

        Returns:
            It returns a list of community names as strings.
        """
        top = self.gen_top()
        nc_get_reply = self.device.get(('subtree', top))
        community_xml = findall_in_data('Name', nc_get_reply.data_ele)
        communities = [community.text for community in community_xml]

        return communities

    def get_config(self):
        """Gets current configuration for a given community name
        """
        top = self.gen_top()
        community_comm_ele = find_in_data('Community', top)
        community_comm_ele.append(data_element_maker().Name(self.community_name))
        nc_get_reply = self.device.get(('subtree', top))
        snmp_community_config = data_elem_to_dict(nc_get_reply.data_ele, self.community_key_map, self.type_value_map)
        return snmp_community_config

    def remove(self, stage=False):
        """Stage or execute XML object for Community removal and send to staging

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

    def build(self, stage=True, **community):
        """Stage or execute XML object for Community configuration and send to staging

        Args:
            stage (bool): whether to stage the command or execute immediately
            community: see Keyword Args

        Keyword Args:
            community_name (str): OPTIONAL - Community name

        Returns:
            True if stage=True and successfully staged
            etree.Element XML response if immediate execution
        """
        config = self._build_config(state='present', **community)
        if stage:
            return self.device.stage_config(config, 'edit_config')
        else:
            return self.device.edit_config(config)

    def _build_config(self, state, **community):
        """Build XML object for Community configuration

        Args:
            state (str): OPTIONAL must be "present" or "absent"
                DEFAULT is "present"
            Community: see Keyword Args

            Keyword Args:
                community_name (str): OPTIONAL - Community name

        Returns:
            XML object for Community configuration
        """
        if state == 'present':
            operation = 'merge'
        elif state == 'absent':
            operation = 'delete'

        EC = nc_element_maker()
        E = config_element_maker()

        # community_name = community.get('community_name')
        # access_right = community.get('access_right')
        # community_mib_view = community.get('community_mib_view')
        # acl_number = community.get('acl_number')
        #
        # data_eles = []
        # if community_name:
        #     data_eles.append(E.Name(community_name))
        # if access_right:
        #     data_eles.append(E.Type(access_right))
        # if community_mib_view:
        #     data_eles.append(E.MIBView(community_mib_view))
        # if access_right:
        #     data_eles.append(E.IPv4BasicACL(E.Number(acl_number)))

        community['community_name'] = self.community_name

        config = EC.config(
            E.top(
                E.SNMP(
                    E.Communities(
                        E.Community(
                            *config_params(community, self.community_key_map, self.R_type_value_map)
                        )
                    ),
                    **operation_kwarg(operation)
                )
            )
        )

        return config

    def create_build(self, stage=True, **community):

        community['community_name'] = self.community_name

        community_name = community.get('community_name')
        access_right = community.get('access_right')
        community_mib_view = community.get('community_mib_view')
        acl_number = community.get('acl_number')

        commands = []
        cmd ='snmp-agent community {0} {1}'.format(access_right, community_name)
        if community_mib_view and community_mib_view != 'ViewDefault':
            cmd = cmd + ' mib-view {0}'.format(community_mib_view)
        if acl_number:
            cmd = cmd + ' acl {0}'.format(acl_number)
        commands.append(cmd)
        if stage:
            return self.device.stage_config(commands, 'cli_config')
        else:
            return self.device.cli_config(commands)
        # E = action_element_maker()
        # EN = nc_element_maker()
        # EC = config_element_maker()
        # config = EN.config(
        #     EC.top(
        #         EC.SNMP(
        #             EC.Communities(
        #                 EC.Community(
        #                     EC.Name(community_name),
        #                     EC.Type(access_right)
        #                     #EC.MIBView(community_mib_view),
        #                     #EC.IPv4BasicACL(
        #                     #    EC.Number(acl_number)
        #                     #)
        #                 )
        #             )
        #         )
        #     )
        # )
        #
        # top = E.top(
        #     E.SNMP(
        #         E.Communities(
        #             E.Community(
        #                 E.Name(community_name),
        #                 E.Type('1')
        #                 # EC.MIBView(community_mib_view),
        #                 # EC.IPv4BasicACL(
        #                 #    EC.Number(acl_number)
        #                 # )
        #             )
        #         )
        #     )
        # )
        #
        # if stage:
        #     return self.device.stage_config(top, 'action')
        # else:
        #     return self.device.action(top)

        # if stage:
        #     return self.device.stage_config(config, 'edit_config')
        # else:
        #     return self.device.edit_config(config)

    def commmunity_remove(self, stage=True, **community):

        community['community_name'] = self.community_name
        community_name = community.get('community_name')

        commands = []
        if community_name:
            cmd = 'undo snmp-agent community {0}'.format(community_name)
            commands.append(cmd)
            if stage:
                return self.device.stage_config(commands, 'cli_config')
            else:
                return self.device.cli_config(commands)
        else:
            module.fail_json(
                msg='Error: please supply the absent community_name')

        # EN = nc_element_maker()
        # EC = config_element_maker()
        # config = EN.config(
        #     EC.top(
        #         EC.SNMP(
        #             EC.Communities(
        #                 EC.Community(
        #                     EC.Name(community_name)
        #                 )
        #             )
        #         )
        #     )
        # )
        #
        # if stage:
        #     return self.device.stage_config(config, 'edit_config')
        # else:
        #     return self.device.edit_config(config)
