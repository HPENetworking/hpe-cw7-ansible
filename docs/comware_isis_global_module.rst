.. _comware_isis_global:


comware_isis_global
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
        <td style="vertical-align:middle">isisID</td>
        <td style="vertical-align:middle">yes</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">create isis process</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">level</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle">Level-1-2</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Configure the level of the router,the default value is Level-1-2.</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">cost_style</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle">narrow</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>narrow</li><li>wide</li><li>compatible</li></td></td>
        <td style="vertical-align:middle;text-align:left">Configure the type of IS-IS overhead value, that is,             the type of destination path overhead value in the message received and sent by IS-IS.</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">spf_limit</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>true</li><li>false</li></td></td>
        <td style="vertical-align:middle;text-align:left">Indicates that it is allowed to receive a message with a destination path overhead value              greater than 1023. If this parameter is not specified, a message with an overhead value greater than              1023 will be discarded. This parameter is optional only when compatible or narrow compatible is specified.</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">network</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Network entity name of the configuration IS-IS process(X...X.XXXX....XXXX.00)</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">add_family</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>ipv4</li><li>ipv6</li></td></td>
        <td style="vertical-align:middle;text-align:left">Create IS-IS IPv4 or IPV6 address family and enter IS-IS IPv4 address family view</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">preference</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle">15</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Configure routing priority of IS-IS protocol(1~225),before config it,you need to               config add_family first.</td>
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
    - comware_isis_global: isisID=4 level=level-2 cost_style=narrow-compatible spf_limit=true network=10.0001.1010.1020.1030.00 
                    add_family=ipv4 preference=25 state=present username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
    
    # delete isis 4
    - comware_isis_global: isisID=4 level=level-2 cost_style=narrow-compatible spf_limit=true network=10.0001.1010.1020.1030.00 
                    add_family=ipv4 preference=25 state=absent username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
    

    



