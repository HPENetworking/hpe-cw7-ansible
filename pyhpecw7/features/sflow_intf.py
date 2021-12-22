"""Manage sflow interface on HPCOM7 devices.
"""
from pyhpecw7.utils.xml.lib import *
from pyhpecw7.features.interface import Interface
import base64
import binascii


class Sflow(object):

    def __init__(self, device, intf_name, collector, rate):
        self.device = device
        self.intf_name = intf_name
        self.collector = collector
        self.rate = rate

    def _get_cmd(self, **SFLOW):

        index = SFLOW.get('intf_name')
        Collector = SFLOW.get('collector')
        Rate = SFLOW.get('rate')

        commands = []

        if index:
            cmd_1 = 'interface {0}'.format(index)
            commands.append(cmd_1)
        if Collector:
            cmd_2 = 'sflow flow collector {0}'.format(Collector)
            commands.append(cmd_2)
        if Rate:
            cmd_3 = 'sflow sampling-rate {0}'.format(Rate)
            commands.append(cmd_3)

        return commands

    def _get_cmd_remove(self, **SFLOW):

        index = SFLOW.get('intf_name')
        Collector = SFLOW.get('collector')
        Rate = SFLOW.get('rate')

        cmd_1 = 'undo sflow flow collector'
        cmd_2 = 'undo sflow sampling-rate'


        commands = []
        if index:
            cmd_3 = 'interface {0}'.format(index)
            commands.append(cmd_3)
            if Collector:
                commands.append(cmd_2)
            if Rate:
                commands.append(cmd_1)
        return commands

    def remove(self, stage=False, **SFLOW):

        return self._build_config_absent(state='absent', stage=stage, **SFLOW)

    def build(self, stage=False, **SFLOW):
        return self._build_config_present(state='present', stage=stage, **SFLOW)

    def _build_config_present(self, state, stage=False, **SFLOW):

        SFLOW['intf_name'] = self.intf_name
        SFLOW['rate'] = self.rate
        SFLOW['collector'] = self.collector

        c2 = True
        if state == 'present':
            get_cmd = self._get_cmd(**SFLOW)
            if get_cmd:
                if stage:
                    c2 = self.device.stage_config(get_cmd, 'cli_config')
                else:
                    c2 = self.device.cli_config(get_cmd)

        if stage:
            return c2
        else:
            return [c2]

    def _build_config_absent(self, state, stage=False, **SFLOW):

        SFLOW['intf_name'] = self.intf_name
        SFLOW['rate'] = self.rate
        SFLOW['collector'] = self.collector

        c2 = True
        if state == 'absent' :
            get_cmd = self._get_cmd_remove(**SFLOW)
            if get_cmd:
                if stage:
                    c2 = self.device.stage_config(get_cmd, 'cli_config')
                else:
                    c2 = self.device.cli_config(get_cmd)

        if stage:
            return c2
        else:
            return [c2]