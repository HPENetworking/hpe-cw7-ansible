.. _comware_reboot:


comware_reboot
++++++++++++++

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Added in version 1.8

Offers ability to reboot Comware 7 devices instantly at a scheduled time, or after a given period of time

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
    <td style="vertical-align:middle">date</td>
    <td style="vertical-align:middle">no</td>
    <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"></ul></td>
        <td style="vertical-align:middle;text-align:left">
      Specify the date at which the reboot will take place. The time parameter is required to use this parameter. Format should be MM/DD/YYYY in quotes.<br>    </td>
    </tr>
            <tr style="text-align:center">
    <td style="vertical-align:middle">delay</td>
    <td style="vertical-align:middle">no</td>
    <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"></ul></td>
        <td style="vertical-align:middle;text-align:left">
      Delay (in minutes) to wait to reboot the device<br>    </td>
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
    <td style="vertical-align:middle">reboot</td>
    <td style="vertical-align:middle">yes</td>
    <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>true</li><li>false</li></ul></td>
        <td style="vertical-align:middle;text-align:left">
      Needs to be set to true to reboot the device<br>    </td>
    </tr>
            <tr style="text-align:center">
    <td style="vertical-align:middle">time</td>
    <td style="vertical-align:middle">no</td>
    <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"></ul></td>
        <td style="vertical-align:middle;text-align:left">
      Specify the time at which the reboot will take place. Format should be HH:MM enclosed in quotes.<br>    </td>
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

    
    # name: reboot immedidately
    - comware_reboot: reboot=true username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
    
    # name: reboot at 5:00
    - comware_reboot: reboot=true time="05:00" username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
    
    # name: reboot in 5 minutes
    - comware_reboot: reboot=true delay="05:00" username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
    
    # name: reboot at 22:00 on July 30 2015
    - comware_reboot: reboot=true time="22:00" date="07/10/2015" username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
    



.. note:: Time/date and delay are mutually exclusive parameters
.. note:: Time is required when specifying date
.. note:: Reboot must be set to true to reboot the device
.. note:: This module is not idempotent
