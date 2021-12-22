from pyhpecw7.features.errors import *
from pyhpecw7.utils.xml.lib import *
from pyhpecw7.features.interface import Interface
import base64
import binascii

class Lacp(object):
    def __init__(self, device,priorityID='32768'):
        self.device = device
        self.priorityID = priorityID


        self.LACP_key_map = {
            'priorityID': 'SystemPriority'

        }

    def gen_top(self):
            E = data_element_maker()
            top = E.top(
                E.LAGG(
                    E.Base()
                )
            )
            return top
    def build_time(self, stage=True, **LACP):

        return self._time_config(state='present', stage=stage, **LACP)

    def build_time_absent(self, stage=True, **LACP):
        return self._time_config(state='default', stage=stage, **LACP)


##global
    def get_default(self):
        return {'priorityID': '32768'}
    def remove(self, stage=False):

        config = self._build_config(state='default')
        if stage:
            return self.device.stage_config(config, 'edit_config')
        else:
            return self.device.edit_config(config)

    def default(self, state, stage=False):
        defaults = self.get_default()
        return self.build(state=state, stage=stage, **defaults)

    def _time_config(self, state, stage=True, **LACP):
        c1 = True
        c2 = True
        sysMAC = LACP.get('sysmac')
        if sysMAC:

            if state == 'present':
                get_cmd = self._get_cmds_present(**LACP)
            if state == 'default':

                get_cmd = self._get_cmds_absent(**LACP)

            if get_cmd:
                if stage:
                    c2 = self.device.stage_config(get_cmd, 'cli_config')
                else:
                    c2 = self.device.cli_config(get_cmd)

        if stage:
            return c1 and c2
        else:
            return [c1, c2]

    def _get_cmds_absent(self, **LACP):
        sysMAC = LACP.get('sysmac')

        cmd = 'undo lacp system-mac'
        if sysMAC:

            return cmd

    def _get_cmds_present(self, **LACP):
        sysMAC = LACP.get('sysmac')
        command = []
        cmd = 'lacp system-mac '
        if sysMAC:
            command = cmd + '{0}'.format(sysMAC)
        return command

    def build(self, stage=False, **LACP):

        config = self._build_config(state='present', **LACP)
        if stage:
            return self.device.stage_config(config, 'edit_config')
        else:
            return self.device.edit_config(config)

    def _build_config(self, state, **LACP):

        if state == 'present':
                operation = 'merge'
                LACP['priorityID'] = self.priorityID

        elif state == 'default':
                operation = 'delete'
                self.priorityID = ''
                LACP['priorityID'] = self.priorityID

        EC = nc_element_maker()
        E = config_element_maker()

        config = EC.config(
            E.top(
                E.LAGG(
                    E.Base(
                            *config_params(LACP, self.LACP_key_map)
                    ),
                    **operation_kwarg(operation)
                )
            )
        )

        return config


