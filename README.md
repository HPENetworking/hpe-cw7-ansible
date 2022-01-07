# Introduction

This project contains Ansible modules and Python3 library that can be used to automate HPE Comware 7 switches. The modules rely on NETCONF to communicate with the device for making configuration changes and getting operational data back such as LLDP neighbors, OS, serial number, uptime, and active interfaces on the device.

# Python Support
  * Python 3.7.4+
  
# Ansible Support
  * Ansible 2.10.4+

# Getting Started
To get started, see the [demo](demo/) for detailed steps.  
  
# Documentation
The [list](docs/README.md) of Ansible modules  and more detailed summary of each module can be found in [docs](docs/). **(Update soon)**

## ansible-doc
ansible-doc is a utility that offers users built-in "man-page-like" docs for Ansible modules.  
This is a great command line utility to reference to understand the parameters each module supports.  
```
ansible-doc -M library/ comware_vlan
```
The -M flag here specifies the directory in which the modules reside.   
The following output shows the result of checking the comware_vlan module document.  
```
$ ansible-doc comware_vlan
> COMWARE_VLAN

  Manage VLAN resources and attributes for Comware v7 devices

Options (= is mandatory):

- descr
        Description for the VLAN (Choices: ) [Default: None]

= hostname
        IP Address or hostname of the Comware v7 device that has
        NETCONF enabled (Choices: ) [Default: None]

- name
        Name to configure for the specified VLAN ID (Choices: )
        [Default: None]

= password
        Password used to login to the switch (Choices: ) [Default:
        None]

= port
        NETCONF port number (Choices: ) [Default: 830]

= username
        Username used to login to the switch (Choices: ) [Default:
        None]

= vlanid
        VLAN ID to configure (Choices: ) [Default: None]


# ensure VLAN 10 exists
- comware_vlan: vlanid=10 name=VLAN10_WEB descr=LOCALSEGMENT state=present username={{ username }} password={{ pas

# update name and descr
- comware_vlan: vlanid=10 name=WEB10 descr=WEBDESCR state=present username={{ username }} password={{ password }} 

# ensure VLAN 10 does not exist
- comware_vlan: vlanid=10 state=absent username={{ username }} password={{ password }} hostname={{ inventory_hostn
```




