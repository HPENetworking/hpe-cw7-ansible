.. _comware_bgp_af:


comware_bgp_af
++++++++++++++++++++++++++++

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Added in version 1.8

Manage address family configs such as ipv4 ipv6 .

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
        <td style="vertical-align:middle">autonomous_system</td>
        <td style="vertical-align:middle">yes</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Autonomous system number <1-4294967295></td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">bgp_instance</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Specify a BGP instance by its name</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">address_familys_ipv4uni</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle">false</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>true</li><li>false</li></td></td>
        <td style="vertical-align:middle;text-align:left">Specify the address-family ipv4 unicast </td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">address_familys_ipv6uni</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle">false</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>true</li><li>false</li></td></td>
        <td style="vertical-align:middle;text-align:left">Specify the address-family ipv6 unicast </td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">address_familys_vpnv4</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle">false</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>true</li><li>false</li></td></td>
        <td style="vertical-align:middle;text-align:left">Specify the VPNv4 address family</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">address_familys_vpnv6</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle">false</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>true</li><li>false</li></td></td>
        <td style="vertical-align:middle;text-align:left">Specify the VPNv6 address family</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">default_ipv4_local_pref</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Set the ipv4 default local preference value</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">default_ipv6_local_pref</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Set the ipv6 default local preference value</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">fast_reroute_frr_policy</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle">false</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>true</li><li>false</li></td></td>
        <td style="vertical-align:middle;text-align:left">Configure fast reroute policy</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">policy_vpn4_target</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle">true</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>true</li><li>false</li></td></td>
        <td style="vertical-align:middle;text-align:left">Filter VPN4 routes with VPN-Target attribute</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">policy_vpn6_target</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle">true</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>true</li><li>false</li></td></td>
        <td style="vertical-align:middle;text-align:left">Filter VPN6 routes with VPN-Target attribute</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">ipv4_route_select_delay</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Set the delay time for optimal route selection of ipv4</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">ipv6_route_select_delay</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Set the delay time for optimal route selection of ipv6</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">vpnv4_route_select_delay</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Set the delay time for optimal route selection of vpnv4</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">vpnv6_route_select_delay</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Set the delay time for optimal route selection of vpnv6</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">allow_invalid_as</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Apply the origin AS validation state to optimal route selection</td>
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

    
        
    # Basic bgp address-family config
    - comware_bgp_af: autonomous_system=10 bgp_instance=test address_familys_ipv4uni=true ipv4_route_select_delay=20 allow_invalid_as=true username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
    - comware_bgp_af: autonomous_system=10 bgp_instance=test address_familys_vpnv4=true policy_vpn4_target=true username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
    

    



.. note:: address family setting include ipv4 ipv6 etc. some of the configsneed address family ipv4 view , some need others , so ensure theview you provided meets the config requirestate default and absent are the same , if you want delete the setting configs ,the comware will undo the autonomous_system and instance .