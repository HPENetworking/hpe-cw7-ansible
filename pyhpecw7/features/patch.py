"""Operation for patch in HPCOM7 devices.
"""
from lxml import etree
from ncclient.xml_ import qualify
from pyhpecw7.utils.xml.namespaces import HPDATA, HPDATA_C, HPACTION
from pyhpecw7.utils.xml.lib import *
import time

class Patch(object):
    """This class is used to get data and configure a specific File.

    Args:
        device (HPCOM7): connected instance of a ``pyhpecw7.comware.HPCOM7``
            object.

    Attributes:
        device (HPCOM7): connected instance of a ``pyhpecw7.comware.HPCOM7``
            object.

    """
    def __init__(self, device, patchname):
        self.device = device
        if patchname:
            self.patchname = patchname

    def get_file_lists(self):
        commands = 'dir | inc bin'
        Filename = '{0}'.format(self.patchname)
        res = self.device.cli_display(commands)
        if Filename in res:
            return True
        else:
            return False

    def Check_result(self):

        commands = 'dis install committed'
        Filename = 'flash:/{0}'.format(self.patchname)
        res = self.device.cli_display(commands)

        if Filename in res:
            return True
        else:
            return False

    def Activate(self, stage=False, **check_file):
        check_file['patchname'] = self.patchname
        Patchname = check_file.get('patchname')
        commands = []
        cmd_1 = 'install activate patch flash:/{0} slot 1'.format(Patchname)
        cmd_2 = 'install commit'
        commands.append(cmd_1)
        commands.insert(-1, 'quit')
        commands.append(cmd_2)
        c2 = True
        if commands:
            if stage:
                c2 = self.device.stage_config(commands, 'cli_config')
            else:
                c2 = self.device.cli_config(commands)
        # time.sleep(10)
        if stage:

            return c2
        else:
            return [c2]

    def build(self, stage=False, **check_file):
        return self.Activate(stage=stage, **check_file)


