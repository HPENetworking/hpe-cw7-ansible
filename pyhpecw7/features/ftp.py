"""Manage FTP on HPCOM7 devices.
author: liudongxue
"""
from pyhpecw7.utils.xml.lib import *
# from pyhpecw7.features.interface import Interface
# import base64
# import binascii
#from pyhpecw7.features.ping import Ping

class Ftp(object):

    def __init__(self, device,state):
        self.device = device
        self.state = state
    def config_ftp(self, stage = False):
        EN = nc_element_maker()
        EC = config_element_maker()
        config = EN.config(
            EC.top(
                EC.FTP(
                    EC.Server(
                        EC.State(self.state)
                    )
                )
            )
        )
        if stage:
            return self.device.stage_config(config, 'edit_config')
        else:
            return self.device.edit_config(config)
    # # def get_cmd(self):
       # Xml = netConf.get('xml')
        # # commands = []
        # # cmds = 'return' 
        # # if self.host :
            # # cmds = 'ftp' + ' '+'{0}'.format(self.host)  
            # # commands.append(cmds)
            # # if self.name:
                # # cmds = '{0}'.format(self.name) 
                # # commands.append(cmds)
            # # if self.keys:
                # # cmds = '{0}'.format(self.keys) 
                # # commands.append(cmds)  
            # # if self.filename:
                # # cmds = 'get' + ' '+'{0}'.format(self.filename) 
                # # commands.append(cmds)                 
        # # return commands

    # def remove(self, stage=False, **netConf):

        # return self._build_config_absent(state='absent', stage=stage, **netConf)
    # def build(self, stage=False, **netConf):
        # return self._build_config_present(state='present', stage=stage, **netCon
    # # def ftp_get_file(self, stage=False):
        # # c2 = True
        # # get_cmd = self.get_cmd()
        # # if get_cmd:
            # # if stage:
                # # c2 = self.device.stage_config(get_cmd, 'cli_config')
            # # else:
                # # c2 = self.device.cli_config(get_cmd)
        # # if stage:
            # # return c2
        # # else:
            # # return [c2]

    # def _build_config_absent(self, state, stage=False, **netConf):


        # netConf['source'] = self.source
        # netConf['operation'] = self.operation
        # netConf['opera_type'] = self.opera_type
# #        netConf['xml'] = self.xml
        # c2 = True
        # if state == 'absent' :
            # get_cmd = self._get_cmd_remove(**netConf)
            # if get_cmd:
                # if stage:
                    # c2 = self.device.stage_config(get_cmd, 'cli_config')
                # else:
                    # c2 = self.device.cli_config(get_cmd)

        # if stage:
            # return c2
        # else:
            # return [c2]