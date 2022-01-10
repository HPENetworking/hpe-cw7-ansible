.. _comware_vrrp:


comware_vrrp
++++++++++++++++++++++++++++

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Added in version 1.0

Manage VRRP configurations on a Comware v7 deviceauthor:hanyangyang

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
        <td style="vertical-align:middle">vrid</td>
        <td style="vertical-align:middle">yes</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">VRRP group ID number</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">interface</td>
        <td style="vertical-align:middle">yes</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Full name of the Layer 3 interface</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">vip</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Virtual IP to assign within the group</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">priority</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">VRRP priority for the device</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">preempt</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>true</li><li>false</li></td></td>
        <td style="vertical-align:middle;text-align:left">Determine preempt mode for the device</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">auth_mode</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>simple</li><li>md5</li></td></td>
        <td style="vertical-align:middle;text-align:left">authentication mode for vrrp</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">key_type</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>cipher</li><li>plain</li></td></td>
        <td style="vertical-align:middle;text-align:left">Type of key, i.e. cipher or clear text</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">key</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">cipher or clear text string</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">delay</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Configure preemption delay time</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">track</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Configure the track entry specified for monitoring.</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">switch</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">when the status of the monitored track item changes to negative,               if the router is in backup status in the backup group, it will immediately switch to master router</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">state</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle">present</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>present</li><li>absent</li><li>shutdown</li><li>undoshutdown</li></td></td>
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

    
        
    # ensure vrid and vrip are configured
    - comware_vrrp: vrid=100 vip=100.100.100.1 interface=Vlan-interface100 username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
    
    # ensure vrid 100 is shutdown
    - comware_vrrp: vrid=100 interface=vlan100 state=shutdown username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
    
    # simple auth w/  plain text key
    - comware_vrrp: vrid=100 interface=vlan100 auth_mode=simple key_type=plain key=testkey username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
    
    # md5 auth w/ cipher
    - comware_vrrp: vrid=100 interface=vlan100 auth_mode=md5 key_type=cipher key='$c$3$d+Pc2DO3clxSA2tC6pe3UBzDEDl1dkE+voI=' username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
    
    # ensure vrid 100 on vlan 100 is removed
    - comware_vrrp: vrid=100 interface=vlan100 state=absent username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
    
    # auth mode simple                                                                                                                                                                         
    - comware_vrrp: vrid=100 vip=100.100.100.1 interface=HundredGigE1/0/27 auth_mode=simple key_type=cipher key=123456  username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
    
    # vrrp delay track & switch                                                                                                                                                                       
    - comware_vrrp: vrid=100 vip=100.100.100.1 interface=HundredGigE1/0/27 delay=20  track=1024 switch=10.10.10.1  username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

    



.. note:: When state is set to absent, the vrrp group for a specificinterface will be removed (if it exists)When state is set to shutdown, the vrrp group for a specificinterface will be shutdown. undoshutdown reverses this operationWhen sending a text password, the module is not idempotentbecause a hash is calculated on the switch. sending a cipherthat matches the one configured is idempotent.