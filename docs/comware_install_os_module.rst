.. _comware_install_os:


comware_install_os
++++++++++++++++++++++++++++

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Added in version 1.8

Offers ability to copy and install a new operating system on Comware v7devices.  Supports using .ipe or .bin system and boot packages.

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
        <td style="vertical-align:middle">ipe_package</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">File (including abs path path) of the local ipe package.</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">boot</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">File (including abs path) of the local boot package (.bin)</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">system</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">File (including abs path) of the local system package (.bin)</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">remote_dir</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle">flash:/</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">The remote directory into which the file(s) would be copied.              See default.</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">deafult</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>true</li><li>false</li><li>yes</li><li>no</li></td></td>
        <td style="vertical-align:middle;text-align:left"></td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">reboot</td>
        <td style="vertical-align:middle">yes</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>true</li><li>false</li><li>yes</li><li>no</li></td></td>
        <td style="vertical-align:middle;text-align:left">Determine if the reboot should take place              after device startup software image is configured</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">delay</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">If reboot is set to yes, this is the delay in minutes              to wait before rebooting.</td>
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

    
        
    # Basic Install OS IPE
    - comware_install_os: ipe_package=/usr/5900_5920_5930-CMW710-E2415.ipe reboot=true username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
    
    # Basic Install OS Boot/Sys
    - comware_install_os: reboot=yes boot=/usr/5930-cmw710-boot-e2415.bin system=/usr/5930-cmw710-system-e2415.bin username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
    

    



.. note:: The parameters ipe_package and boot/system aremutually exclusive.If the files are not currently on the device,they will be transfered to the device.