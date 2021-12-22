.. _comware_portchannel:


comware_portchannel
+++++++++++++++++++

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Added in version 1.8

Manage routed and bridged aggregation configurations on Comware 7 devices.  This includes physical interface configs for LACP.

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
    </tr>
            <tr style="text-align:center">
    <td style="vertical-align:middle">group</td>
    <td style="vertical-align:middle">yes</td>
    <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"></ul></td>
        <td style="vertical-align:middle;text-align:left">
      Group number to identify the Aggregate interface<br>    </td>
    </tr>
            <tr style="text-align:center">
    <td style="vertical-align:middle">hostname</td>
    <td style="vertical-align:middle">yes</td>
    <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"></ul></td>
        <td style="vertical-align:middle;text-align:left">
      IP Address or hostname of the Comware v7 device that has NETCONF enabled<br>    </td>
    </tr>
            <tr style="text-align:center">
    <td style="vertical-align:middle">lacp_edge</td>
    <td style="vertical-align:middle">no</td>
    <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>enabled</li><li>disabled</li></ul></td>
        <td style="vertical-align:middle;text-align:left">
      Determine if an LACP agg group should be an edge aggregate interface<br>    </td>
    </tr>
            <tr style="text-align:center">
    <td style="vertical-align:middle">lacp_mode</td>
    <td style="vertical-align:middle">no</td>
    <td style="vertical-align:middle">active</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>active</li><li>passive</li></ul></td>
        <td style="vertical-align:middle;text-align:left">
      If mode is set to LACP, the type operating mode can be selected. This  mode will then be set for all members in the group.<br>    </td>
    </tr>
            <tr style="text-align:center">
    <td style="vertical-align:middle">max_ports</td>
    <td style="vertical-align:middle">no</td>
    <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"></ul></td>
        <td style="vertical-align:middle;text-align:left">
      Maximum number of selected ports for the agg group<br>    </td>
    </tr>
            <tr style="text-align:center">
    <td style="vertical-align:middle">members</td>
    <td style="vertical-align:middle">no</td>
    <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"></ul></td>
        <td style="vertical-align:middle;text-align:left">
      COMPLETE Interface List that should be in the agg group. Full names should be used AND Interface names ARE case sensitive. For example, FortyGigE1/0/1 should NOT be written as fortygige1/0/1.  This is for safety.<br>    </td>
    </tr>
            <tr style="text-align:center">
    <td style="vertical-align:middle">min_ports</td>
    <td style="vertical-align:middle">no</td>
    <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"></ul></td>
        <td style="vertical-align:middle;text-align:left">
      Minimum number of selected ports for the agg group<br>    </td>
    </tr>
            <tr style="text-align:center">
    <td style="vertical-align:middle">mode</td>
    <td style="vertical-align:middle">no</td>
    <td style="vertical-align:middle">dynamic</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>static</li><li>dynamic</li></ul></td>
        <td style="vertical-align:middle;text-align:left">
      Mode of the Aggregate interface<br>    </td>
    </tr>
            <tr style="text-align:center">
    <td style="vertical-align:middle">password</td>
    <td style="vertical-align:middle">yes</td>
    <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"></ul></td>
        <td style="vertical-align:middle;text-align:left">
      Password used to login to the switch<br>    </td>
    </tr>
            <tr style="text-align:center">
    <td style="vertical-align:middle">port</td>
    <td style="vertical-align:middle">no</td>
    <td style="vertical-align:middle">830</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"></ul></td>
        <td style="vertical-align:middle;text-align:left">
      NETCONF port number<br>    </td>
    </tr>
            <tr style="text-align:center">
    <td style="vertical-align:middle">state</td>
    <td style="vertical-align:middle">no</td>
    <td style="vertical-align:middle">present</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>present</li><li>absent</li></ul></td>
        <td style="vertical-align:middle;text-align:left">
      Desired state for the interface configuration<br>    </td>
    </tr>
            <tr style="text-align:center">
    <td style="vertical-align:middle">type</td>
    <td style="vertical-align:middle">yes</td>
    <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>bridged</li><li>routed</li></ul></td>
        <td style="vertical-align:middle;text-align:left">
      Type of the Aggregate interface (L2 or L3)<br>    </td>
    </tr>
            <tr style="text-align:center">
    <td style="vertical-align:middle">username</td>
    <td style="vertical-align:middle">yes</td>
    <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"></ul></td>
        <td style="vertical-align:middle;text-align:left">
      Username used to login to the switch<br>    </td>
    </tr>
        </table><br>


Examples
--------

.. raw:: html

    <br/>


::

    
      # Portchannel config
      - comware_portchannel:
          group: 100
          members:
            - FortyGigE1/0/27
            - FortyGigE1/0/28
            - FortyGigE1/0/29
            - FortyGigE1/0/30
          type: routed
          mode: static
          min_ports: 2
          max_ports: 4
          username: "{{ username }}"
          password: "{{ password }}"
          hostname: "{{ inventory_hostname }}"
          state: present
    



.. note:: When configuring a LAGG, the members param must be included
.. note:: Members is ALL members - it is ensuring that the members sent is the full list of all members.  This means to remove a member it just needs to be removed from the members list.
.. note:: When removing a LAGG, members is not required
.. note:: If mode is set to static, lacp_edge and lacp_mode are disregarded if those params are set
