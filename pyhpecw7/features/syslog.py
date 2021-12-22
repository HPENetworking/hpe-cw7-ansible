"""Manage syslog information on HPCOM7 devices.
"""
from pyhpecw7.features.interface import Interface

from pyhpecw7.utils.xml.lib import *


class Loghost(object):
    """This class is used to get and build syslog host
    configurations on ``HPCOM7`` devices.

    Args:
        device (HPCOM7): connected instance of a ``pyhpecw7.comware.HPCOM7``
            object.

    Attributes:
        device (HPCOM7): connected instance of a ``pyhpecw7.comware.HPCOM7``
            object.
    """
    def __init__(self, device, loghost=None, VRF=None, hostport='514', facility='184'):
#    def __init__(self, device):
        self.device = device
        self.loghost = loghost
        self.VRF = VRF
        self.hostport = hostport
        self.facility = facility

        self.LOGhost_key_map = {
            'loghost': 'Address',
            'VRF': 'VRF',
            'hostport': 'Port',
            'facility': 'Facility'
        }

    def gen_top(self):
        E = data_element_maker()
        top = E.top(
            E.Syslog(
                E.LogHosts(
                    E.Host()
                )
            )
        )
        return top

    def get_config(self):
        """

        Returns:
            A dictionary of current configuration parameters.

                }
        """
        top = self.gen_top()
        Loghost_id_ele = find_in_data('Host', top)
        Loghost_id_ele.append(data_element_maker().Address(self.loghost))
        Loghost_id_ele.append(data_element_maker().VRF(self.VRF))
        Loghost_id_ele.append(data_element_maker().Port(self.hostport))
        Loghost_id_ele.append(data_element_maker().Facility(self.facility))

        nc_get_reply = self.device.get(('subtree', top))
        Loghost_config = data_elem_to_dict(nc_get_reply.data_ele, self.LOGhost_key_map)

        return Loghost_config

    def remove(self, stage=False):
        """Stage or execute syslog configuration.

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


    def build(self, stage=False, **LOGhost):
        """Stage syslog collectorconfiguration with given parameters.

        Args:
            stage (bool): whether to stage the command or execute immediately

        Returns:
            True if stage=True and successfully staged
            etree.Element XML response if immediate execution
        """
        config = self._build_config(state='present', **LOGhost)
        if stage:
            return self.device.stage_config(config, 'edit_config')
        else:
            return self.device.edit_config(config)

    def _build_config(self, state, **LOGhost):

        if state == 'present':
            operation = 'merge'
            LOGhost['loghost'] = self.loghost
            LOGhost['VRF'] = self.VRF
            LOGhost['hostport'] = self.hostport
            LOGhost['facility'] = self.facility

        elif state == 'absent':
            operation = 'delete'

            LOGhost['loghost'] = self.loghost
            LOGhost['VRF'] = self.VRF

            LOGHOST = LOGhost.get('loghost')
            vrf = LOGhost.get('VRF')
            if LOGHOST and vrf:

                self.loghost = LOGHOST
                self.VRF = vrf

                LOGhost['loghost'] = self.loghost
                LOGhost['VRF'] = self.VRF

        EC = nc_element_maker()
        E = config_element_maker()
        config = EC.config(
            E.top(
                E.Syslog(
                    E.LogHosts(
                        E.Host(
                            *config_params(LOGhost, self.LOGhost_key_map)
                        )
                    ),
                    **operation_kwarg(operation)
                )
            )
        )

        return config

    def build_time(self, stage=True, **LOGhost):

        return self._time_config(state='present', stage=stage, **LOGhost)

    def build_time_absent(self, stage=True, **LOGhost):
        return self._time_config(state='absent', stage=stage, **LOGhost)

    def _time_config(self, state, stage=True, **LOGhost):
        c1 = True
        c2 = True
        sourceid = LOGhost.get('sourceID')
        if sourceid:

            if state == 'present':
                get_cmd = self._get_cmds_present(**LOGhost)
            if state == 'absent':
                get_cmd = self._get_cmds_absent(**LOGhost)

            if get_cmd:
                if stage:
                    c2 = self.device.stage_config(get_cmd, 'cli_config')
                else:
                    c2 = self.device.cli_config(get_cmd)

        if stage:
            return c1 and c2
        else:
            return [c1, c2]

    def _get_cmds_present(self, **LOGhost):
        sourceid = LOGhost.get('sourceID')
        command = []
        cmd = 'info-center loghost '
        if sourceid:
            command = cmd + 'source {0}'.format(sourceid)
        return command

    def _get_cmds_absent(self, **LOGhost):
        sourceid = LOGhost.get('sourceID')
        cmd = 'undo info-center loghost source'
        if sourceid:
            return cmd

#syslog souce class
class Source(object):
    """This class is used to get and build telemetry stream collector
    configurations on ``HPCOM7`` devices.

    Args:
        device (HPCOM7): connected instance of a ``pyhpecw7.comware.HPCOM7``
            object.

    Attributes:
        device (HPCOM7): connected instance of a ``pyhpecw7.comware.HPCOM7``
            object.
    """
    def __init__(self, device, channelID=None, channelName=None, level=''):

        self.device = device
        self.channelID = channelID
        self.channelName = channelName
        self.level = level

        self.source_key_map = {
            'channelID': 'Destination',
            'channelName': 'MouduleName',
            'level': 'Rule'
        }

    def gen_top(self):
        E = data_element_maker()
        top = E.top(
            E.Syslog(
                E.OutputRules(
                    E.OutputRule()
                )
            )
        )
        return top

    def get_config(self):
        """

        Returns:
            A dictionary of current configuration parameters.

  
        """
        top = self.gen_top()
        source_id_ele = find_in_data('OutputRule', top)
        source_id_ele.append(data_element_maker().Destination(self.channelID))
        source_id_ele.append(data_element_maker().MouduleName(self.channelName))
        source_id_ele.append(data_element_maker().Rule(self.level))

        nc_get_reply = self.device.get(('subtree', top))
        source_config = data_elem_to_dict(nc_get_reply.data_ele, self.source_key_map)

        return source_config

    def remove(self, stage=False):
        """Stage or execute syslog configuration.

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


    def build(self, stage=False, **SOURCE):
        """Stage syslog configuration with given parameters.

        Args:
            stage (bool): whether to stage the command or execute immediately

        Returns:
            True if stage=True and successfully staged
            etree.Element XML response if immediate execution
        """
        config = self._build_config(state='present', **SOURCE)
        if stage:
            return self.device.stage_config(config, 'edit_config')
        else:
            return self.device.edit_config(config)

    def _build_config(self, state, **SOURCE):

        if state == 'present':
            operation = 'merge'
            SOURCE['channelID'] = self.channelID
            SOURCE['channelName'] = self.channelName
            SOURCE['level'] = self.level

        elif state == 'absent':
            operation = 'delete'

            SOURCE['channelID'] = self.channelID
            SOURCE['channelName'] = self.channelName

            channelid = SOURCE.get('channelID')
            channelname = SOURCE.get('channelName')

            if channelid and channelname:

                self.channelID = channelid
                self.channelName = channelname

                SOURCE['channelID'] = self.channelID
                SOURCE['channelName'] = self.channelName

        EC = nc_element_maker()
        E = config_element_maker()
        config = EC.config(
            E.top(
                E.Syslog(
                    E.OutputRules(
                        E.OutputRule(
                            *config_params(SOURCE, self.source_key_map)
                        )
                    ),
                    **operation_kwarg(operation)
                )
            )
        )

        return config