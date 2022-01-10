.. _comware_install_config:


comware_install_config
++++++++++++++++++++++++++++

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Added in version 1.8

Activate a new current-running config in realtime

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
        <td style="vertical-align:middle">config_file</td>
        <td style="vertical-align:middle">yes</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">File that will be sent to the device.  Relative path is              location of Ansible playbook.  Recommended to use              absolute path.</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">commit_changes</td>
        <td style="vertical-align:middle">yes</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>true</li><li>false</li></td></td>
        <td style="vertical-align:middle;text-align:left">Used to determine the action to take after transferring the              config to the switch.  Either activate using the rollback              feature or load on next-reboot.</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">diff_file</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">File that will be used to store the diffs.  Relative path is              location of ansible playbook. If not set, no diffs are saved.</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">port</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle">830</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">NETCONF port number</td>
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

    
        
    # install config file that will be the new running config
    - comware_install_config:
        config_file='/root/ansible-hpe-cw7-master/gqy/123.cfg'
        diff_file='/root/ansible-hpe-cw7-master/gqy/diffs.diff'
        commit_changes=true
        username={{ username }}
        password={{ password }}
        hostname={{ inventory_hostname }}
    

    



.. note:: Check mode copies config file to device and still generates diffsdiff_file must be specified to write diffs to a file, otherwise,only summarized diffs are returned from the modulecommit_changes must be true to apply changesthis module does an automatic backup of the existing configto the filename flash:/safety_file.cfgthis module does an auto save to flash:/startup.cfg upon completionconfig_file MUST be a valid FULL config file for a given device.