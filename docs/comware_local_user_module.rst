.. _comware_local_user:


comware_local_user
++++++++++++++++++++++++++++

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Added in version 1.8

Manage local_user

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
        <td style="vertical-align:middle">localusername</td>
        <td style="vertical-align:middle">yes</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Local user name</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">group</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">User group name</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">group</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>true</li><li>false</li></td></td>
        <td style="vertical-align:middle;text-align:left">User group nameenable or disable local user service-type ftp</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">group</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>true</li><li>false</li></td></td>
        <td style="vertical-align:middle;text-align:left">User group nameenable or disable local user service-type ftpenable or disable local user service-type http</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">group</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>true</li><li>false</li></td></td>
        <td style="vertical-align:middle;text-align:left">User group nameenable or disable local user service-type ftpenable or disable local user service-type httpenable or disable local user service-type https</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">group</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>true</li><li>false</li></td></td>
        <td style="vertical-align:middle;text-align:left">User group nameenable or disable local user service-type ftpenable or disable local user service-type httpenable or disable local user service-type httpsenable or disable local user service-type pad</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">group</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>true</li><li>false</li></td></td>
        <td style="vertical-align:middle;text-align:left">User group nameenable or disable local user service-type ftpenable or disable local user service-type httpenable or disable local user service-type httpsenable or disable local user service-type padenable or disable local user service-type ssh</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">group</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>true</li><li>false</li></td></td>
        <td style="vertical-align:middle;text-align:left">User group nameenable or disable local user service-type ftpenable or disable local user service-type httpenable or disable local user service-type httpsenable or disable local user service-type padenable or disable local user service-type sshenable or disable local user service-type telnet</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">group</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>true</li><li>false</li></td></td>
        <td style="vertical-align:middle;text-align:left">User group nameenable or disable local user service-type ftpenable or disable local user service-type httpenable or disable local user service-type httpsenable or disable local user service-type padenable or disable local user service-type sshenable or disable local user service-type telnetenable or disable local user service-type Terminal</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">ftp_dir</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Specify work directory of local user</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">local_user_level</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Specify local user work level</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">localspassword</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Password used to login to the local user</td>
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
    - Before using ftp_dir , ensure it already exist in the device.   e.g. flash:/
    - comware_local_user: localusername=test server_ftp=True local_user_level=15 username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
    

    



.. note:: Before using ftp_dir , ensure it already exist in the device.Local user group specify the user group , if the device has the group then do the config ,if not , create group and config