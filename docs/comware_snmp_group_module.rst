.. _comware_snmp_group:


comware_snmp_group
++++++++++++++++++++++++++++

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Added in version 1.8

Manages SNMP group configuration on H3C switches.

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

    
                 
    - name: "Config SNMP group"
       comware_snmp_group: state=present version=v2c group_name=wdz_group security_level=noAuthNoPriv acl_number=2000 
       username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
          
    - name: "Undo SNMP group"
      comware_snmp_group: state=absent  version=v2c group_name=wdz_group security_level=noAuthNoPriv acl_number=2000 
       username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
        
    - name: Config SNMP V3 group
        comware_snmp_group:
          state=present group_name=test_wl version=v3 security_level=authentication  acl_number=3000  write_view='testv3c'
          username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
          
    - name: Config SNMP V3 group
        comware_snmp_group:
          state=absent group_name=test_wl version=v3 security_level=authentication  acl_number=3000  write_view='testv3c'
          username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

    



