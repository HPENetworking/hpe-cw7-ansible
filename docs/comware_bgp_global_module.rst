.. _comware_bgp_global:


comware_bgp_global
++++++++++++++++++++++++++++

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Added in version 1.8

config bgp configs in the bgp instance view such as routerid

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
        <td style="vertical-align:middle">router_id</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Router ID in IP address format</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">advertise_rib_active</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle">false</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>true</li><li>false</li></td></td>
        <td style="vertical-align:middle;text-align:left">Advertise the best route in IP routing table</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">timer_connect_retry</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Configure the session retry timer for all BGP peers</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">timer_hold</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Hold timer , Value of hold timer in seconds</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">compare_as_med</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Compare the MEDs of routes from different ASs</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">compare_as_med</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle">false</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>false</li></td></td>
        <td style="vertical-align:middle;text-align:left">Compare the MEDs of routes from different ASs</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">peer_ip</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Specify BGP peers IPv4 address</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">peer_as_num</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Specify BGP peers AS number</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">peer_ignore</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Disable session establishment with the peers</td>
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

    
        
    # bgp global views configs
    -  comware_bgp_global: autonomous_system=10 bgp_instance=test router_id=192.168.1.185 advertise_rib_active=true timer_connect_retry=100 timer_keepalive=100 timer_hold=301 \
       compare_as_med=true peer_ip=1.1.1.3 peer_as_num=10 peer_ignore=true username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
    

    



.. note:: all the configs except autonomous_system and bgp_instance are set in bgp instance view.timer keepalive and time hold must be set together .timer hold must be greater than 3 times timer keepalive.peer relations are need peer ip first.state default and absent are the same , if you want delete the setting configs , the comwarewill undo the autonomous_system and instance .