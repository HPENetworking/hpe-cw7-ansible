.. _comware_command:


comware_command
++++++++++++++++++++++++++++

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Added in version 1.8

Execute CLI commands on Comware 7 devices

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
        <td style="vertical-align:middle">type</td>
        <td style="vertical-align:middle">yes</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>display</li><li>config</li><li>show</li></td></td>
        <td style="vertical-align:middle;text-align:left">State whether the commands are display (user view)              or configure (system view) commands.  Display and              show are the same thing.</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">command</td>
        <td style="vertical-align:middle">yes</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">String (single command) or list of commands to be              executed on the device.  Sending a list requires              YAML format to be used in the playbook.</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">file_txt</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Text file on server.              Include file path and file name.</td>
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

    
        
    # display vlan 10 passing in a string
    - comware_command: command='display vlan 5' type=display username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
    
    # execute command by using file
    - comware_command: file_txt=/root/ansible-hpe-cw7-master/test.txt type=config username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
    
    # display vlans passing in a list
    - comware_command:
        command:
          - display vlan 10
          - display vlan 5
        type: display
        username: "{{ username }}"
        password: "{{ password }}"
        hostname: "{{ inventory_hostname }}"
    
    # passing in config commands as a list
    - comware_command:
        command:
          - vlan 5
          - name web_vlan
        type: config
        username: "{{ username }}"
        password: "{{ password }}"
        hostname: "{{ inventory_hostname }}"
    

    



.. note:: This module is not idempotent