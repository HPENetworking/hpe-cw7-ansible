"""Manage syslpg_global on HPCOM7 devices.
"""
from pyhpecw7.utils.xml.lib import *
from pyhpecw7.features.interface import Interface
import base64
import binascii


class Netconf(object):

    def __init__(self, device, source, operation, opera_type, soap, ssh):
        self.device = device
        self.source = source
        self.operation = operation
        self.opera_type = opera_type
        self.soap = soap
        self.ssh = ssh
    def _get_cmd(self, **netConf):

        Source = netConf.get('source')
        Operation = netConf.get('operation')
        Opera_type = netConf.get('opera_type')
        SOAP = netConf.get('soap')
        SSH = netConf.get('ssh')

        commands = []
        if Source and Operation:
            if Operation == 'protocol-operation':
                cmds = 'netconf log ' + 'source {0}'.format(Source) + ' {0}'.format(Operation) + ' {0}'.format(Opera_type)
            else:
                cmds = 'netconf log ' + 'source {0}'.format(Source) + ' {0}'.format(Operation)
            commands.append(cmds)
        if SOAP:
            cmds_1 = 'netconf soap {0}'.format(SOAP) + ' enable'
            commands.append(cmds_1)
        if SSH:
            if SSH == 'enable':
                cmds_2 = 'netconf ssh server enable '
            else:
                cmds_2 = 'undo netconf ssh server enable'
            commands.append(cmds_2)
        return commands

    def _get_cmd_remove(self, **netConf):

        Source = netConf.get('source')
        Operation = netConf.get('operation')
        Opera_type = netConf.get('opera_type')
        SOAP = netConf.get('soap')
        SSH = netConf.get('ssh')

        commands = []
        if Operation == 'protocol-operation':
            cmds = 'undo netconf log ' + 'source {0}'.format(Source) + ' {0}'.format(Operation) + ' {0}'.format(Opera_type)
        else:
            cmds = 'undo netconf log ' + 'source {0}'.format(Source) + ' {0}'.format(Operation)
        commands.append(cmds)

        if SOAP:
            cmds_1 = 'undo netconf soap {0}'.format(SOAP) + ' enable'
            commands.append(cmds_1)
        if SSH:
            cmds_2 = 'undo netconf ssh server enable'
            commands.append(cmds_2)

        return commands

    def remove(self, stage=False, **netConf):

        return self._build_config_absent(state='absent', stage=stage, **netConf)

    def build(self, stage=False, **netConf):
        return self._build_config_present(state='present', stage=stage, **netConf)

    def _build_config_present(self, state, stage=False, **netConf):

        netConf['source'] = self.source
        netConf['operation'] = self.operation
        netConf['opera_type'] = self.opera_type
        netConf['soap'] = self.soap
        netConf['ssh'] = self.ssh

        c2 = True
        if state == 'present' :
            get_cmd = self._get_cmd(**netConf)
            if get_cmd:
                if stage:
                    c2 = self.device.stage_config(get_cmd, 'cli_config')
                else:
                    c2 = self.device.cli_config(get_cmd)

        if stage:
            return c2
        else:
            return [c2]

    def _build_config_absent(self, state, stage=False, **netConf):
        netConf['source'] = self.source
        netConf['operation'] = self.operation
        netConf['opera_type'] = self.opera_type
        netConf['soap'] = self.soap
        netConf['ssh'] = self.ssh
        c2 = True
        if state == 'absent' :
            get_cmd = self._get_cmd_remove(**netConf)
            if get_cmd:
                if stage:
                    c2 = self.device.stage_config(get_cmd, 'cli_config')
                else:
                    c2 = self.device.cli_config(get_cmd)

        if stage:
            return c2
        else:
            return [c2]