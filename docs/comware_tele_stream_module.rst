.. _comware_tele_stream:


comware_tele_stream
++++++++++++++++++++++++++++

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Added in version 1.0

Manage telemetry global enable(disable) and telemetry stream timestamp enable(disable) and device-idon Comware 7 devices.Before config device-id,the timestamp must be enable.

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
        <td style="vertical-align:middle">glo_enable</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle">enable</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>enable</li><li>disable</li></td></td>
        <td style="vertical-align:middle;text-align:left">config global telemetry stream enable.The default state is enable.</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">timestamp</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle">disable</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>enable</li><li>disable</li></td></td>
        <td style="vertical-align:middle;text-align:left">config telemetry stream timestamp enable.The default state is disable.</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">timestamp</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">config telemetry stream timestamp enable.The default state is disable.config telemetry stream device-id.</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">state</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle">present</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>present</li><li>default</li></td></td>
        <td style="vertical-align:middle;text-align:left">Recovering the dufault state of telemetry stream</td>
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

    
        
      # telemetry config
      - comware_tele_stream:
          glo_enable: enable
          timestamp: enable
    	  deviceID: 10.10.10.1
          username: "{{ username }}"
          password: "{{ password }}"
          hostname: "{{ inventory_hostname }}"
          state: present
    

    



