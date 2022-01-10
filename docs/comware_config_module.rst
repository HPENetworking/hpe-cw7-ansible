.. _comware_config:


comware_config
++++++++++++++++++++++++++++

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Added in version 1.8

Back uo current configuration to the specified file

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
        <td style="vertical-align:middle">flash</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"></td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">arcstate</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle">absent</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>absent</li><li>present</li></td></td>
        <td style="vertical-align:middle;text-align:left">The switch of backup</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">filename</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle">my_file</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Backup file</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">replacefile</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Rolling file</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">repswitch</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>false</li><li>true</li></td></td>
        <td style="vertical-align:middle;text-align:left">Configure rollback switch</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">y_or_no</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>y</li><li>n</li></td></td>
        <td style="vertical-align:middle;text-align:left">Configure the switch to save the current configuration during rollback.</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">hostname</td>
        <td style="vertical-align:middle">yes</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">IP Address or hostname of the Comware 7 device that has              NETCONF enabled</td>
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

    
        
    
    
    # backup config to flash:/llld/ans.cfg (in flash)
    - comware_config: filename=ans arcstate=present filefolder=flash:/llld/ username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
    # rollback config to netconf.cfg and save the current configuration(in flash)
    - comware_config: repswitch=true replacefile=netconf.cfg y_or_no=y username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
    # rollback config to netconf.cfg and do not save the current configuration
    comware_config: replacefile=netconf.cfg  repswitch=true y_or_no=n username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
    

    



.. note:: This modules backup the config to specified file in specified flash.-You can use the specified file for configuration distribution.