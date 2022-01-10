.. _comware_snmp_user:


comware_snmp_user
++++++++++++++++++++++++++++

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Added in version 1.8

Manages SNMP community configuration on H3C switches.

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

    
                 
    - name: Config SNMP v3 User
        comware_snmp_user:
          state=present usm_user_name=gtest_w_ansbile sercurity_model=v3 user_group=gtest_w_ansbile
          auth_protocol=sha priv_protocol=3des auth_key=gtest_w_ansbile priv_key=gtest_w_ansbile
          username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
    
    - name: undo SNMP v3 User
        comware_snmp_user:
          state=absent usm_user_name=gtest_w_ansbile sercurity_model=v3 user_group=gtest_w_ansbile
          auth_protocol=sha priv_protocol=3des auth_key=gtest_w_ansbile priv_key=gtest_w_ansbile
          username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
    
    - name: Config SNMP v2c User
        comware_snmp_user:
          state=present usm_user_name=gtest_w_ansbile sercurity_model=v2c user_group=gtest_w_ansbile
          username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
    
    - name: undo SNMP v2c User
        comware_snmp_user:
          state=absent usm_user_name=gtest_w_ansbile sercurity_model=v2c user_group=gtest_w_ansbile
          username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

    



