.. _comware_rollback:


comware_rollback
++++++++++++++++++++++++++++

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Added in version 1.8

Rollback theconfiguration to the file

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
        <td style="vertical-align:middle">filename</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle">startup.cfg</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Name of file that will be used when rollback the conifg to flash.</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">comparefile</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Name of file that will be used when compared with filename file.               if not set, no compared action executed.</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">clean</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle">false</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>true</li><li>false</li></td></td>
        <td style="vertical-align:middle;text-align:left">delete the rollback point</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">diff_file</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">File that will be used to store the diffs.  Relative path is              location of ansible playbook. If not set, no diffs are saved.</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">hostname</td>
        <td style="vertical-align:middle">yes</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">IP Address or hostname of the Comware 7 device that has              NETCONF enabled</td>
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

    
        
    # rollback config to myfile.cfg (in flash)
    - comware_rollback: filename=myfile.cfg username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
    
    # rollback config to startup.cfg (in flash)
    - comware_rollback: username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
    
    # delete rollback point 123.cfg (in flash)
    - comware_rollback: filename=123.cfg clean=true username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
    
    # files compared
    - comware_rollback: filename=123.cfg comparefile=test.cfg username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
      diff_file='/root/ansible-hpe-cw7-master/diffs.diff'

    



.. note:: This modules rollback the config to startup.cfg, or the suppliedfilename, in flash. It is notchanging the config file to load on next boot.