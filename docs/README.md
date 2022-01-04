# HPE COMWARE 7 Ansible Modules

The list of Ansible modules that has been developed can be broken down into two types of modules: read-only modules and read-write modules.  The read-write modules, or those that can implement a change on the system, can further be broken down into feature-level and system-level modules.

The list of modules can be seen below.

## Read-Only Modules

The following modules gather data from the switches.  They do **NOT** impact system or feature level configuration.

* comware_facts - gather device facts (characteristics) such as hostname, operating system (OS), serial number, uptime, localtime, list of interfaces, and hardware platform
* comware_neighbors - gather neighbor information
* comware_ping - test remote reachability to specific destinations from the switch

## Read-Write Modules

### System Modules

Several modules can be used to modify system level change on the HP Com7 devices.  They are listed here:

* comware_file_copy - copy file from local Ansible machine to remote switch
* comware_install_config - copy a valid config file for the desired switch model from local Ansible machine to remote switch and activates it to be the running configuration
* comware_install_os - copy OS (bin or ipe files) from local Ansible machine to switch, set image to load on next boot, and reboots switch
* comware_reboot - reboots switch
* comware_save - saves current config
* comware_clean_erase - factory defaults the switch (**BE CAREFUL!**)

### Feature Modules

Several modules can be used to modify feature level configuration on the HPE COMWARE 7 devices.  They are listed here:

* comware_command - send raw CLI command(s) to the device
* comware_interface - manage physical interface characteristics
* comware_ipinterface - manage Layer 3 interface attributes
* comware_switchport - manage Layer 2 interface attributes
* comware_vlan - manage VLAN attributes
* comware_portchannel - manage portchannels (LAGGs) and members
* comware_irf_members - manages IRF membership creation
* comware_irf_ports - manages IRF port creation and removal
* comware_vrrp - manage VRRP vrid (group) configuration
* comware_vrrp_global - manage VRRP global load-balancing method
* comware_l2vpn_global - enable/disable L2VPN globally
* comware_vxlan - manages the VXLAN to VSI mapping and associated tunnels
* comware_vxlan_tunnel - manages VXLAN tunnel interfaces (pre-req to comware_vxlan)
* comware_vxlan_svc_instance - manages interface level service instance and maps appropriate VSI, i.e. (xconnect)