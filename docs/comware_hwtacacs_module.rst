.. _comware_hwtacacs:


comware_hwtacacs
++++++++++++++++++++++++++++

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Added in version 1.8

Manage hwtacacs scheme

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
        <td style="vertical-align:middle">hwtacacs_scheme_name</td>
        <td style="vertical-align:middle">yes</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">hwtacacs scheme name</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">priority</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>primary</li><li>secondary</li></td></td>
        <td style="vertical-align:middle;text-align:left">Specify the primary or secondary HWTACACS server</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">auth_host_name</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Specify the primary HWTACACS authentication server name</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">auth_host_ip</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">authentication ip address</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">auth_host_port</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle">'49'</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">port number, 49 by default</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">author_host_name</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle">'49'</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Specify the primary HWTACACS authorization server name</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">author_host_ip</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">authorization ip address</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">author_host_port</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle">'49'</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">port number, 49 by default</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">acct_host_name</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Specify the primary HWTACACS accounting server name</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">acct_host_ip</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">accounting ip address</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">acct_host_port</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle">'49'</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">port number, 49 by default</td>
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

    
        
    # config hwtacacs scheme
    - comware_hwtacacs: hwtacacs_scheme_name=test priority=primary auth_host_ip=192.168.1.186 auth_host_port=48 username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
    

    



.. note:: authentication host name can not set together with authentication ipauthorization host name can not set together with authorization ipaccounting host name can not set together with accounting ip