"""Manage connections to HPCOM7 devices.

(c) Copyright 2016 Hewlett Packard Enterprise Development LP Licensed under the Apache License, Version 2.0
(the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License
at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
express or implied. See the License for the specific language governing permissions and limitations under the License.

"""
from ncclient import manager
from ncclient.operations.rpc import RPCError
import ncclient.transport.errors as NcTransErrors
import ncclient.operations.errors as NcOpErrors
from pyhpecw7.features.facts import Facts
import time
import socket
from lxml import etree
from pyhpecw7.utils.xml.namespaces import NETCONFBASE_C
from pyhpecw7.errors import NCTimeoutError, ConnectionClosedError, NCError,\
    ConnectionAuthenticationError, ConnectionSSHError, ConnectionUnkownHostError,\
    ConnectionError, LockConflictError, UnlockConflictError


class HPCOM7(object):
    """This class manages the NETCONF connection to an HP Comware switch,
    and provides methods to execute various NETCONF operations.

    Args:
        host: REQUIRED - hostname or IP address of the HP Comware Switch
        username: REQUIRED - username used to login to the switch. Requires
            network-admin access
        password: REQUIRED - password used to login to the switch. Requires
            network-admin access
        port: OPTIONAL - integer that represents the NETCONF port being
            used on the switch.  Default is 830.
        timeout: OPTIONAL - How long a single RPC rquest should wait
            before timing out.
        ssh_config: OPTIONAL - enables parsing of a OpenSSH configuration
            file, either file in string, or defaults to ~/.ssh/config if True

    Attributes:
        staged: Dictionary that stores XML objects prior to being sent to
           the device.  It is a "holding" area.  The stage_config method
           is are used to build this attribute.  Keys are user defined
           to make it possible to recall/view the specified object if more
           than one are being prepared to send.
        staged_cli: Dictionary that stores XML objects when pushing
           raw CLI commands via NETCONF.  It is a "holding" area.
           The stage_cli_display and stage_cli_config methods are used
           to build this attribute.  Keys are user defined to make it
           possible to recall/view the specified object if more than one
           are being prepared to send.
    """
    def __init__(self, **kvargs):
        self.host = kvargs.get('host')
        self.username = kvargs.get('username')
        self.password = kvargs.get('password')
        self.port = kvargs.get('port') or 830
        self.timeout = kvargs.get('timeout') or 30
        self.ssh_config = kvargs.get('ssh_config', None)
        self.staged = []

        self._locked = False

    def open(self,
             hostkey_verify=False,
             allow_agent=False,
             look_for_keys=False):
        """Open the NETCONF connection to the HP switch.

        Args:
            hostkey_verify (bool): OPTIONAL - enables hostkey verification
                from ~/.ssh/known_hosts
            allow_agent (bool): OPTIONAL -
                enables querying SSH agent (if found) for keys
            look_for_keys (bool): OPTIONAL - enables looking in the
                usual locations for ssh keys (e.g. ~/.ssh/id_*)

        Returns:
            Connection to the device using ncclient's connect method.

        Raises:
            ConnectionAuthenticationError: if there is an error authenticating
                to the device.
            ConnectionSSHError: if NETCONF isn't enabled on the device, or the
                device isn't reachable
            ConnectionUnkownHostError: if the device's network name cannot
                be resolved to an IP address.
            ConnectionError: if an unkown error occurs during connection
        """
        time.sleep(.25)

        try:
            self.connection = manager.connect(host=self.host,
                                              port=self.port,
                                              username=self.username,
                                              password=self.password,
                                              device_params={'name': 'hpcomware'},
                                              hostkey_verify=hostkey_verify,
                                              allow_agent=allow_agent,
                                              manager_params={'timeout': self.timeout},
                                              look_for_keys=look_for_keys,
                                              timeout=self.timeout,
                                              ssh_config=self.ssh_config)

        except NcTransErrors.AuthenticationError:
            raise ConnectionAuthenticationError(self)
        except NcTransErrors.SSHError:
            raise ConnectionSSHError(
                self, msg='There was an error connecting with SSH.'
                ' The NETCONF server may be down or refused the connection.'
                ' The connection may have timed out if the server wasn\'t reachable.')
        except socket.gaierror:
            raise ConnectionUnkownHostError(self)
        except ImportError:
            raise ImportError('ncclient does not have the comware extensions')
        except Exception:
            raise ConnectionError(self, msg='There was an unknown error while trying to connect.')

        return self.connection

    @property
    def facts(self):
        """
        A dictionary of a facts about the device.
        ``None`` if not connected.
        """
        if hasattr(self, 'connection'):
            if self.connection.connected:
                facts = Facts(self)
                return dict(facts.facts)
        return None

    @property
    def connected(self):
        """``True`` if the NETCONF session to the device is open
        else it is ``False``.
        """
        if hasattr(self, 'connection'):
            return self.connection.connected

        return False

    def close(self):
        """Close the NETCONF connection to the HP switch.
        """
        try:
            if self.connected:
                self.connection.close_session()
        except NcOpErrors.TimeoutExpiredError:
            raise NCTimeoutError

    def stage_config(self, config, cfg_type):
        """Append config object to the staging area.

        Args:
            config: The config payload. Could be a partial etree.Element XML
                object or raw text if using a CLI config type
            cfg_type (string): The type of config payload.
                Permitted options: "edit_config", "action", "cli_config",
                "cli_display", "save", "rollback"

        Returns:
            True if config object was successfully staged.

        Raises:
            ValueError: if an invalid config type is supplied.
        """
        if cfg_type in ['edit_config', 'action', 'cli_config',
                        'cli_display', 'save', 'rollback']:
            self.staged.append({'config': config, 'cfg_type': cfg_type})
            return True
        else:
            raise ValueError("Invalid config type for staging.  Must be one"
                             + "of the following: edit_config, action, "
                             + "cli_config, cli_display, save, rollback")

    def staged_to_string(self):
        """Convert the staging area to a list of strings.

        Returns:
            A list of string representing the configuration in the
            staging area.
        """
        cfgs = []
        for cfg in self.staged:
            if isinstance(cfg['config'], etree._Element):
                cfgs.append(etree.tostring(cfg['config']))
            else:
                cfgs.append(cfg['config'])

        return cfgs

    def execute(self, run_cmd_func, args=[], kwargs={}):
        """Safely execute the supplied function with args and kwargs.

        Args:
            run_cmd_func(executable): Function to be run.

        Returns:
            The return value of the supplied function.

        Raises:
            NCError: if there is an error in the NETCONF protocol.
            NCTimeoutError: if a client-side timeout has occured.
            ConnectionClosedError: if the NETCONF session is closed.
        """
        if self.connected is not True:
            raise ConnectionClosedError(self)

        try:
            self.lock()
            rsp = run_cmd_func(*args, **kwargs)
        except RPCError as e:
            raise NCError(e)
        except NcOpErrors.TimeoutExpiredError:
            raise NCTimeoutError
        except NcTransErrors.TransportError:
            raise ConnectionClosedError(self)
        finally:
            self.unlock()

        return rsp

    def execute_staged(self, target='running'):
        """Execute/Push the XML object(s) or CLI strings in the staging
        area (self.staged) to the device.

        Args:
            target (str): must be set to running.
                It *could* change in the future
                if HP supports candidate configurations, etc.
                Only used for 'edit_config' API calls.
                Defaults to 'running'.

        Returns:
            A list of responses received from the device.
            Responses with CLI information are extracted from the XML
            response.
        """
        rsps = []
        for command in self.staged:
            cfg_type = command['cfg_type']
            config = command['config']
            args = []
            kwargs = {}
            if cfg_type == 'edit_config':
                run_cmd_func, kwargs = self.edit_config, dict(target=target, config=config)
            elif cfg_type == 'action':
                run_cmd_func, args = self.action, [config]
            elif cfg_type == 'save':
                run_cmd_func, args = self.save, [config]
            elif cfg_type == 'rollback':
                run_cmd_func, args = self.rollback, [config]
            elif cfg_type == 'cli_config':
                run_cmd_func, args = self.cli_config, [config]
            elif cfg_type == 'cli_display':
                run_cmd_func, args = self.cli_display, [config]

            rsps.append(run_cmd_func(*args, **kwargs))

        del self.staged[:]
        return rsps

    def lock(self, target='running'):
        """Attempt to lock the NETCONF connection.

        Raises:
            NCError: if there is an error in the NETCONF protocol.
            LockConflictError: if another process hold the NETCONF lock.
        """
        try:
            self.connection.lock(target)
            self._locked = True
        except RPCError as e:
            if e.tag == 'lock-denied':
                raise LockConflictError
            else:
                raise NCError(e)

    def unlock(self, target='running'):
        """Attempt to unlock the NETCONF connection.

        Raises:
            NCError: if there is an error in the NETCONF protocol.
            LockConflictError: if another process hold the NETCONF lock.
        """
        try:
            if self._locked:
                self.connection.unlock(target)
                self._locked = False
        except RPCError as e:
            if e.tag == 'operation-failed'\
                    and 'Unlock Failed' in e.message:
                raise UnlockConflictError
            else:
                raise NCError(e)
        except NcTransErrors.TransportError:
            pass

    def edit_config(self, config, target='running'):
        """Send a NETCONF edit_config XML object to the device.

        Args:
            config: etree.Element sent to ncclient.manager.edit_config
            target: Name of configuration on the remote device. Defaults to 'running'

        Returns:
            The etree.Element returned from ncclient.manager.edit_config
        """
        rsp = self.execute(self.connection.edit_config, kwargs=dict(target=target, config=config))
        return rsp

    def get(self, get_tuple=None):
        """Wrapper for ncclient.manger.get

        Args:
            get_tuple: The tuple sent to ncclient.manager.get,
                e.g: ('subtree', <etree.Element>)

        Returns:
            The etree.Element returned from ncclient.manager.get

        """
        rsp = self.execute(self.connection.get, [get_tuple])
        return rsp

    def action(self, element):
        """Wrapper for ncclient.manger.action

        Args:
            element: etree.Element sent to ncclient.manager.action

        Returns:
            The etree.Element returned from ncclient.manager.action
        """
        rsp = self.execute(self.connection.action, [element])
        return rsp

    def save(self, filename=None):
        """Wrapper for ncclient.manger.save

        Args:
            element: etree.Element sent to ncclient.manager.save

        Returns:
            The etree.Element returned from ncclient.manager.save
        """
        rsp = self.execute(self.connection.save, [filename])
        return rsp

    def rollback(self, filename):
        """Wrapper for ncclient.manger.rollback

        Args:
            element: etree.Element sent to ncclient.manager.rollback

        Returns:
            The etree.Element returned from ncclient.manager.rollback
        """
        rsp = self.execute(self.connection.rollback, [filename])
        return rsp

    def cli_display(self, command):
        """Immediately push display commands to the device and returns text.

        Args:
            command (list or string): display commands

        Returns:
            raw text CLI output

        """
        rsp = self.execute(self.connection.cli_display, [command])
        text = self._find_between(rsp.xml, 'CDATA[', ']]')
        text = self._strip_return(text)

        return text

    def cli_config(self, command):
        """Immediately push config commands to the device and returns text.

        Args:
            command (list or string): config commands

        Returns:
            raw text CLI output

        """
        rsp = self.execute(self.connection.cli_config, [command])
        xml = bytes(bytearray(rsp.xml, encoding='utf-8'))
        xml_obj = etree.fromstring(xml)
        return self._extract_config(xml_obj)

    def reboot(self):
        """Attempt an immediate reboot of the device.

        """
        try:
            self.connection.async_mode = True
            self.connection.cli_display(['reboot force'])
        except NCTimeoutError:
            pass
        finally:
            self.connection.async_mode = False

    def _strip_return(self, text):
        """Strip excess return characters from text.
        """
        if text:
            text = text.replace('\r\r\r', '\r')
            text = text.replace('\r\r', '\r')
            text = text.replace('\n\n\n', '\n')
            text = text.replace('\n\n', '\n')

        return text

    def _extract_config(self, xml_resp):
        """Extract a CLI response from an XML object.
        """
        conf = xml_resp.find('.//{0}Configuration'.format(NETCONFBASE_C))
        execu = xml_resp.find('.//{0}Execution'.format(NETCONFBASE_C))

        if execu is not None:
            text = execu.text
        elif conf is not None:
            text = conf.text
        else:
            text = 'Unable to extract CLI data.'

        text = self._strip_return(text)

        return text

    def _find_between(self, s, first, last):
        """Find a substring in between two other substrings.

        Args:
            s: The full string
            first: The first substring
            second: The second substring
        """
        try:
            start = s.index(first) + len(first)
            end = s.index(last, start)
            return s[start:end]
        except ValueError:
            return ""
