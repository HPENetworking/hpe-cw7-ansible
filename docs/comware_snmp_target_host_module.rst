.. _comware_snmp_target_host:


comware_snmp_target_host
++++++++++++++++++++++++++++

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Added in version 1.8

Manages SNMP target host configuration on H3c switches.

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

    
        - name: Config SNMP v3 TagetHost
      comware_snmp_target_host:
        state=absent target_type=trap server_address=10.1.1.1 usm_user_name=Uv3
        sercurity_model=v3 security_level=authentication vpnname=testvpn
        username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
              
    - name: Undo SNMP v3 TagetHost
      comware_snmp_target_host:
        state=absent target_type=trap server_address=10.1.1.1 usm_user_name=Uv3
        vpnname=testvpn
        username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
    
    - name: Config SNMP TagetHost
      comware_snmp_target_host:
        state=present target_type=trap server_address=100.1.1.1 usm_user_name=testuv2c 
        sercurity_model=v2c
        username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
              
    - name: Undo SNMP TagetHost
      comware_snmp_target_host:
        state=present target_type=trap server_address=100.1.1.1 usm_user_name=testuv2c 
        sercurity_model=v2c vpnname=testvpn
        username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

    



