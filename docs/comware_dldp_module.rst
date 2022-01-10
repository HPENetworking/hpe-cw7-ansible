.. _comware_dldp:


comware_dldp
++++++++++++++++++++++++++++

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Added in version 1.0

Manage dldp authentication,interface,timeout and mode  on Comware 7 devices.author: gongqianyu

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
        <td style="vertical-align:middle">global_enable</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle">disable</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">global dldp enable or disable</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">auth_mode</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Configure dldp authentication mode between current device and neighbor device.</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">pwd_mode</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Configure the dldp authentication password mode between the current device and the neighbor device.</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">pwd</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Configure the dldp authentication password between the current device and the neighbor device</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">timeout</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle">5</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Configure the sending interval of advertisement message(1~100)</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">shutdown_mode</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle">auto</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Global configuration of interface shutdown mode after dldp discovers unidirectional link.</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">name</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">The full name of the interface.</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">interface_enable</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Enable dldp function on the interface.</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">init_delay</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Delay time of dldp blocking interface from initial state to single pass state.(1~5)</td>
    </tr>
    </table><br>


Examples
--------

.. raw:: html

    <br/>


::

    
        
      - name: config dldp
            comware_dldp: global_enable=enable auth_mode=md5 shutdown_mode=auto pwd_mode=cipher pwd=123456 timeout=10 name=HundredGigE1/0/27 
                          interface_enable=disable state=present username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
      - name: delete dldp configuration
            comware_dldp: global_enable=enable auth_mode=md5 shutdown_mode=auto pwd_mode=cipher pwd=123456 timeout=10 name=HundredGigE1/0/27 
                          interface_enable=disable state=absent username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
    

    



.. note:: To enable the dldp feature, the dldp feature must be enabled on both the global and the interface.when config interface_enable、init_delay and port_shutdown,name must be exit.