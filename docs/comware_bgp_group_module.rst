.. _comware_bgp_group:


comware_bgp_group
++++++++++++++++++++++++++++

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Added in version 1.8

create and config bgp group

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
        <td style="vertical-align:middle">bgp</td>
        <td style="vertical-align:middle">yes</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Autonomous system number <1-4294967295></td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">instance</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Specify a BGP instance by its name</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">group</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Create a peer group</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">group_type</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>external</li><li>internal</li></td></td>
        <td style="vertical-align:middle;text-align:left">Group type , include external and internal</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">peer</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Specify BGP peers , a group or peer ID</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">peer_connect_intf</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle">false</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Set interface name to be used as session's output interface</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">peer_in_group</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Specify a peer-group </td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">address_family</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>l2vpn</li></td></td>
        <td style="vertical-align:middle;text-align:left">Specify an address family , only l2vpn can be config here</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">evpn</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle">false</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>true</li><li>false</li></td></td>
        <td style="vertical-align:middle;text-align:left">Specify the EVPN address family</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">policy_vpn_target</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle">enable</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>enable</li><li>disable</li></td></td>
        <td style="vertical-align:middle;text-align:left">Filter VPN routes with VPN-Target attribute</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">reflect_client</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle">false</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>false</li></td></td>
        <td style="vertical-align:middle;text-align:left">Configure the peers as route reflectors</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">peer_group_state</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>false</li></td></td>
        <td style="vertical-align:middle;text-align:left">Enable or disable the specified peers</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">state</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle">present</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>present</li><li>default</li></td></td>
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

    
             # - name:  config bgp and create group
           # comware_bgp_group: bgp=200 group=evpn  group_type=internal   username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
         # - name:  config peer connet interface
           # comware_bgp_group: bgp=200 peer=evpn peer_connect_intf=LoopBack0  username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
         # - name:  join peer in the group
           # comware_bgp_group: bgp=200 peer=1.1.1.1 peer_in_group=evpn  username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
         # - name:  join peer in the group
           # comware_bgp_group: bgp=200 peer=3.3.3.3 peer_in_group=evpn  username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
         # - name:  create address-family view and config it
           # comware_bgp_group: bgp=200 address_family=l2vpn evpn=true policy_vpn_target=disable peer=evpn reflect_client=true  peer_group_state=true  \
           username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
         # - name:  remove bgp
           # comware_bgp_group: bgp=200 state=default username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

    



.. note:: Connect interface must be exist in the device if you want use it.If you want join a peer in a group , the group must be already exist.bgp with and without instance are in different view , carefully config it.