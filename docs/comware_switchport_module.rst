.. _comware_switchport:


comware_switchport
++++++++++++++++++++++++++++

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Added in version 1.0

Manage Layer 2 parameters on switchport interfaces

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
        <td style="vertical-align:middle">yes</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Full name of the interface</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">link_type</td>
        <td style="vertical-align:middle">yes</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>access</li><li>trunk</li><li>hybrid</li></td></td>
        <td style="vertical-align:middle;text-align:left">Layer 2 mode of the interface</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">pvid</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">If link_type is set to trunk this will be used as the native              native VLAN ID for that trunk. If link_type is set to access              then this is the VLAN ID of the interface.</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">permitted_vlans</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">If mode is set to trunk this will be the complete list/range              (as a string) of VLANs allowed on that trunk interface.              E.g. 1-3,5,8-10              Any VLAN not in the list              will be removed from the interface.</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">untaggedvlan</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">              E.g. 1-3,5,8-10</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">taggedvlan</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">              E.g. 1-3,5,8-10</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">state</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle">present</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>present</li><li>default</li><li>absent</li></td></td>
        <td style="vertical-align:middle;text-align:left">Desired state of the switchport</td>
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

    
        
    # Basic access config
    - comware_switchport: name=FortyGigE1/0/2 link_type=access pvid=3 username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
    
    # Basic trunk config
    - comware_switchport: name=FortyGigE1/0/2 link_type=trunk permitted_vlans="1-3,5,8-10" username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
    

    



.. note:: If the interface is configured to be a Layer 3 port, the modulewill fail and ask the user to use the comware_interface moduleto convert it to be a Layer 2 port first.If the interface is a member in a LAG, the module will failtelling the user changes hould be made to the LAG interfaceIf VLANs are trying to be assigned that are not yet created onthe switch, the module will fail asking the user to createthem first.If state=default, the switchport settings will be defaulted.That means it will be set as an access port in VLAN 1.