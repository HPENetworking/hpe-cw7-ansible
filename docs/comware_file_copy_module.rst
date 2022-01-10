.. _comware_file_copy:


comware_file_copy
++++++++++++++++++++++++++++

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Added in version 1.8

Copy a local file to a remote Comware v7 device

Options
-------

.. raw:: html

    <table border=1 cellpadding=4>
    <tr>
    <th class="head">parameter</th>
    <th class="head">required</th>
    <th class="head">default</th>
    <th class="head">choices</th>
    <th class="head">comments</th>
    </tr><tr style="text-align:center">
        <td style="vertical-align:middle">file</td>
        <td style="vertical-align:middle">yes</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">File (including absolute path of local file) that will be sent              to the device</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">flash</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle">flash:/<file></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">              If no directory is included in remote_path, flash will be prepended.              If remote_path is omitted, flash will be prepended to the source file name.</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">ftpupload</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle">false</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>true</li><li>false</li></td></td>
        <td style="vertical-align:middle;text-align:left">If you want to upload by FTP, change the params to true</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">ftpdownload</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle">false</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>true</li><li>false</li></td></td>
        <td style="vertical-align:middle;text-align:left">If you want to download by FTP, change the params to true</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">hostname</td>
        <td style="vertical-align:middle">yes</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">IP Address or hostname of the Comware v7 device that has              NETCONF enabled</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">username</td>
        <td style="vertical-align:middle">yes</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Username used to login to the switch</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">password</td>
        <td style="vertical-align:middle">yes</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Password used to login to the switch</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">port</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle">830</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">NETCONF port number</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">look_for_keys</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle">False</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Whether searching for discoverable private key files in ~/.ssh/</td>
    </tr>
    </table><br>


Examples
--------

.. raw:: html

    <br/>


::

    
        
    # copy file
    - comware_file_copy: file=/usr/smallfile remote_path=flash:/otherfile 
      username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
      
    - comware_file_copy: file=/root/ansible-hpe-cw7-master/hp-vlans.yml remote_path=flash:/ldx/hp-vlans.yml 
      ftpupload=true username={{ username }} password={{ password }}   hostname={{ inventory_hostname }}
      
    # name: use FTP to download files to the server--module 1.3
      comware_file_copy: file=/root/ansible-hpe-cw7-master/11.txt remote_path=flash:/llld/11.txt ftpdownload=true username={{ username }} password={{ password }}   hostname={{ inventory_hostname }}

    



.. note:: If the remote directory doesn't exist, it will be automaticallycreated.If you want to use FTP, you need to enable the FTP function on the device,e.g.[Sysname] local-user h3c class manage[Sysname-luser-manage-h3c] service-type ftp[Sysname] ftp server enableYou can configure it using the 'comware_local_user.py' and 'comware_ftp.py' modules first.