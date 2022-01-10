.. _comware_patch:


comware_patch
++++++++++++++++++++++++++++

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Added in version 1.8

Rollback theconfiguration to the file

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
        <td style="vertical-align:middle">patchname</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Name of patch that will be used .</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">activate</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>false</li><li>true</li></td></td>
        <td style="vertical-align:middle;text-align:left">active patch or not.</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">check_result</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle">false</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>true</li><li>false</li></td></td>
        <td style="vertical-align:middle;text-align:left"></td>
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

    
        
          - name: copy version from ansible server into switch.
            comware_file_copy: file=/root/ansible-hpe-cw7-master/gqy/s6820-cmw710-system-weak-patch-f6205p05h16.bin remote_path=flash:/s6820-cmw710-system-weak-patch-f6205p05h16.bin username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
    
          - name: check bin is exit or not and active it.
            comware_patch: patchname=patch.bin activate=true username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
            async: 60
            poll: 0
    
          - name: check patch is active or not 
            comware_patch: patchname=s6805-cmw710-boot-r6607.bin check_result=true username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
    

    



.. note:: This modules rollback the config to startup.cfg, or the suppliedfilename, in flash. It is notchanging the config file to load on next boot.