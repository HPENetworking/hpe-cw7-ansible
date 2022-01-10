.. _comware_vsi:


comware_vsi
++++++++++++++++++++++++++++

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Added in version 1.8

Configure some command functions of vsi view

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
        <td style="vertical-align:middle">vsi</td>
        <td style="vertical-align:middle">yes</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Name of the VSI</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">gateway_intf</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">vsi view Gateway configuration interface </td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">gateway_subnet</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">vsi view Gateway configuration subnet </td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">gateway_mask</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">vsi view Gateway configuration subnet wild card mask</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">vxlan</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Specify a Virtual eXtensible LAN</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">encap</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>true</li><li>false</li></td></td>
        <td style="vertical-align:middle;text-align:left">Ethernet virtual private network module </td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">rd</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Configure a route distinguisher</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">vpn_target_auto</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>both</li><li>export</li><li>import</li></td></td>
        <td style="vertical-align:middle;text-align:left">Configure route targets</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">state</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle">present</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>present</li><li>absent</li></td></td>
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

    
             # - name:  config vsi
           # comware_vsi: vsi=vpna gateway_intf=Vsi-interface1 gateway_subnet=10.1.1.0 gateway_mask=0.0.0.255 vxlan=10 \
           encap=true rd=auto vpn_target_auto=both username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
           
         # - name:  delelte vsi configs
           # comware_vsi: vsi=vpna state=default username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
    

    



.. note:: l2vpn needs to enbled before config vsi view.If you want to use vsi gateway interface, it must be exist , you can use interface module to create it.when giving vsi and state is default , it will delete the given vsi config all.