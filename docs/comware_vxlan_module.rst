.. _comware_vxlan:


comware_vxlan
+++++++++++++

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Added in version 1.8

Manage VXLAN to VSI mappings and Tunnel mappings to VXLAN

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
    <td style="vertical-align:middle">descr</td>
    <td style="vertical-align:middle">yes</td>
    <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"></ul></td>
        <td style="vertical-align:middle;text-align:left">
      description of the VSI<br>    </td>
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
    <td style="vertical-align:middle">tunnels</td>
    <td style="vertical-align:middle">no</td>
    <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"></ul></td>
        <td style="vertical-align:middle;text-align:left">
      Desired Tunnel interface ID or a list of IDs. Any tunnel not in the list will be removed if it exists<br>    </td>
    </tr>
            <tr style="text-align:center">
    <td style="vertical-align:middle">username</td>
    <td style="vertical-align:middle">yes</td>
    <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"></ul></td>
        <td style="vertical-align:middle;text-align:left">
      Username used to login to the switch<br>    </td>
    </tr>
            <tr style="text-align:center">
    <td style="vertical-align:middle">vsi</td>
    <td style="vertical-align:middle">yes</td>
    <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"></ul></td>
        <td style="vertical-align:middle;text-align:left">
      Name of the VSI<br>    </td>
    </tr>
            <tr style="text-align:center">
    <td style="vertical-align:middle">vxlan</td>
    <td style="vertical-align:middle">yes</td>
    <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"></ul></td>
        <td style="vertical-align:middle;text-align:left">
      VXLAN that will be mapped to the VSI<br>    </td>
    </tr>
        </table><br>


Examples
--------

.. raw:: html

    <br/>


::

    
    # ensure VXLAN and VSI do not exist
    - comware_vxlan: vxlan=100 vsi=VSI_VXLAN_100 tunnels=20 state=absent username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
    
    
    # ensure VXLAN 100 exists and is mapped to VSI VSI_VXLAN_100 with only tunnel interface 20
    - comware_vxlan: vxlan=100 vsi=VSI_VXLAN_100 tunnels=20 username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
    
    # ensure 3 tunnels mapped to the vxlan
    - comware_vxlan:
        vxlan: 100
        vsi: VSI_VXLAN_100
        tunnels: ['20', '21', '22']
        username: "{{ username }}"
        password: "{{ password }}"
        hostname: "{{ inventory_hostname }}"
    



.. note:: VXLAN tunnels should be created before using this module.
.. note:: state=absent removes the vsi and associated vxlan mapping if they both exist.
.. note:: Remember that is a 1 to 1 mapping between vxlan IDs and VSIs
