.. _comware_irf_members:


comware_irf_members
+++++++++++++++++++

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Added in version 1.8

Manage IRF member configuration.

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
    <td style="vertical-align:middle">auto_update</td>
    <td style="vertical-align:middle">no</td>
    <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>enable</li><li>disable</li></ul></td>
        <td style="vertical-align:middle;text-align:left">
      Whether software autoupdate should be enabled for the fabric.<br>    </td>
    </tr>
            <tr style="text-align:center">
    <td style="vertical-align:middle">descr</td>
    <td style="vertical-align:middle">no</td>
    <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"></ul></td>
        <td style="vertical-align:middle;text-align:left">
      The text description of the IRF member switch.<br>    </td>
    </tr>
            <tr style="text-align:center">
    <td style="vertical-align:middle">domain_id</td>
    <td style="vertical-align:middle">no</td>
    <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"></ul></td>
        <td style="vertical-align:middle;text-align:left">
      The domain ID for the IRF fabric.<br>    </td>
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
    <td style="vertical-align:middle">mad_exclude</td>
    <td style="vertical-align:middle">no</td>
    <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"></ul></td>
        <td style="vertical-align:middle;text-align:left">
      Interface or list of interfaces that should be excluded from shutting down in a recovery event.<br>    </td>
    </tr>
            <tr style="text-align:center">
    <td style="vertical-align:middle">member_id</td>
    <td style="vertical-align:middle">yes</td>
    <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"></ul></td>
        <td style="vertical-align:middle;text-align:left">
      Current IRF member ID of the switch. If the switch has not been configured for IRF yet, this should be 1.<br>    </td>
    </tr>
            <tr style="text-align:center">
    <td style="vertical-align:middle">new_member_id</td>
    <td style="vertical-align:middle">no</td>
    <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"></ul></td>
        <td style="vertical-align:middle;text-align:left">
      The desired IRF member ID for the switch. The new member ID takes effect after a reboot.<br>    </td>
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
    <td style="vertical-align:middle">priority</td>
    <td style="vertical-align:middle">no</td>
    <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"></ul></td>
        <td style="vertical-align:middle;text-align:left">
      The desired IRF priority for the switch.<br>    </td>
    </tr>
            <tr style="text-align:center">
    <td style="vertical-align:middle">reboot</td>
    <td style="vertical-align:middle">yes</td>
    <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>True</li><li>False</li><li>True</li><li>False</li></ul></td>
        <td style="vertical-align:middle;text-align:left">
      Whether to reboot the switch after member id changes are made.<br>    </td>
    </tr>
            <tr style="text-align:center">
    <td style="vertical-align:middle">state</td>
    <td style="vertical-align:middle">no</td>
    <td style="vertical-align:middle">present</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>present</li><li>absent</li></ul></td>
        <td style="vertical-align:middle;text-align:left">
      Desired state of the interfaces listed in mad_exclude<br>    </td>
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

    
      # irf members
      - comware_irf_members:
          member_id: 9
          state: present
          auto_update: disable
          mad_exclude:
            - FortyGigE9/0/30
            - FortyGigE9/0/23
            - FortyGigE9/0/24
          priority: 4
          descr: My description
          reboot: no
          username: "{{ username }}"
          password: "{{ password }}"
          hostname: "{{ inventory_hostname }}"
    



.. note:: This module should be used before the comware_irf_ports module.
.. note:: The process is as follows 1) Use comware_irf_members to change the IRF member identity of the device, with the reboot=true flag, or reboot the device through some other means. 2) Use comware_irf_members to change priority, description, and domain, if desired. 3) Use the comware_irf_ports module to create IRF port to physical port bindings, and set activate=true to activate the IRF. If IRF neighbors are already configured, the IRF will be formed, some devices may reboot.
.. note:: When state=absent, the interfaces in mad_exclude will be removed if present. Other parameters will be ignored.
