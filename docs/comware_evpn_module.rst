.. _comware_evpn:


comware_evpn
++++++++++++++++++++++++++++

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Added in version 1.8

Configure the EVPN issue to be applied to the device.

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
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Full name of the interface</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">vrf</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle">false</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">VPN instance name.</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">state</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle">present</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>present</li><li>absent</li></td></td>
        <td style="vertical-align:middle;text-align:left">Desired state for the interface configuration</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">rd</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle">false</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Route distinguisher</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">rtentry</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Route target</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">addrfamily</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>ipv4</li><li>ipv6</li><li>vpn</li><li>evpn</li></td></td>
        <td style="vertical-align:middle;text-align:left">Address family</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">rttype</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>import</li><li>export</li></td></td>
        <td style="vertical-align:middle;text-align:left">RT type</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">asnum</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>md5</li><li>hmac_sha_1</li><li>hmac_sha_256</li><li>hmac_sha_384</li><li>hmac_sha_384</li></td></td>
        <td style="vertical-align:middle;text-align:left">Autonomous System number</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">sessaf</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>ipv4</li><li>ipv6</li></td></td>
        <td style="vertical-align:middle;text-align:left">Address family of session</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">ipaddr</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle">false</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>true</li><li>false</li></td></td>
        <td style="vertical-align:middle;text-align:left">Address of session</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">ipadd</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Remote IPv4 or IPv6 address</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">mask</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Mask of session address</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">aftype</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>ipv4uni</li><li>ipv4mul</li><li>mdt</li><li>vpnv4</li><li>ipv6uni</li><li>ipv6mul</li><li>vpnv6</li><li>l2vpn</li><li>l2vpn_evpn</li><li>link_state</li><li>ipv4mvpn</li><li>ipv4flosp</li><li>vpnv4flosp</li><li>ipv6flosp</li><li>vpnv6flosp</li></td></td>
        <td style="vertical-align:middle;text-align:left">Address Family Identifier</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">family</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>ipv4uni</li><li>ipv4mul</li><li>mdt</li><li>vpnv4</li><li>ipv6uni</li><li>ipv6mul</li><li>vpnv6</li><li>l2vpn</li><li>l2vpn_evpn</li><li>link_state</li><li>ipv4mvpn</li><li>ipv4flosp</li><li>vpnv4flosp</li><li>ipv6flosp</li><li>vpnv6flosp</li></td></td>
        <td style="vertical-align:middle;text-align:left">Address Family Identifier of Neighbor</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">del_bgp</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>true</li><li>false</li></td></td>
        <td style="vertical-align:middle;text-align:left">Whether delete BGP</td>
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

    
        
    # configure evpn rt
    - comware_evpn: vrf=ali1 addrfamily=ipv4 rttype=export rtentry=30:2  username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
    # delete bgp
    - comware_evpn: del_bgp=true state=absent username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
    
    comware_evpn: bgp_name=10 vrf=200 asnum=120 mask=255 ipaddr=1.1.1.1 sessaf=ipv4 state=present username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
    

    



.. note:: The asnum is unsigned integer,and the value range is 1 to 4294967295.The type of vrf is string,the length is 1 to 31 characters.The type of mask is Unsigned integer,and the value range is 0 to 128,or 255.For non-dynamic peers, this is 255.For IPv4 dynamic peers,this is 0 to 32.For IPv6 dynamic peers, this is 0 to 128.Dynamic peers are not supported.if you want to config bgp  evpn   ,please use comware_bgp_global.py to create bgp process first.