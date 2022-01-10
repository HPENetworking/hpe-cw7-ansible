.. _comware_syslog_global:


comware_syslog_global
++++++++++++++++++++++++++++

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Added in version 1.0

Manage system log timestamps and  terminal logging level on Comware 7 devices

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
        <td style="vertical-align:middle">timestamps</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle">date</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Configure the time stamp output format of log information sent to the console, monitoring terminal,                log buffer and log file direction.</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">level</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle">informational</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Configure the minimum level of log information that the current terminal allows to output.</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">state</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle">present</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>present</li><li>absent</li></td></td>
        <td style="vertical-align:middle;text-align:left">Desired state for the interface configuration</td>
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

    
        
      # timestamps and level config
      - comware_syslog_global: timestamps=boot  level=debugging username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
    
      # Restore timestamps and level to default state    
      - comware_syslog_global:timestamps=boot level=debugging username={{ username }} password={{ password }} hostname={{ inventory_hostname }} state=absent
    

    



.. note:: Before configuring this,the global syslog need to be enabled.The timestamps default state is data, terminal logging level default is 6.