.. _comware_isis_interface:


comware_isis_interface
++++++++++++++++++++++++++++

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Added in version 1.0

Manage isis for Comware 7 devicesauthor:gongqianyu

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
        <td style="vertical-align:middle;text-align:left">interface name</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">isisID</td>
        <td style="vertical-align:middle">yes</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">cSpecifies that IS-IS functions are enabled on the interface and configures the IS-IS                processes associated with the interface</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">level</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle">3</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>1</li><li>2</li><li>3</li></td></td>
        <td style="vertical-align:middle;text-align:left">Link adjacency type of configuration interface.</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">cost</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Configure the link cost value of IS-IS interface.(1锝?6777215)</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">routerid</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Configure the link cost value of IS-IS interface,to chose router.</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">silent</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>true</li><li>false</li></td></td>
        <td style="vertical-align:middle;text-align:left">Forbid the interface to send and receive IS-IS message.</td>
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
        <td style="vertical-align:middle">state</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle">present</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>present</li><li>absent</li></td></td>
        <td style="vertical-align:middle;text-align:left">Desired state of the vlan</td>
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

    
        
    # create sisi 4 and releated params.
    - comware_isis_interface: name=vlan-interface30 isisID=4 level=2 networkType=p2p cost=5 routerid=level-2 silent=true state=present 
                    username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
    
    # delete isis 4
    - comware_isis_interface: name=vlan-interface30 isisID=4 level=2 networkType=p2p cost=5 routerid=level-2 silent=true state=absent 
                    username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
    

    



