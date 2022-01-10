.. _comware_ntp:


comware_ntp
++++++++++++++++++++++++++++

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Added in version 1.8

-Configure the ntp issue to be applied to the device.

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
        <td style="vertical-align:middle">ntpenable</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle">false</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>true</li><li>false</li></td></td>
        <td style="vertical-align:middle;text-align:left">The status of NTP</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">state</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle">present</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>present</li><li>absent</li></td></td>
        <td style="vertical-align:middle;text-align:left">Desired state for the interface configuration</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">ntpauthenable</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle">false</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>true</li><li>false</li></td></td>
        <td style="vertical-align:middle;text-align:left">The status of NTP authentication</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">stratum</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">The stratum level of the local clock</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">service</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>ntp</li><li>sntp</li></td></td>
        <td style="vertical-align:middle;text-align:left">The service of NTP </td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">keyid</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">The authentication-keys of NTP</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">authmode</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>md5</li><li>hmac_sha_1</li><li>hmac_sha_256</li><li>hmac_sha_384</li><li>hmac_sha_384</li></td></td>
        <td style="vertical-align:middle;text-align:left">Authentication mode</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">authkey</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Authentication key</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">reliable</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle">false</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>true</li><li>false</li></td></td>
        <td style="vertical-align:middle;text-align:left">Whether the key is a trusted key.</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">ipadd</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Remote IPv4 or IPv6 address</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">del_rel_alone</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>true</li><li>false</li></td></td>
        <td style="vertical-align:middle;text-align:left">Whether delete trusted key alone</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">del_auth_all</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>true</li><li>false</li></td></td>
        <td style="vertical-align:middle;text-align:left">Whether delete all trusted key configurations</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">hostmode</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>symactive</li><li>client</li></td></td>
        <td style="vertical-align:middle;text-align:left">Client mode</td>
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

    
        
    # configure NTP authentication 
    - comware_ntp: service=ntp keyid=42 authmode=md5 authkey=anicekey reliable=true username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
    # configure NTP reference clock
    - comware_ntp: stratum=2 username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
    # configure NTP client
    - comware_ntp: service=ntp keyid=42 hostmode=client ipadd=10.1.1.1 name=hun1/2/2 username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
    # delete trusted keys alone
    - comware_ntp: state=absent del_rel_alone=true service=ntp keyid=42 reliable=false  username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
    # delete all verfication keys
    - comware_ntp: state=absent service=ntp keyid=42 del_auth_all=true  username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

    



.. note:: When configurating clients, IPv6 does not support.The keyid is unsigned integer,and the value range is 1 to 4294967295.The type of authkey is string,the length is 1 to 32 characters.The stratum is unsigned integer,and the value range is 1 to 15.