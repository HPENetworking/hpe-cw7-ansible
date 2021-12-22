"""Manage dldp on HPCOM7 devices.
"""
from pyhpecw7.utils.xml.lib import *
from pyhpecw7.features.interface import Interface
import base64
import binascii


class Dldp(object):

    def __init__(self, device, global_enable, auth_mode, timeout, port_shutdown, pwd_mode, init_delay, pwd, name, interface_enable, shutdown_mode):
        self.device = device
        self.global_enable = global_enable
        self.auth_mode = auth_mode
        self.timeout = timeout
        self.pwd_mode = pwd_mode
        self.init_delay = init_delay
        self.pwd = pwd
        self.name = name
        self.interface_enable = interface_enable
        self.shutdown_mode = shutdown_mode
        self.port_shutdown = port_shutdown

    def _get_cmd(self, **DLDP):

        Global_enable = DLDP.get('global_enable')
        Auth_mode = DLDP.get('auth_mode')
        Name = DLDP.get('name')
        Interface_enable = DLDP.get('interface_enable')
        Pwd_mode = DLDP.get('pwd_mode')
        Init_delay = DLDP.get('init_delay')
        Pwd = DLDP.get('pwd')
        Shutdown_mode = DLDP.get('shutdown_mode')
        Port_shutdown = DLDP.get('port_shutdown')
        Timeout = DLDP.get('timeout')

        commands = []
        cmd_1 = 'dldp global enable'
        cmd_2 = 'dldp authentication-mode '
        cmd_3 = 'dldp authentication-password '
        cmd_4= 'dldp enable'
        cmd_5 = 'dldp unidirectional-shutdown '
        cmd_6 = 'dldp port unidirectional-shutdown '
        cmd_7 = 'undo dldp global enable'
        cmd_12 = 'dldp interval '
        cmd_16 = 'undo dldp enable'
        if Global_enable:
            if Global_enable == 'enable':
                commands.append(cmd_1)
            else:
                commands.append(cmd_7)
        if Auth_mode:
            cmd_8 = cmd_2 + '{0}'.format(Auth_mode)
            commands.append(cmd_8)
        if Pwd:
            cmd_9 = cmd_3 + '{0}'.format(Pwd_mode) + ' {0}'.format(Pwd)
            commands.append(cmd_9)
        if Shutdown_mode:
            cmd_10 = cmd_5 + '{0}'.format(Shutdown_mode)
            commands.append(cmd_10)
        if Timeout:
            cmd_11 = cmd_12 + '{0}'.format(Timeout)
            commands.append(cmd_11)
        if Name:
            cmd_13 = 'interface ' + '{0}'.format(Name)
            commands.append(cmd_13)
            if Interface_enable and not Init_delay:
                if Interface_enable == 'enable':
                    commands.append(cmd_4)
                else:
                    commands.append(cmd_16)
            if Interface_enable and Init_delay:
                cmd_14 = cmd_4 + ' initial-unidirectional-delay ' + '{0}'.format(Init_delay)
                commands.append(cmd_14)
            if Port_shutdown:
                cmd_15 = cmd_6 + '{0}'.format(Port_shutdown)
                commands.append(cmd_15)

        return commands

    def _get_cmd_remove(self, **DLDP):

        Global_enable = DLDP.get('global_enable')
        Auth_mode = DLDP.get('auth_mode')
        Name = DLDP.get('name')
        Interface_enable = DLDP.get('interface_enable')
        Pwd_mode = DLDP.get('pwd_mode')
        Init_delay = DLDP.get('init_delay')
#        Pwd = DLDP.get('pwd')
        Shutdown_mode = DLDP.get('shutdown_mode')
        Port_shutdown = DLDP.get('port_shutdown')
        Timeout = DLDP.get('timeout')

        cmd_1 = 'undo dldp global enable'
        cmd_2 = 'undo dldp authentication-mode'
        cmd_3 = 'undo dldp interval'
        cmd_4 = 'undo dldp unidirectional-shutdown'
        cmd_6 = 'undo dldp enable'
        cmd_7 = 'undo dldp port unidirectional-shutdown'
        cmd_8 = 'undo dldp authentication-password'
        commands = []
        if Global_enable:
            commands.append(cmd_1)
        if Auth_mode:
            commands.append(cmd_2)
        if Pwd_mode:
            commands.append(cmd_8)
        if Timeout:
            commands.append(cmd_3)
        if Shutdown_mode:
            commands.append(cmd_4)
        if Name:
            cmd_5 = 'interface ' + '{0}'.format(Name)
            commands.append(cmd_5)
            if Interface_enable:
                commands.append(cmd_6)
            if Port_shutdown:
                commands.append(cmd_7)

        return commands

    def remove(self, stage=False, **DLDP):

        return self._build_config_absent(state='absent', stage=stage, **DLDP)

    def build(self, stage=False, **DLDP):
        return self._build_config_present(state='present', stage=stage, **DLDP)

    def _build_config_present(self, state, stage=False, **DLDP):

        DLDP['global_enable'] = self.global_enable
        DLDP['auth_mode'] = self.auth_mode
        DLDP['pwd_mode'] = self.pwd_mode
        DLDP['interface_enable'] = self.interface_enable
        DLDP['pwd'] = self.pwd
        DLDP['timeout'] = self.timeout
        DLDP['name'] = self.name
        DLDP['init_delay'] = self.init_delay
        DLDP['shutdown_mode'] = self.shutdown_mode
        DLDP['port_shutdown'] = self.port_shutdown

        c2 = True
        if state == 'present':
            get_cmd = self._get_cmd(**DLDP)
            if get_cmd:
                if stage:
                    c2 = self.device.stage_config(get_cmd, 'cli_config')
                else:
                    c2 = self.device.cli_config(get_cmd)

        if stage:
            return c2
        else:
            return [c2]

    def _build_config_absent(self, state, stage=False, **DLDP):

        DLDP['global_enable'] = self.global_enable
        DLDP['auth_mode'] = self.auth_mode
        DLDP['pwd_mode'] = self.pwd_mode
        DLDP['interface_enable'] = self.interface_enable
        DLDP['pwd'] = self.pwd
        DLDP['timeout'] = self.timeout
        DLDP['name'] = self.name
        DLDP['init_delay'] = self.init_delay
        DLDP['shutdown_mode'] = self.shutdown_mode
        DLDP['port_shutdown'] = self.port_shutdown

        c2 = True
        if state == 'absent' :
            get_cmd = self._get_cmd_remove(**DLDP)
            if get_cmd:
                if stage:
                    c2 = self.device.stage_config(get_cmd, 'cli_config')
                else:
                    c2 = self.device.cli_config(get_cmd)

        if stage:
            return c2
        else:
            return [c2]