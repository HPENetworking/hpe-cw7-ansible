.. _comware_file_copy:


comware_file_copy
+++++++++++++++++

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Added in version 1.8

Copy a local file to a remote Comware v7 device

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
    </tr>
            <tr style="text-align:center">
    <td style="vertical-align:middle">file</td>
    <td style="vertical-align:middle">yes</td>
    <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"></ul></td>
        <td style="vertical-align:middle;text-align:left">
      File (including absolute path of local file) that will be sent to the device<br>    </td>
    </tr>
            <tr style="text-align:center">
    <td style="vertical-align:middle">hostname</td>
    <td style="vertical-align:middle">yes</td>
    <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"></ul></td>
        <td style="vertical-align:middle;text-align:left">
      IP Address or hostname of the Comware v7 device that has NETCONF enabled<br>    </td>
    </tr>
            <tr style="text-align:center">
    <td style="vertical-align:middle">password</td>
    <td style="vertical-align:middle">yes</td>
    <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"></ul></td>
        <td style="vertical-align:middle;text-align:left">
      Password used to login to the switch<br>    </td>
    </tr>
            <tr style="text-align:center">
    <td style="vertical-align:middle">port</td>
    <td style="vertical-align:middle">no</td>
    <td style="vertical-align:middle">830</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"></ul></td>
        <td style="vertical-align:middle;text-align:left">
      NETCONF port number<br>    </td>
    </tr>
            <tr style="text-align:center">
    <td style="vertical-align:middle">remote_path</td>
    <td style="vertical-align:middle">no</td>
    <td style="vertical-align:middle">flash:/<file></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"></ul></td>
        <td style="vertical-align:middle;text-align:left">
      Full file path on remote Comware v7 device, e.g. flash:/myfile. If no directory is included in remote_path, flash will be prepended. If remote_path is omitted, flash will be prepended to the source file name.<br>    </td>
    </tr>
            <tr style="text-align:center">
    <td style="vertical-align:middle">username</td>
    <td style="vertical-align:middle">yes</td>
    <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"></ul></td>
        <td style="vertical-align:middle;text-align:left">
      Username used to login to the switch<br>    </td>
    </tr>
        </table><br>


Examples
--------

.. raw:: html

    <br/>


::

    
    # copy file
    - comware_file_copy: file=/usr/smallfile remote_path=flash:/otherfile username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
    



.. note:: If the remote directory doesn't exist, it will be automatically created.
