.. _comware_ospf_intf:


comware_ospf_intf
++++++++++++++++++++++++++++

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Added in version 1.0

Manage ospf in interface

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
        <td style="vertical-align:middle">name</td>
        <td style="vertical-align:middle">yes</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">full name of interface</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">ospfname</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Instance name.(1~65535)</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">ospfcost</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Configure the overhead required for the interface to run OSPF</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">area</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Specify the OSPF area</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">simplepwdtype</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>cipher</li><li>plain</li></td></td>
        <td style="vertical-align:middle;text-align:left">Specify the password type of ospf auth_mode simple</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">simplepwd</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Specify the password  of ospf auth_mode simple</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">keyid</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Specify the md5 or hwac-md5 key of ospf auth_mode</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">md5type</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>md5</li></td></td>
        <td style="vertical-align:middle;text-align:left">Specify the ospf auth_mode md5 type</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">md5pwdtype</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>cipher</li><li>plain</li></td></td>
        <td style="vertical-align:middle;text-align:left">Specify the password type of ospf auth_mode md5</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">md5pwd</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Specify the password of ospf auth_mode md5</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">network_type</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>broadcast</li><li>nbma</li><li>p2p</li><li>p2mp</li></td></td>
        <td style="vertical-align:middle;text-align:left">Specify OSPF network type</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">state</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle">present</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>present</li><li>absent</li><li>default</li></td></td>
        <td style="vertical-align:middle;text-align:left">Desired state for the interface configuration</td>
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
        <td style="vertical-align:middle;text-align:left">The Comware port used to connect to the switch</td>
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

    
        
    # Basic Ethernet config
      ensure name (interface name) exists in device and the interface support ospf setting.
    - comware_ospf_intf: name=Ten-GigabitEthernet1/0/7 ospfname=1 area=0 ospfcost=10 network_type=p2p keyid=11 \
      md5type=md5 md5pwdtype=plain md5pwd=1 username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
    - comware_ospf_intf: name=Ten-GigabitEthernet1/0/7 state=default \
      username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

    



.. note:: The module is used to config interface ospf setting , before using the module , pleaseensure the interface exists and is able to make ospf setting .Interface ospf auth mode can config as simple or md5 , however these two mode can not beset at the same time.Some of the setting must be set together e.g. ospfname must together with area.state default or absent will delete all the ospf settings ,