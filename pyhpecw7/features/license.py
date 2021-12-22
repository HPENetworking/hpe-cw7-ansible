"""Manage interfaces on HPCOM7 devices.
"""

from pyhpecw7.utils.xml.lib import reverse_value_map
from pyhpecw7.features.errors import InterfaceCreateError, InterfaceTypeError,\
    InterfaceAbsentError, InterfaceParamsError, InterfaceVlanMustExist, StpParamsError
from pyhpecw7.features.interface import Interface
from pyhpecw7.utils.xml.lib import *
import re


class License(object):
    """This class is used to get and handle radius config
    """
    def __init__(self,device,):
        self.device = device

    def get_config(self):
        license = {}
        commands = 'display license'
        rsp = self.device.cli_display(commands)
        rsp_line = rsp.split('\n')
        for each in rsp_line[1:]:
            if each.split(':')[0].strip().lower() == 'flash':
                license['license'] = each.split(':')[1].strip()
            if each.split(':')[0].strip().lower() == 'current state':
                license['license_state'] = each.split(':')[1].strip()

        return license

    def build(self, stage=False, **kvargs):
        commands = []
        CMDS = {
            'license': 'license activation-file install flash:/{0} slot {1}',
        }
        license_active = kvargs.get('license')
        slot = kvargs.get('slot')
        if license_active:
            commands.append((CMDS.get('license')).format(license_active,slot))

        if commands:
            commands.insert(0, 'system-view')
            commands.append('\n')
            if stage:
                return self.device.stage_config(commands, 'cli_config')
            else:
                return self.device.cli_config(commands)


