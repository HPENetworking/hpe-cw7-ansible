.. _comware_igmp:


comware_igmp
++++++++++++++++++++++++++++

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Added in version 1.8

-Configure the acl igmp to be applied to the interface.

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
        <td style="vertical-align:middle">igstate</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>enabled</li><li>disabled</li></td></td>
        <td style="vertical-align:middle;text-align:left">The status of IGMP</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">state</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle">present</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>present</li><li>absent</li></td></td>
        <td style="vertical-align:middle;text-align:left">Desired state for the interface configuration</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">version</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle">version2</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>version1</li><li>version2</li><li>version3</li></td></td>
        <td style="vertical-align:middle;text-align:left">The version of IGMP</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">snstate</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle">disable</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>enable</li><li>disable</li></td></td>
        <td style="vertical-align:middle;text-align:left">The state of igmp-snooping </td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">mode</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>sm</li><li>dm</li></td></td>
        <td style="vertical-align:middle;text-align:left">The mode of PIM</td>
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

    
        
    # create IGMP and configure IGMP version
    - comware_igmp: name=HundredGigE1/2/2 igstate=enabled version=version1 state=present username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
    # delete IGMP ,delete IGMP version
    - comware_igmp: name=hun1/2/2 igstate=disabled state=absent username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
    # configure PIM mode
    -  comware_igmp: name=hun1/2/2 mode=dm state=present username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
    # delete PIM mode
    -  comware_igmp: name=hun1/2/2 mode=dm state=absent username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
    # configure IMGP-Snooping
    - comware_igmp: snstate=enable state=present username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
    # delete IMGP-Snooping
    - comware_igmp: snstate=disable state=absent username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

    



.. note:: When configuring IGMP,the interface must be a routing interface.Parameter 'name' is required when deleting IGMP.