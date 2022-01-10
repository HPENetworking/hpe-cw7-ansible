.. _comware_startup:


comware_startup
++++++++++++++++++++++++++++

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Added in version 1.8

Offers ability to config the restart file or config image or patch for the device.Supports using .ipe or .bin system and boot packages.

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
        <td style="vertical-align:middle">patch</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">File (including abs path) of the local patch package (.bin)</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">deafult</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>true</li><li>false</li><li>yes</li><li>no</li></td></td>
        <td style="vertical-align:middle;text-align:left"></td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">nextstartupfile</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Name of file that will be used for the next start.</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">filename</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Name of file that will be show content.</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">show_file</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">File that will be used to store the config file content.  Relative path is              location of ansible playbook. If not set, no file saved.</td>
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

    
        
    #Basic Install OS Bootsys
      comware_startup:
        boot='flash:/s9850_6850-cmw710-boot-r6555p01.bin'
        system='flash:/s9850_6850-cmw710-system-r6555p01.bin'
        patch='flash:/s9850_6850-cmw710-system-patch-r6555p01h31.bin'
        username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
          
    #Basic Install OS IPE
      comware_startup: 
        ipe_package='flash:/s9850-h3c.ipe'
        username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
             
    #Config next startup file
      comware_startup: 
        nextstartupfile='flash:/123.cfg'
        username={{ username }} password={{ password }} hostname={{ inventory_hostname }} 
          
    #Show content for the existing config file
      comware_startup: filename='flash:/123.cfg' show_file='/root/ansible-hpe-cw7-master/123.cfg' username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

    



.. note:: The parameters ipe_package and boot/system aremutually exclusive.makesure the files are already existing on the device.