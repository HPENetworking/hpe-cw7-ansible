.. _comware_acl:


comware_acl
++++++++++++++++++++++++++++

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Added in version 1.8

-Configure the acl issue to be applied to the interface.

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
        <td style="vertical-align:middle">state</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle">present</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>present</li><li>absent</li></td></td>
        <td style="vertical-align:middle;text-align:left">Desired state for the interface configuration</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">ruleid</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">The ID of rule</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">scripaddr</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left">Ip source address of rule</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">action</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>deny</li><li>permit</li></td></td>
        <td style="vertical-align:middle;text-align:left">Action of the rule</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">appdirec</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>inbound</li><li>outbound</li></td></td>
        <td style="vertical-align:middle;text-align:left">Direction Applied to the interface</td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">groupcg</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"><li>basic</li><li>advanced</li></td></td>
        <td style="vertical-align:middle;text-align:left">ACL groupacategory</td>
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

    
        
    # deploy advanced ACL (IPv4 advanced ACL 3000 to 3999)
    - comware_acl: aclid=3010  groupcg=advanced appdirec=inbound username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
    # deploy basic ACL (IPv4 basic ACL 2000 to 2999)
    - comware_acl: aclid=2010  groupcg=advanced appdirec=inbound username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
    # delete advanced ACL
    - comware_acl: aclid=3010 groupcg=advanced state=absent username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
    # create rule
    - comware_acl: aclid=3010 groupcg=advanced ruleid=0 action=deny scripaddr=10.1.1.1 username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
    # apply ACL to interface
    - comware_acl: aclid=3010 groupcg=advanced name=hun1/2/2 appdirec=inbound username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
    # delete rule
    - comware_acl: aclid=3010 ruleid=0 state=absent username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
    #delete interface ACL application
    - comware_acl: aclid=3010 name=hun1/2/2 appdirec=inbound state=absent username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

    



.. note:: When using this feature, "acliid" and "groupcg" are required parameters.You must select a groupcategory when configurating the acl.If you want to configure rule,you need to configure the acl first.The rule value range 0 to 65535.The value 65535 is an invalid rule ID.If you want to configure acl advanded,the acl id rang from 3000 to 3999.If you want to configure acl basic,the acl id rang from 2000 to 2999.When you want to create an rule, you must have a "aclid" and "action" and "scripaddr".When you want to apply an rule to the interface, you must configure "aclid" and "groupcg".You cannot have a "groupcg" parameter when deleting a rule.