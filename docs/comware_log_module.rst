.. _comware_log:


comware_log
++++++++++++++++++++++++++++

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Added in version 1.8

get the device diagnostic information and upload to file server

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
        <td style="vertical-align:middle">service_dir</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">the dir in server which you want to upload the diag file from device</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">flash</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle">'flash:/'</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"></td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">ftpupload</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle">true</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>true</li><li>false</li></td></td>
        <td style="vertical-align:middle;text-align:left">whether upload the diagnostic information to the service.</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">servertype</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>ftp</li><li>scp</li></td></td>
        <td style="vertical-align:middle;text-align:left">choose the diagnostic file upload server type.</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">server_hostname</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">the remote server hostname e.g.192.168.1.199.</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">server_name</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">the name to login in remote server.</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">server_pwd</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">the password to login in remote server.</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">dst_dir</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">remote dir where the file save.</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">state</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>present</li><li>default</li><li>loadtoserver</li></td></td>
        <td style="vertical-align:middle;text-align:left">The state of operation</td>
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

    
        
    # e.g.ensure the dir exsits
          - name: get diagnostic information to the file server
            comware_log:  diag_dir=flash:/diaglog service_dir=/root/ansible-hpe-cw7-master/diaglog/ ftpupload=true 
            username={{ username }} password={{ password }} hostname={{ inventory_hostname }}     
                  
          - name: delete diagnostic information in device
            comware_log:  state=loadtoserver servertype=ftp server_hostname=192.168.1.199 server_name=fc server_pwd=111111 
            diag_dir=flash:/diaglog service_dir=/root/ansible-hpe-cw7-master/diaglog/ dst_dir= 
            username={{ username }} password={{ password }} hostname={{ inventory_hostname }} 
                                           
          # - name: delete diagnostic information in device
            # comware_log:  state=loadtoserver servertype=scp server_hostname=192.168.1.185 server_name=h3c server_pwd=h3c 
            diag_dir=flash:/diaglog service_dir=/root/ansible-hpe-cw7-master/diaglog/ dst_dir=flash:/ 
            username={{ username }} password={{ password }} hostname={{ inventory_hostname }} 
            
          - name: delete diagnostic information in device
            comware_log:  diag_dir=flash:/diaglog state=default username={{ username }} password={{ password }} hostname={{ inventory_hostname }} 
            

    



.. note:: Getting device diagnostic information will take some time , here give 300s to get the information,if result goes to time out , check the timeout 300s first.if state is present , you will get the diag file with .tar.gz , and it will upload to ansibleserver.-