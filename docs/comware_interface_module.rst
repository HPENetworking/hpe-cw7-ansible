.. _comware_interface:


comware_interface
+++++++++++++++++

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
    </tr>
            <tr style="text-align:center">
    <td style="vertical-align:middle">admin</td>
    <td style="vertical-align:middle">no</td>
    <td style="vertical-align:middle">up</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>up</li><li>down</li></ul></td>
        <td style="vertical-align:middle;text-align:left">
      Admin state of the interface<br>    </td>
    </tr>
            <tr style="text-align:center">
    <td style="vertical-align:middle">description</td>
    <td style="vertical-align:middle">no</td>
    <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"></ul></td>
        <td style="vertical-align:middle;text-align:left">
      Single line description for the interface<br>    </td>
    </tr>
            <tr style="text-align:center">
    <td style="vertical-align:middle">duplex</td>
    <td style="vertical-align:middle">no</td>
    <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>auto</li><li>full</li></ul></td>
        <td style="vertical-align:middle;text-align:left">
      Duplex of the interface<br>    </td>
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
    <td style="vertical-align:middle">name</td>
    <td style="vertical-align:middle">yes</td>
    <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"></ul></td>
        <td style="vertical-align:middle;text-align:left">
      Full name of the interface<br>    </td>
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
      The Comware port used to connect to the switch<br>    </td>
    </tr>
            <tr style="text-align:center">
    <td style="vertical-align:middle">speed</td>
    <td style="vertical-align:middle">no</td>
    <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"></ul></td>
        <td style="vertical-align:middle;text-align:left">
      Speed of the interface in Mbps<br>    </td>
    </tr>
            <tr style="text-align:center">
    <td style="vertical-align:middle">state</td>
    <td style="vertical-align:middle">no</td>
    <td style="vertical-align:middle">present</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>present</li><li>absent</li><li>default</li></ul></td>
        <td style="vertical-align:middle;text-align:left">
      Desired state for the interface configuration<br>    </td>
    </tr>
            <tr style="text-align:center">
    <td style="vertical-align:middle">type</td>
    <td style="vertical-align:middle">no</td>
    <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>bridged</li><li>routed</li></ul></td>
        <td style="vertical-align:middle;text-align:left">
      Type of interface, i.e. L2 or L3<br>    </td>
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





.. note:: Only logical interfaces can be removed with state=absent.
.. note:: If you want to configure type (bridged or routed), run this module first with no other interface parameters. Then, remove the type parameter and include the other desired parameters. When the type parameter is given, other parameters are defaulted.
.. note:: When state is set to default, the interface will be "defaulted" regardless of what other parameters are entered.
.. note:: When state is set to default, the interface must already exist.
.. note:: When state is set to absent, logical interfaces will be removed from the switch, while physical interfaces will be "defaulted"
.. note:: Tunnel interface creation and removal is not currently supported.
