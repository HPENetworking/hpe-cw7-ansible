.. _comware_vxlan_vsi:


comware_vxlan_vsi
++++++++++++++++++++++++++++

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Added in version 1.8

Manage the mapping of an Ethernet Service to a VSI (VXLAN ID)

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
        <td style="vertical-align:middle">vsi</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Name of the VSI</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">interface</td>
        <td style="vertical-align:middle">yes</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Layer 2 interface or bridged-interface</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">instance</td>
        <td style="vertical-align:middle">yes</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Service instance id</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">encap</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle">default</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>default</li><li>tagged</li><li>untagged</li></td></td>
        <td style="vertical-align:middle;text-align:left">only-tagged also ensures s-vid</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">vlanid</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">If encap is set to only-tagged or s-vid, vlanid must be set.</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">access_mode</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle">vlan</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>ethernet</li><li>vlan</li></td></td>
        <td style="vertical-align:middle;text-align:left">Mapping Ethernet service instance to a VSI using Ethernet              or VLAN mode (options for xconnect command)</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">state</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle">present</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>present</li><li>absent</li></td></td>
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

    
        
    # ensure the vsi is not mapped to the instance
    - comware_vxlan_svc_instance: interface=Fo1/0/32 vsi=VSI_VXLAN_100 instance=100 state=absent username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
    
    # ensure instance and vsi and configured with encap and access mode as specified
    - comware_vxlan_svc_instance: interface=Fo1/0/32 vsi=VSI_VXLAN_100 instance=100 encap=default access_mode=vlan username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
    
    # ensure instance and vsi and configured with encap and access mode as specified
    - comware_vxlan_svc_instance: interface=Fo1/0/32 vsi=VSI_VXLAN_100 instance=100 encap=tagged access_mode=ethernet username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
    
    # ensure instance and vsi and configured with encap and access mode as specified
    - comware_vxlan_svc_instance: interface=Fo1/0/32 vsi=VSI_VXLAN_100 instance=100 encap=only-tagged vlanid=10 state=present username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
    

    



.. note:: VSI needs to be created before using this module (comware_vxlan)encap and xconnect access_mode cannot be altered once setto change, use state=absent and re-configurestate=absent removes the service instance for specified interface ifif it existsThis should be the last VXLAN module used after comware_vxlan_tunnel,and comware_vxlan.