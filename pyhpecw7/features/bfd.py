"""Manage interfaces on HPCOM7 devices.
"""

from pyhpecw7.utils.xml.lib import reverse_value_map
from pyhpecw7.features.errors import InterfaceCreateError, InterfaceTypeError,\
    InterfaceAbsentError, InterfaceParamsError, InterfaceVlanMustExist, StpParamsError
from pyhpecw7.features.interface import Interface
from pyhpecw7.utils.xml.lib import *


class Bfd(object):
    """This class is used to get and handle bfd config
    """
    def __init__(self,device,):
        self.device = device

    def get_config(self):
        dampening_info = {}
        commands = 'dis current-configuration | inc "bfd dampening"'
        rsp = self.device.cli_display(commands)
        by_line = rsp.split('\n')
        if len(by_line)<3:
            return dampening_info
        # for each in by_line[1:]:
        damp_info = by_line[1]
        if 'dampening' in damp_info:
            dampening = damp_info.split('dampening')[-1].strip()
            dampening_vars = dampening.split(' ')
            damp_max_wait_time = dampening_vars[1]
            damp_init_wait_time = dampening_vars[3]
            secondary = dampening_vars[-1]
            dampening_info = dict(damp_max_wait_time=damp_max_wait_time,\
                                  damp_init_wait_time=damp_init_wait_time,\
                                  secondary=secondary)
        return dampening_info

    def build(self, stage=False, **kvargs):
        commands = []

        CMDS = {
            'dampening': 'bfd dampening maximum {0} initial {1} secondary {2}',
        }

        damp_max_wait_time = kvargs.get('damp_max_wait_time')
        damp_init_wait_time = kvargs.get('damp_init_wait_time')
        secondary = kvargs.get('secondary')

        if damp_max_wait_time:
            commands.append((CMDS.get('dampening')).format(damp_max_wait_time,\
                                                           damp_init_wait_time,\
                                                           secondary))
        if commands:
            if stage:
                return self.device.stage_config(commands, 'cli_config')
            else:
                return self.device.cli_config(commands)

    def default(self,stage=False):
        commands = []
        commands.append('undo bfd dampening')
        commands.append('\n')

        if stage:
            return self.device.stage_config(commands, 'cli_config')
        else:
            return self.device.cli_config(commands)