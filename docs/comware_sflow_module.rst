.. _comware_sflow:


comware_sflow
++++++++++++++++++++++++++++

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Added in version 1.0

Manage sflow attributes for Comware 7 devices

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
        <td style="vertical-align:middle">collectorID</td>
        <td style="vertical-align:middle">yes</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">the sflow collector id</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">addr</td>
        <td style="vertical-align:middle">yes</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">the ipv4 or ipv6 address </td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">vpn</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Name to configure for the specified vpn-instance</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">descr</td>
        <td style="vertical-align:middle">yes</td>
        <td style="vertical-align:middle">CLI Collector</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Description for the collectorID.must be exit</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">time_out</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">the collector's parameter aging time</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">Port</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle">6343</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">UDP port</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">data_size</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle">1400</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">the sflow datagram max size</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">agent_ip</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Configure the IP address of the sFlow agent.</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">sourceIpv4IP</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Configure the source IPV4 address of the sFlow message.</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">sourceIpv6IP</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Configure the source IPV6 address of the sFlow message.</td>
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

    
        # Basic  config
    - comware_sflow: collectorID=1 vpn=1 addr=1.1.1.1 data_size=500 descr=netconf time_out=1200 username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
    
    # delete config
    - comware_sflow: collectorID=1 addr=1.1.1.1 state=absent username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
    

    



