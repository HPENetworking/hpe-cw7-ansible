.. _comware_netstream:


comware_netstream
++++++++++++++++++++++++++++

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Added in version 1.0

Manage ip netstream,rate,timeout, max_entry,vxlan udp-port,and interface enable and ip netstream aggregation destination-prefix enable,netstream statistics output message destination address and destination UDP port number configurationonComware 7 devices

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
        <td style="vertical-align:middle">netstream</td>
        <td style="vertical-align:middle">yes</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">global netstream enable or disable</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">rate</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Configure output rate limit</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">timeout</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Active aging time of configuration flow</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">max_enter</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Active aging time of configuration flow</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">vxlan_udp</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Enable vxlan message statistics function</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">sampler</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Create a sampler.</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">mode</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>fixed</li><li>random</li></td></td>
        <td style="vertical-align:middle;text-align:left">Sampler mode.if config sampler,this parameter is must be exit.</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">sampler_rate</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Sampler rate. if config sampler,this parameter is must be exit.</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">version</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle">9</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>5</li><li>9</li><li>10</li></td></td>
        <td style="vertical-align:middle;text-align:left">Configure autonomous system options for netstream version.</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">BGP</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">BGP next hop option.</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">inactive</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Configure Inactive aging time of flow.(10~600).</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">source_intf</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Configure the source interface of netstream statistical output message.</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">aggregation</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>as</li><li>prefix</li></td></td>
        <td style="vertical-align:middle;text-align:left">Enter netstream aggregation view and enable it</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">name</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Full name of the interface</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">interface_enable</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>inbound</li><li>outbound</li></td></td>
        <td style="vertical-align:middle;text-align:left">manage interface netstream enable.To config this, name parameter must be exit.</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">interface_sampler</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">manage interface sampler.</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">host</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Configure the destination address of netstream statistical output message.</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">udp</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Configure the destination UDP port number of netstream statistical output message.</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">vpn_name</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Specify the VPN to which the destination address of netstream statistical output message belongs.</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">state</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle">present</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>present</li><li>absent</li></td></td>
        <td style="vertical-align:middle;text-align:left">Desired state for the interface configuration.</td>
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

    
        
    # netstream config
      - comware_netstream: netstream=enable rate=10 timeout=1 max_entry=2 vxlan_udp=8000 aggregation=prefix host=192.168.1.43 udp=29 state=present username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
    # delete netstream config
      - comware_netstream: netstream=enable rate=10 timeout=1 max_entry=2 vxlan_udp=8000 aggregation=prefix host=192.168.1.43 udp=29 state=absent username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
    

    



.. note:: Before configuring netstream stream image, you need to enable the global netstream function.The default state is not open global netstream function.If you want to config interface netstream enable,the name parametermust be exit.If you config netstream statistics output message,host and udp paramaters must be exit.