"""Operation for Configuration comparison in HPCOM7 devices.
"""
from lxml import etree
from ncclient.xml_ import qualify
from pyhpecw7.utils.xml.namespaces import HPDATA, HPDATA_C, HPACTION
from pyhpecw7.utils.xml.lib import *
import os

class Compare(object):
    """This class is used to get data and configure a specific File.

    Args:
        device (HPCOM7): connected instance of a ``pyhpecw7.comware.HPCOM7``
            object.

    Attributes:
        device (HPCOM7): connected instance of a ``pyhpecw7.comware.HPCOM7``
            object.

    """
    def __init__(self, device, cmd, result):
        self.device = device
        if cmd:
            self.cmd = cmd
        if result:
            self.result=result

    def get_result(self):
        Result = self.result

        commands = '{0}'.format(self.cmd)
        res = self.device.cli_display(commands)
        ele = res.split('\n')
        element = ele[1:-1]


        with open('/root/ansible-hpe-cw7-master/gqy/gqy.txt', 'w+') as f:
            for i in enumerate (element):
                if i[0] != len(element)-1:
                    f.write(i[1].lstrip() + '\n')
                else:
                    f.write(i[1].strip())


        alist = []
        blist = []

        for line in open(Result):
            alist.append(line)
        for line in open('/root/ansible-hpe-cw7-master/gqy/gqy.txt'):
            blist.append(line)

        # print("a have  b not have")
        # print(set(alist).difference(set(blist)))
        # print("b have  a not have")
        # print(set(blist).difference(set(alist)))
        if set(alist) == set(blist):
            return True
        else:
            return False



