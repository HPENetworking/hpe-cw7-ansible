.. _comware_interface:


comware_interface
++++++++++++++++++++++++++++

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Added in version 1.8

Manage administrative state and physical attributes of the interface

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
        <td style="vertical-align:middle">admin</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle">up</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>up</li><li>down</li></td></td>
        <td style="vertical-align:middle;text-align:left">Admin state of the interface</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">admin</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Admin state of the interfaceSingle line description for the interface</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">type</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>bridged</li><li>routed</li></td></td>
        <td style="vertical-align:middle;text-align:left">Type of interface, i.e. L2 or L3</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">duplex</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>auto</li><li>full</li></td></td>
        <td style="vertical-align:middle;text-align:left">Duplex of the interface</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">speed</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Speed of the interface in Mbps</td>
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

    
        
    # Basic Ethernet config
    - comware_interface: name=FortyGigE1/0/5 admin=up description=mydesc duplex=auto speed=40000 username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
    - comware_interface: name=hun1/0/26.1 type=routed state=present username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

    



.. note:: Only logical interfaces can be removed with state=absent.If you want to configure type (bridged or routed),run this module first with no other interface parameters.Then, remove the type parameter and include the other desired parameters.When the type parameter is given, other parameters are defaulted.When state is set to default, the interface will be "defaulted"regardless of what other parameters are entered.When state is set to default, the interface must already exist.When state is set to absent, logical interfaces will be removedfrom the switch, while physical interfaces will be "defaulted"Tunnel interface creation and removal is not currently supported.