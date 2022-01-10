.. _comware_portchannel:


comware_portchannel
++++++++++++++++++++++++++++

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Added in version 1.0

Manage routed and bridged aggregation configurations on Comware 7devices.  This includes physical interface configs for LACP.

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
        <td style="vertical-align:middle">group</td>
        <td style="vertical-align:middle">yes</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Group number to identify the Aggregate interface</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">members</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">COMPLETE Interface List that should be in the agg group.              Full names should be used AND Interface names ARE case              sensitive. For example, FortyGigE1/0/1 should NOT be written              as fortygige1/0/1.  This is for safety.</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">mode</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle">dynamic</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>static</li><li>dynamic</li></td></td>
        <td style="vertical-align:middle;text-align:left">Mode of the Aggregate interface.If you want to Configure the port rate as a condition for selecting the               reference port first, require it.</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">type</td>
        <td style="vertical-align:middle">yes</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>bridged</li><li>routed</li></td></td>
        <td style="vertical-align:middle;text-align:left">Type of the Aggregate interface (L2 or L3)</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">lacp_mode</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle">active</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>active</li><li>passive</li></td></td>
        <td style="vertical-align:middle;text-align:left">If mode is set to LACP, the type operating mode can be selected.              This  mode will then be set for all members in the group.</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">hash_mode</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">            -Hash mode  for the agg group.             some mode cannot config use netconfig,like 'flexible' and 'per-packet'.</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">min_ports</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Minimum number of selected ports for the agg group</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">max_ports</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Maximum number of selected ports for the agg group</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">lacp_edge</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>enabled</li><li>disabled</li></td></td>
        <td style="vertical-align:middle;text-align:left">Determine if an LACP agg group should be an edge aggregate              interface</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">s_mlag</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Determine if add agg group into s_mlag group.If you want to collocate lacp system-mac,              you must require it</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">speed</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>enabled</li><li>disabled</li></td></td>
        <td style="vertical-align:middle;text-align:left">Configure the port rate as a condition for selecting the reference port first.The default state is port ID               as a condition for selecting the reference port first.Before configure it, the agg group interface must                be dynamic agg interface.</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">state</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle">present</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>present</li><li>absent</li></td></td>
        <td style="vertical-align:middle;text-align:left">Desired state for the interface configuration</td>
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

    
        
      # Portchannel config
      -  comware_portchannel: group=100 members=HundredGigE1/0/3 mode=static type=bridged lacp_mode=active hash_mode=source-ip min_ports=2 max_ports=4 lacp_edge=enabled s_mlag=1 speed=enabled state=present username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
    #delete config
      -  comware_portchannel: group=100 members=HundredGigE1/0/3 mode=static type=bridged lacp_mode=active hash_mode=source-ip min_ports=2 max_ports=4 lacp_edge=enabled s_mlag=1 speed=enabled state=absent username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
      

    



.. note:: When configuring a LAGG, the members param must be includedMembers is ALL membersit is ensuring that the members sentis the full list of all members.  This means to remove a memberit just needs to be removed from the members list.When removing a LAGG, members is not requiredIf mode is set to static, lacp_edge and lacp_mode are disregardedif those params are set