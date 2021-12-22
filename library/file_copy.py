"""Manage file transfer to HPCOM7 devices.
author: liudongxue
"""
from scp import SCPClient
from lxml import etree
from pyhpecw7.utils.xml.lib import *
from pyhpecw7.features.errors import FileNotEnoughSpaceError,\
    FileNotReadableError, FileRemoteDirDoesNotExist, FileTransferError, FileHashMismatchError
from pyhpecw7.errors import NCError
from ftplib import FTP
import paramiko
import hashlib
import re
import os


class FileCopy(object):
    """This class is used to copy local files to a ``HPCOM7`` device.

    Note:
        SCP should first be enabled on the device.

    Note:
        When using this class, the passed in ``HPCOM7`` object should
        be constructed with the ``timeout`` equal to at least 60 seconds.
        Remote MD5 sum calculations can take some time.

    Note:
        If the remote directory doesn't exist (check ``remote_dir_exists``),
        it's the responsibility of the user to call ``create_remote_dir()``
        before calling ``transfer_file()``. Otherwise, a
        ``FileRemoteDirDoesNotExist`` exception will be raised.

    Args:
        device (HPCOM7): connected instance of
            a ``pyhpecw7.comware.HPCOM7`` object.
        src (str): Full path to local file to be copied.
        dst (str): OPTIONAL - Full path or filename of remote file.
            If just a filename is supplied, 'flash:/' will be prepended.
            If nothing is supplied, the source filename will be used,
            and 'flash:/' will be prepended.
        port (int): OPTIONAL - The SSH port over which
            the SCP connection is made. Defaults to 22.

    Attributes:
        device (HPCOM7): connected instance of
            a ``pyhpecw7.comware.HPCOM7`` object.
        src (str): Full path to local file to be copied.
        dst (str): Full path of remote file.
        port (int): The SSH port over which
            the SCP connection is made.
        remote_dir_exists (bool): Whether there remote
            directory exists.
    """
    def __init__(self, device, src, dst=None, port=22):
        self.device = device
        self.src = src
        self.dst = dst or os.path.basename(src)

        if self.dst.find(':/') < 0:
            self._remote_dir = 'flash:/'
            self.dst = self._remote_dir + self.dst
            self.ftp_dst = os.path.basename(self.src)            
        else:
            self._remote_dir = '/'.join(
                self.dst.split('/')[:-1]) + '/'
            self.ftp_dst=self.dst.split('flash:/')[1].rstrip()
        if self._remote_dir[-2:] == ':/':
            self.remote_dir_exists = True
        else:
            self.remote_dir_exists = self._remote_dir_exists()

        self.port = port

    def _get_flash_size(self):
        """Return the available space in the remote directory.
        """
        rsp = self.device.cli_display('dir ' + self._remote_dir)
        match = re.search(r'\((\d+)(\s+KB\s+free\))', rsp)

        try:
            return int(match.group(1)) * 1000
        except:
            return 0

    def _enough_space(self):
        """Check for enough space on the remote device.

        Raises:
            FileNotEnoughSpaceError: if there isn't enough space
                on the remote device.
        """
        flash_size = self._get_flash_size()
        file_size = os.path.getsize(self.src)
        if file_size > flash_size:
            raise FileNotEnoughSpaceError(self.src, file_size, flash_size)

    def file_already_exists(self):
        """Check to see if there is a remote file with the same
        name and md5 sum.

        Returns:
            ``True`` if exists, ``False`` otherwise.
        """
        if not self.remote_dir_exists:
            return False

        try:
            dst_hash = self._get_remote_md5()
        except NCError:
            return False

        src_hash = self._get_local_md5()
        if src_hash == dst_hash:
            return True

        return False

    def _safety_checks(self):
        """Check to make sure the source file exists,
        and that there's enough space on the device.

        Throws:
            FileNotReadableError: if the local file doesn't
                exist or isn't readable.
        """
        try:
            f = open(self.src, "rb")
        except IOError:
            raise FileNotReadableError(self.src)
        finally:
            try:
                f.close()
            except NameError:
                pass

        if not self.remote_dir_exists:
            raise FileRemoteDirDoesNotExist(self._remote_dir)

        if self.remote_dir_exists:
            if not self.file_already_exists():
                self._enough_space()

    def _get_remote_md5(self):
        """Return the md5 sum of the remote file,
        if it exists.
        """
        E = action_element_maker()
        top = E.top(
            E.FileSystem(
                E.Files(
                    E.File(
                        E.SrcName(self.dst),
                        E.Operations(
                            E.md5sum()
                        )
                    )
                )
            )
        )


        nc_get_reply = self.device.action(top)
        reply_ele = etree.fromstring(nc_get_reply.xml)
        md5sum = find_in_action('md5sum', reply_ele)

        if md5sum is not None:
            return md5sum.text.strip()

    def _get_local_md5(self, blocksize=2**20):
        """Get the md5 sum of the local file,
        if it exists.
        """
        m = hashlib.md5()
        with open(self.src, "rb") as f:
            buf = f.read(blocksize)
            while buf:
                m.update(buf)
                buf = f.read(blocksize)
        return m.hexdigest()

    def _remote_dir_exists(self):
        """Check to see if the remote directory exists.
        """
        E = data_element_maker()
        top = E.top(
            E.FileSystem(
                E.Files(
                    E.File(
                        E.Name(self._remote_dir.rstrip('/')),
                        E.IsDirectory()
                    )
                )
            )
        )

        nc_get_reply = self.device.get(('subtree', top))

        reply_ele = etree.fromstring(nc_get_reply.xml)
        is_dir = find_in_data('IsDirectory', reply_ele)

        if is_dir is not None\
                and is_dir.text == 'true':
            return True

        return False

    def create_remote_dir(self):
        """Create the remote directory.

        Raises:
            FileCreateDirectoryError: if the directory could
                not be created.
        """
        E = action_element_maker()
        top = E.top(
            E.FileSystem(
                E.Files(
                    E.File(
                        E.SrcName(self._remote_dir.strip('/')),
                        E.Operations(
                            E.MkDir()
                        )
                    )
                )
            )
        )

        nc_get_reply = self.device.action(top)
        reply_ele = etree.fromstring(nc_get_reply.xml)

        self.remote_dir_exists = True

    def transfer_file(self, hostname=None, username=None, password=None, look_for_keys=False):
        """Transfer the file to the remote device over SCP.

        Note:
            If any arguments are omitted, the corresponding attributes
            of the ``self.device`` will be used.

        Args:
            hostname (str): OPTIONAL - The name or
                IP address of the remote device.
            username (str): OPTIONAL - The SSH username
                for the remote device.
            password (str): OPTIONAL - The SSH password
                for the remote device.

        Raises:
            FileTransferError: if an error occurs during the file transfer.
            FileHashMismatchError: if the source and
                destination hashes don't match.
            FileNotReadableError: if the local file doesn't exist or isn't readable.
            FileNotEnoughSpaceError: if there isn't enough space on the device.
            FileRemoteDirDoesNotExist: if the remote directory doesn't exist.
        """
        self._safety_checks()

        hostname = hostname or self.device.host
        username = username or self.device.username
        password = password or self.device.password

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(
            hostname=hostname,
            username=username,
            password=password,
            port=self.port,
            allow_agent=False,
            look_for_keys=look_for_keys)

        scp = SCPClient(ssh.get_transport())
        try:
            scp.put(self.src, self.dst)
        except:
            raise FileTransferError

        scp.close()

        src_hash = self._get_local_md5()
        dst_hash = self._get_remote_md5()

        if src_hash != dst_hash:
            raise FileHashMismatchError(self.src, self.dst, src_hash, dst_hash)
    def ftp_file(self, hostname=None, username=None, password=None):
        """Transfer the file to the remote device over FTP.

        Note:
            If any arguments are omitted, the corresponding attributes
            of the ``self.device`` will be used.

        Args:
            hostname (str): OPTIONAL - The name or
                IP address of the remote device.
            username (str): OPTIONAL - The SSH username
                for the remote device.
            password (str): OPTIONAL - The SSH password
                for the remote device.

        Raises:
            FileTransferError: if an error occurs during the file transfer.
            FileHashMismatchError: if the source and
                destination hashes don't match.
            FileNotReadableError: if the local file doesn't exist or isn't readable.
            FileNotEnoughSpaceError: if there isn't enough space on the device.
            FileRemoteDirDoesNotExist: if the remote directory doesn't exist.
        """
        self._safety_checks()

        hostname = hostname or self.device.host
        username = username or self.device.username
        password = password or self.device.password

        ftp = FTP()
        ftp.connect(hostname,21)
        ftp.login(username,password)
        bufsize=1024
        fp=open(self.src,'rb')
        try:
            ftp.storbinary('STOR ' + self.ftp_dst, fp, bufsize)
        except:
            raise FileTransferError
        fp.close()
        ftp.quit()

        src_hash = self._get_local_md5()
        dst_hash = self._get_remote_md5()

        if src_hash != dst_hash:
            raise FileHashMismatchError(self.src, self.dst, src_hash, dst_hash)
    def ftp_downloadfile(self, hostname=None, username=None, password=None):
        """Transfer the file to the remote device over FTP.

        Note:
            If any arguments are omitted, the corresponding attributes
            of the ``self.device`` will be used.

        Args:
            hostname (str): OPTIONAL - The name or
                IP address of the remote device.
            username (str): OPTIONAL - The SSH username
                for the remote device.
            password (str): OPTIONAL - The SSH password
                for the remote device.

        Raises:
            FileTransferError: if an error occurs during the file transfer.
            FileHashMismatchError: if the source and
                destination hashes don't match.
            FileNotReadableError: if the local file doesn't exist or isn't readable.
            FileNotEnoughSpaceError: if there isn't enough space on the device.
            FileRemoteDirDoesNotExist: if the remote directory doesn't exist.
        """
        hostname = hostname or self.device.host
        username = username or self.device.username
        password = password or self.device.password

        ftp = FTP()
        ftp.connect(hostname,21)
        ftp.login(username,password)
        ftp.set_debuglevel(2)
        bufsize=1024
        try:
            ftp.retrbinary('RETR ' + str(self.ftp_dst), open(str(self.src), 'wb').write)
        except:
            raise FileTransferError
        ftp.quit()

        src_hash = self._get_local_md5()
        dst_hash = self._get_remote_md5()

        if src_hash != dst_hash:
            raise FileHashMismatchError(self.src, self.dst, src_hash, dst_hash)
