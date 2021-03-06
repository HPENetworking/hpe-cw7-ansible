.. _comware_irf_ports:


comware_irf_ports
++++++++++++++++++++++++++++

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Added in version 1.8

Manage IRF port creation and removal for Comware v7 devices

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
        <td style="vertical-align:middle">member_id</td>
        <td style="vertical-align:middle">yes</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">IRF member id for switch (must be unique).              IRF member ids can be configured with the comware_irf_members module.</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">irf_p1</td>
        <td style="vertical-align:middle">yes</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Physical Interface or List of Physical Interfaces that will be              bound to IRF port 1. Any physical interfaces not in the list will              be removed from the IRF port. An empty list removes all interfaces.</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">irf_p2</td>
        <td style="vertical-align:middle">yes</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Physical Interface or List of Physical Interfaces that will be              bound to IRF port 2. Any physical interfaces not in the list will              be removed from the IRF port. An empty list removes all interfaces.</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">filename</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle">startup.cfg</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Where to save the current configuration. Default is startup.cfg.</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">activate</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle">true</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>true</li><li>false</li><li>yes</li><li>no</li></td></td>
        <td style="vertical-align:middle;text-align:left">activate the IRF after the configuration is initially performed</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">removal_override</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle">false</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>true</li><li>false</li><li>yes</li><li>no</li></td></td>
        <td style="vertical-align:middle;text-align:left">When set to true, allows the removal of physical ports from IRF port(s).              Removing physical ports may have adverse effects and be disallowed by the switch.              Disconnecting all IRF ports could lead to a split-brain scenario.</td>
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

    
        
       # irf ports
       - comware_irf_ports:
          member_id: 1
          irf_p1:
            - FortyGigE1/0/1
            - FortyGigE1/0/3
          irf_p2: FortyGigE1/0/2
          username: "{{ username }}"
          password: "{{ password }}"
          hostname: "{{ inventory_hostname }}"
          removal_override: yes
    

    



.. note:: This module is meant to be run after the comware_irf_members module.The process is as follows 1) Use comware_irf_members to changethe IRF member identity of the device, with the reboot=trueflag, or reboot the device through some other means. 2) Usecomware_irf_members to change priority, description, and domain,if desired. 3) Use the comware_irf_ports module to create IRF portto physical port bindings, and set activate=true to activate theIRF. If IRF neighbors are already configured, the IRF will beformed, some devices may reboot.Any physical interfaces not in an interface list (irf_p1 or irf_p2) willbe removed from the IRF port. An empty list removes all interfaces.If an IRF is succesfully created, the non-master members will no longerbe accessible through their management interfaces.