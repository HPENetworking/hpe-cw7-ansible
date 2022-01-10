# HPE Networking Comware 7 Ansible Docs
### *Network Automation with HPE and Ansible*

---
### Requirements
* Comware 7 and NETCONF support
* Python 3.7.4+
* Ansible 2.10.4+

---
### Modules

  * [comware_ping - ping remote destinations *from* the comware 7 switch](#comware_ping)
  * [comware_vrrp - manages vrrp configurations on a comware v7 device](#comware_vrrp)
  * [comware_file_copy - copy local file to remote comware v7 device](#comware_file_copy)
  * [comware_install_os - copy (if necessary) and install a new operating system on comware v7 device](#comware_install_os)
  * [comware_irf_ports - manages irf port creation and removal for comware v7 devices](#comware_irf_ports)
  * [comware_vxlan - manages vxlan to vsi mappings and tunnel mappings to vxlan](#comware_vxlan)
  * [comware_vlan - manage vlan attributes for comware 7 devices](#comware_vlan)
  * [comware_reboot - perform a reboot of a comware 7 device](#comware_reboot)
  * [comware_irf_members - manages irf membership configuration](#comware_irf_members)
  * [comware_l2vpn_global - manage global config state for l2vpn](#comware_l2vpn_global)
  * [comware_neighbors - retrieves active lldp neighbors (read-only)](#comware_neighbors)
  * [comware_ipinterface - manages ipv4/ipv6 addresses on interfaces](#comware_ipinterface)
  * [comware_switchport - manages layer 2 parameters on switchport interfaces](#comware_switchport)
  * [comware_install_config - activate a new current-running config in realtime](#comware_install_config)
  * [comware_vxlan_tunnel - manages vxlan tunnels on comware 7 devices](#comware_vxlan_tunnel)
  * [comware_command - execute cli commands on comware 7 devices](#comware_command)
  * [comware_interface - manages physical interface attributes](#comware_interface)
  * [comware_facts - gathers facts of comware 7 devices](#comware_facts)
  * [comware_save - save the running configuration](#comware_save)
  * [comware_portchannel - manages port-channel (lag) on comware 7 devices](#comware_portchannel)
  * [comware_vrrp_global - manages vrrp global configuration mode](#comware_vrrp_global)
  * [comware_vxlan_vsi - manages mapping of an ethernet service to a vsi (vxlan id)](#comware_vxlan_vsi)
  * [comware_clean_erase - factory default hp comware 7 device](#comware_clean_erase)
  * [comware_aaa - Manage AAA](#comware_aaa)
  * [comware_acl - Configure the acl issue to be applied to the interface](#comware_acl)
  * [comware_bfd - Manage bfd config](#comware_bfd)
  * [comware_bgp_af - Manage address family configs](#comware_bgp_af)
  * [comware_bgp_global - config bgp configs in the bgp instance view such as routerid](#comware_bgp_global)
  * [comware_bgp_group - create and config bgp group](#comware_bgp_group)
  * [comware_compare - Enter the configuration command and compare it with the expected result](#comware_compare)
  * [comware_config - Back uo current configuration to the specified file](#comware_config)
  * [comware_dldp - Manage dldp authentication,interface,timeout and mode  on Comware 7 devices](#comware_dldp)
  * [comware_evpn - Configure the EVPN issue to be applied to the device](#comware_evpn)
  * [comware_ftp - Configure device FTP function](#comware_ftp)
  * [comware_hwtacacs - Manage hwtacacs scheme](#comware_hwtacacs)
  * [comware_iface_stp - Manage stp config in interface](#comware_iface_stp)
  * [comware_igmp - Configure the igmp issue to be applied to the interface](#comware_igmp)
  * [comware_intfState - Check the port status. If there are undo shutdown ports but the field ports are down, list these inconsistent ports. If not, return OK](#comware_intfState)
  * [comware_isis_global - Manage isis for Comware 7 devices](#comware_isis_global)
  * [comware_isis_interface -  Manage isis for Comware 7 devices](#comware_isis_interface)
  * [comware_lacp - Manage lacp system priority, system mac on Comware 7 devices](#comware_lacp)
  * [comware_license - loading device license](#comware_license)
  * [comware_lldp - Manage lacp fast-Interval, tx-interval,hold-multplier on Comware 7 devices](#comware_lldp)
  * [comware_lldp_global - Manage global config state for LLDP.this funtion can be take effect only global and interface LLDP all open. The interface LLDP is open default](#comware_lldp_global)
  * [comware_lldp_interface - Manage lldp enable on interfaces.The default state is enable](#comware_lldp_interface)
  * [comware_local_user - Manage local_user](#comware_local_user)
  * [comware_log - get the device diagnostic information and upload to file server](#comware_log)
  * [comware_log_source - Manage output rules for log information on V7 devices](#comware_log_source)
  * [comware_loghost - Manage info-center log host and related parameters on V7 devices](#comware_loghost)
  * [comware_mtu - Manage mtu and jumboframe of the interface](#comware_mtu)
  * [comware_netconf - Manage netconf log and xml function on Comware 7 devices.XML cfg not support enter xml view now,This is not normally done](#comware_netconf)
  * [comware_netstream - Manage ip netstream,rate,timeout, max_entry,vxlan udp-port,and interface enable and ip netstream aggregation destination-prefix enable, netstream statistics output message destination address and destination UDP port number configurationon  Comware 7 devices](#comware_netstream)
  * [comware_ntp - Configure the ntp issue to be applied to the device](#comware_ntp)
  * [comware_ospf - Manage ospf](#comware_ospf)
  * [comware_ospf_intf - Manage ospf in interface](#comware_ospf_intf)
  * [comware_patch - Rollback the running configuration](#comware_patch)
  * [comware_radius - create radius scheme](#comware_radius)
  * [comware_rollback - Rollback the running configuration](#comware_rollback)
  * [comware_sflow - Manage sflow attributes for Comware 7 devices](#comware_sflow)
  * [comware_sflow_intf - Manage sflow interface flow collector and sampling_rate on Comware 7 devices](comware_sflow_intf)
  * [comware_snmp_community - Manages SNMP community configuration on H3C switches](#comware_snmp_community)
  * [comware_snmp_group - Manages SNMP group configuration on H3C switches.](#comware_snmp_group)
  * [comware_snmp_target_host - Manages SNMP user configuration on H3c switches](#comware_snmp_target_host)
  * [comware_snmp_user - Manages SNMP user configuration on H3c switches](#comware_snmp_user)
  * [comware_startup - config the next restart file or ipe .   patch function not available,please use patch module](#comware_startup)
  * [comware_stp - Manage stp global BPDU enable, working mode and tc-bpdu attack protection function](#comware_stp)
  * [comware_syslog_global - Manage system log timestamps and  terminal logging level on Comware 7 devices](#comware_syslog_global)
  * [comware_tele_stream - Manage telemetry global enable(disable) and telemetry stream timestamp enable(disable) and device-id on Comware 7 devices.Before config device-id,the timestamp must be enable](#comware_tele_stream)
  * [comware_teleFlowGroup_global - Manage telemetry flow group agingtime on Comware 7 devices.The default value is Varies by device](#comware_teleFlowGroup_global)
  * [comware_TelemetryFlowTrace - Manage Package information of the message sent to the collector on V7 devices](#comware_TelemetryFlowTrace)
  * [comware_vpn_instance - config instance rely ensure some instance configs can be set](#comware_vpn_instance)
  * [comware_vsi - Configure some command functions of vsi view](#comware_vsi)
  * [comware_vsi_intf - Configure some functions of vsi-interface](#comware_vsi_intf)

---

## comware_ping
Ping remote destinations *from* the Comware 7 switch

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Ping remote destinations *from* the Comware 7 device.  Really helpful for reachability testing.

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| username  |   no  |  | <ul></ul> |  Username used to login to the switch  |
| hostname  |   yes  |  | <ul></ul> |  IP Address or hostname of the Comware v7 device that has NETCONF enabled  |
| host  |   yes  |  | <ul></ul> |  IP or name (resolvable by the switch) that you want to ping  |
| vrf  |   no  |  | <ul></ul> |  VRF instance pings should be sourced from  |
| password  |   no  |  | <ul></ul> |  Password used to login to the switch  |
| port  |   yes  |  830  | <ul></ul> |  NETCONF port number  |


 
#### Examples

```

# test reachability to 8.8.8.8
- comware_ping: host=8.8.8.8 username={{ username }} password={{ password }} hostname={{ inventory_hostname }}


```



---


## comware_vrrp
Manages VRRP configurations on a Comware v7 device

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Manages VRRP configurations on a Comware v7 device

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| username  |   yes  |  | <ul></ul> |  Username used to login to the switch  |
| key_type  |   no  |  | <ul> <li>cipher</li>  <li>plain</li> </ul> |  Type of key, i.e. cipher or clear text  |
| hostname  |   yes  |  | <ul></ul> |  IP Address or hostname of the Comware v7 device that has NETCONF enabled  |
| state  |   no  |  present  | <ul> <li>present</li>  <li>absent</li>  <li>shutdown</li>  <li>undoshutdown</li> </ul> |  Desired state for the interface configuration  |
| vrid  |   yes  |  | <ul></ul> |  VRRP group ID number  |
| preempt  |   no  |  | <ul> <li>true</li>  <li>false</li> </ul> |  Determine preempt mode for the device  |
| auth_mode  |   no  |  | <ul> <li>simple</li>  <li>md5</li> </ul> |  authentication mode for vrrp  |
| priority  |   no  |  | <ul></ul> |  VRRP priority for the device  |
| vip  |   no  |  | <ul></ul> |  Virtual IP to assign within the group  |
| key  |   no  |  | <ul></ul> |  cipher or clear text string  |
| interface  |   yes  |  | <ul></ul> |  Full name of the Layer 3 interface  |
| password  |   yes  |  | <ul></ul> |  Password used to login to the switch  |
| port  |   yes  |  830  | <ul></ul> |  NETCONF port number  |


 
#### Examples

```

# ensure vrid and vrip are configured
- comware_vrrp: vrid=100 vip=100.100.100.1 interface=vlan100 username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

# ensure vrid 100 is shutdown
- comware_vrrp: vrid=100 interface=vlan100 state=shutdown username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

# simple auth w/  plain text key
- comware_vrrp: vrid=100 interface=vlan100 auth_mode=simple key_type=plain key=testkey username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

# md5 auth w/ cipher
- comware_vrrp: vrid=100 interface=vlan100 auth_mode=md5 key_type=cipher key='$c$3$d+Pc2DO3clxSA2tC6pe3UBzDEDl1dkE+voI=' username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

# ensure vrid 100 on vlan 100 is removed
- comware_vrrp: vrid=100 interface=vlan100 state=absent username={{ username }} password={{ password }} hostname={{ inventory_hostname }}


```


#### Notes

- When state is set to absent, the vrrp group for a specific interface will be removed (if it exists)

- When state is set to shutdown, the vrrp group for a specific interface will be shutdown. undoshutdown reverses this operation

- When sending a text password, the module is not idempotent because a hash is calculated on the switch. sending a cipher that matches the one configured is idempotent.


---


## comware_file_copy
Copy local file to remote Comware v7 device

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Copy local file to remote Comware v7 device

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| username  |   yes  |  | <ul></ul> |  Username used to login to the switch  |
| hostname  |   yes  |  | <ul></ul> |  IP Address or hostname of the Comware v7 device that has NETCONF enabled  |
| remote_path  |   no  |  flash:/<file>  | <ul></ul> |  Full file path on remote Comware v7 device, e.g. flash:/myfile. If no directory is included, flash will be prepended.  |
| file  |   yes  |  | <ul></ul> |  File (including absolute path of local file) that will be sent to the device  |
| password  |   yes  |  | <ul></ul> |  Password used to login to the switch  |
| port  |   yes  |  830  | <ul></ul> |  NETCONF port number  |


 
#### Examples

```

# copy file
- comware_file_copy: file=/usr/smallfile remote_path=flash:/otherfile username={{ username }} password={{ password }} hostname={{ inventory_hostname }}


```


#### Notes

- If the remote directory doesn't exist, it will be automatically created.


---


## comware_install_os
Copy (if necessary) and install a new operating system on Comware v7 device

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Offers ability to copy and install a new operating system on Comware v7 devices.  Supports using .ipe or .bin system and boot packages.

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| username  |   yes  |  | <ul></ul> |  Username used to login to the switch  |
| delete_ipe  |   no  |  | <ul> <li>true</li>  <li>false</li>  <li>yes</li>  <li>no</li> </ul> |  If ipe_package is used, this specifies whether the .ipe file is deleted from the device after it is unpacked.  |
| hostname  |   yes  |  | <ul></ul> |  IP Address or hostname of the Comware v7 device that has NETCONF enabled  |
| boot  |   no  |  | <ul></ul> |  File (including abs path) of the boot package (.bin)  |
| system  |   no  |  | <ul></ul> |  File (including abs path) of the system package (.bin)  |
| reboot  |   yes  |  | <ul> <li>true</li>  <li>false</li>  <li>yes</li>  <li>no</li> </ul> |  Determine if the reboot should take place after device startup software image is configured  |
| delay  |   no  |  | <ul></ul> |  If reboot is set to yes, this is the delay in minutes to wait before rebooting.  |
| remote_dir  |   no  |  flash:/  | <ul></ul> |  The remote directory into which the file(s) would be copied. See default.  |
| ipe_package  |   no  |  | <ul></ul> |  File (including abs path path) of the ipe package.  |
| password  |   yes  |  | <ul></ul> |  Password used to login to the switch  |
| port  |   yes  |  830  | <ul></ul> |  NETCONF port number  |


 

#### Notes

- The parameters ipe_package and boot/system are mutually exclusive.

- If the files are not currently on the device, the will be transfered to the device.


---


## comware_irf_ports
Manages IRF port creation and removal for Comware v7 devices

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Manages IRF port creation and removal for Comware v7 devices

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| username  |   yes  |  | <ul></ul> |  Username used to login to the switch  |
| password  |   yes  |  | <ul></ul> |  Password used to login to the switch  |
| activate  |   no  |  True  | <ul> <li>true</li>  <li>false</li>  <li>yes</li>  <li>no</li> </ul> |  activate the IRF after the configuration is initially performed  |
| hostname  |   yes  |  | <ul></ul> |  IP Address or hostname of the Comware v7 device that has NETCONF enabled  |
| irf_p2  |   yes  |  | <ul></ul> |  Physical Interface or List of Physical Interfaces that will be bound to IRF port 2. Any physical interfaces not in the list will be removed from the IRF port. An empty list removes all interfaces.  |
| irf_p1  |   yes  |  | <ul></ul> |  Physical Interface or List of Physical Interfaces that will be bound to IRF port 1. Any physical interfaces not in the list will be removed from the IRF port. An empty list removes all interfaces.  |
| member_id  |   yes  |  | <ul></ul> |  IRF member id for switch (must be unique). IRF member ids can be configured with the comware_irf_members module.  |
| filename  |   no  |  startup.cfg  | <ul></ul> |  Where to save the current configuration. Default is startup.cfg.  |
| port  |   yes  |  830  | <ul></ul> |  NETCONF port number  |
| removal_override  |   no  |  False  | <ul> <li>true</li>  <li>false</li>  <li>yes</li>  <li>no</li> </ul> |  When set to true, allows the removal of physical ports from IRF port(s). Removing physical ports may have adverse effects and be disallowed by the switch. Disconnecting all IRF ports could lead to a split-brain scenario.  |


 
#### Examples

```

   # irf ports
   - comware_irf_ports:
      member_id: 1
      irf_p1:
        - FortyGigE1/0/1
        - FortyGigE1/0/3
      irf_p2: FortyGigE1/0/2
      username: "{{ username }}"
      password: "{{ password }}"
      hostname: "{{ inventory_hostname }}"
      removal_override: yes


```


#### Notes

- This module is meant to be run after the comware_irf_members module.

- Any physical interfaces not in an interface list (irf_p1 or irf_p2) will be removed from the IRF port. An empty list removes all interfaces.

- If an IRF is succesfully created, the non-master members will no longer be accessible through their management interfaces.

- The process is as follows 1) Use comware_irf_members to change the IRF member identity of the device. 2) Use the reboot=true flag or reboot the device through some other means. 3) Use the comware_irf_ports module to create IRF port to physical port bindings. 4) In that module set activate=true to activate the IRF. If IRF neighbors are already configured, the IRF will be formed, some devices may reboot.


---


## comware_vxlan
Manages VXLAN to VSI mappings and Tunnel mappings to VXLAN

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Manages VXLAN to VSI mappings and Tunnel mappings to VXLAN

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| username  |   yes  |  | <ul></ul> |  Username used to login to the switch  |
| descr  |   yes  |  | <ul></ul> |  description of the VSI  |
| hostname  |   yes  |  | <ul></ul> |  IP Address or hostname of the Comware v7 device that has NETCONF enabled  |
| state  |   no  |  present  | <ul> <li>present</li>  <li>absent</li> </ul> |  Desired state for the interface configuration  |
| tunnels  |   no  |  | <ul></ul> |  Desired Tunnel interface ID or a list of IDs. Any tunnel not in the list will be removed if it exists  |
| vsi  |   yes  |  | <ul></ul> |  Name of the VSI  |
| password  |   yes  |  | <ul></ul> |  Password used to login to the switch  |
| port  |   yes  |  830  | <ul></ul> |  NETCONF port number  |
| vxlan  |   yes  |  | <ul></ul> |  VXLAN that will be mapped to the VSI  |


 
#### Examples

```

# ensure VXLAN and VSI do not exist
- comware_vxlan: vxlan=100 vsi=VSI_VXLAN_100 tunnels=20 state=absent username={{ username }} password={{ password }} hostname={{ inventory_hostname }}


# ensure VXLAN 100 exists and is mapped to VSI VSI_VXLAN_100 with only tunnel interface 20
- comware_vxlan: vxlan=100 vsi=VSI_VXLAN_100 tunnels=20 username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

# ensure 3 tunnels mapped to the vxlan
- comware_vxlan:
    vxlan: 100
    vsi: VSI_VXLAN_100
    tunnels: ['20', '21', '22']
    username: "{{ username }}"
    password: "{{ password }}"
    hostname: "{{ inventory_hostname }}"


```


#### Notes

- VXLAN tunnels should be created before using this module.

- state=absent removes the vsi and associated vxlan mapping if they both exist.

- Remember that is a 1 to 1 mapping between vxlan IDs and VSIs


---


## comware_vlan
Manage VLAN attributes for Comware 7 devices

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Manage VLAN attributes for Comware 7 devices

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| username  |   yes  |  | <ul></ul> |  Username used to login to the switch  |
| name  |   no  |  | <ul></ul> |  Name to configure for the specified VLAN ID  |
| descr  |   no  |  | <ul></ul> |  Description for the VLAN  |
| hostname  |   yes  |  | <ul></ul> |  IP Address or hostname of the Comware v7 device that has NETCONF enabled  |
| vlanid  |   yes  |  | <ul></ul> |  VLAN ID to configure  |
| password  |   yes  |  | <ul></ul> |  Password used to login to the switch  |
| port  |   yes  |  830  | <ul></ul> |  NETCONF port number  |


 
#### Examples

```

# ensure VLAN 10 exists
- comware_vlan: vlanid=10 name=VLAN10_WEB descr=LOCALSEGMENT state=present username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

# update name and descr
- comware_vlan: vlanid=10 name=WEB10 descr=WEBDESCR state=present username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

# ensure VLAN 10 does not exist
- comware_vlan: vlanid=10 state=absent username={{ username }} password={{ password }} hostname={{ inventory_hostname }}


```



---


## comware_reboot
Perform a reboot of a Comware 7 device

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Offers ability to reboot Comware 7 devices instantly at a scheduled time, or after a given period of time

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| username  |   no  |  | <ul></ul> |  Username used to login to the switch  |
| hostname  |   yes  |  | <ul></ul> |  IP Address or hostname of the Comware v7 device that has NETCONF enabled  |
| reboot  |   yes  |  | <ul> <li>true</li>  <li>false</li> </ul> |  Needs to be set to true to reboot the device  |
| delay  |   no  |  | <ul></ul> |  Delay (in minutes) to wait to reboot the device  |
| time  |   no  |  | <ul></ul> |  Specify the time at which the reboot will take place. Format should be HH:MM enclosed in quotes.  |
| date  |   no  |  | <ul></ul> |  Specify the date at which the reboot will take place. The time parameter is required to use this parameter. Format should be MM/DD/YYYY in quotes.  |
| password  |   no  |  | <ul></ul> |  Password used to login to the switch  |
| port  |   yes  |  830  | <ul></ul> |  NETCONF port number  |


 
#### Examples

```

# name: reboot immedidately
- comware_reboot: reboot=true username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

# name: reboot at 5:00
- comware_reboot: reboot=true time="05:00" username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

# name: reboot in 5 minutes
- comware_reboot: reboot=true delay="05:00" username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

# name: reboot at 22:00 on July 30 2015
- comware_reboot: reboot=true time="22:00" date="07/10/2015" username={{ username }} password={{ password }} hostname={{ inventory_hostname }}


```


#### Notes

- Time/date and delay are mutually exclusive parameters

- Time is required when specifying date

- Reboot must be set to true to reboot the device

- This module is not idempotent


---


## comware_irf_members
Manages IRF membership configuration

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Manages IRF member configuration.
 This module should be used before the comware_irf_ports module.
 The process is as follows 1) Use comware_irf_members to change the IRF member identity of the device. 2) Use the reboot=true flag or reboot the device through some other means. 3) Use the comware_irf_ports module to create IRF port to physical port bindings. 4) In that module set activate=true to activate the IRF. If IRF neighbors are already configured, the IRF will be formed, some devices may reboot.

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| username  |   yes  |  | <ul></ul> |  Username used to login to the switch  |
| priority  |   no  |  | <ul></ul> |  The desired IRF priority for the switch.  |
| descr  |   no  |  False  | <ul></ul> |  The text description of the IRF member switch.  |
| state  |   no  |  present  | <ul> <li>present</li>  <li>absent</li> </ul> |  Desired state of the interfaces listed in mad_exclude  |
| auto_update  |   no  |  | <ul> <li>enable</li>  <li>disable</li> </ul> |  Whether software autoupdate should be enabled for the fabric.  |
| hostname  |   yes  |  | <ul></ul> |  IP Address or hostname of the Comware v7 device that has NETCONF enabled  |
| reboot  |   yes  |  False  | <ul></ul> |  Whether to reboot the switch after member changes are made.  |
| new_member_id  |   no  |  | <ul></ul> |  The desired IRF member ID for the switch. The new member ID takes effect after a reboot.  |
| mad_exclude  |   no  |  | <ul></ul> |  Interface or list of interfaces that should be excluded from shutting down in a recovery event.  |
| member_id  |   yes  |  | <ul></ul> |  Current IRF member ID of the switch. If the switch has not been configured for IRF yet, this should be 1.  |
| password  |   yes  |  | <ul></ul> |  Password used to login to the switch  |
| port  |   yes  |  830  | <ul></ul> |  NETCONF port number  |


 
#### Examples

```

  # irf members
  - comware_irf_members:
      member_id: 9
      state: present
      auto_update: disable
      mad_exclude:
        - FortyGigE9/0/30
        - FortyGigE9/0/23
        - FortyGigE9/0/24
      priority: 4
      descr: My description
      reboot: no
      username: "{{ username }}"
      password: "{{ password }}"
      hostname: "{{ inventory_hostname }}"


```


#### Notes

- When state=absent, the interfaces in mad_exclude will be removed if present. Other parameters will be ignored.


---


## comware_l2vpn_global
Manage global config state for L2VPN

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Enable or Disable L2VPN on a HP Comware 7 device

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| username  |   yes  |  | <ul></ul> |  Username used to login to the switch  |
| state  |   yes  |  | <ul> <li>enabled</li>  <li>disabled</li> </ul> |  Desired state for l2vpn global configuration  |
| password  |   yes  |  | <ul></ul> |  Password used to login to the switch  |
| hostname  |   yes  |  | <ul></ul> |  IP Address or hostname of the Comware 7 device that has NETCONF enabled  |
| port  |   yes  |  830  | <ul></ul> |  NETCONF port number  |


 
#### Examples

```

# enable l2vpn globally
- comware_l2vpn_global: state=enabled username={{ username }} password={{ password }} hostname={{ inventory_hostname }}


```



---


## comware_neighbors
Retrieves active LLDP neighbors (read-only)

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Retrieves active LLDP neighbors (read-only)

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| username  |   yes  |  | <ul></ul> |  Username used to login to the switch  |
| password  |   yes  |  | <ul></ul> |  Password used to login to the switch  |
| hostname  |   yes  |  | <ul></ul> |  IP Address or hostname of the Comware v7 device that has NETCONF enabled  |
| neigh_type  |   no  |  lldp  | <ul> <li>lldp</li>  <li>cdp</li> </ul> |  type of neighbors  |
| port  |   yes  |  830  | <ul></ul> |  NETCONF port number  |


 
#### Examples

```

# get lldp neighbors
- comware_neighbors: username={{ username }} password={{ password }} hostname={{ inventory_hostname }}


```



---


## comware_ipinterface
Manages IPv4/IPv6 addresses on interfaces

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Manages IPv4/IPv6 addresses on interfaces

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| username  |   yes  |  | <ul></ul> |  Username used to login to the switch  |
| name  |   yes  |  | <ul></ul> |  Full name of the interface  |
| hostname  |   yes  |  | <ul></ul> |  IP Address or hostname of the Comware v7 device that has NETCONF enabled  |
| mask  |   yes  |  | <ul></ul> |  The network mask, in dotted decimal or prefix length notation. If using IPv6, only prefix length is supported.  |
| state  |   no  |  present  | <ul> <li>present</li>  <li>absent</li> </ul> |  Desired state of the switchport  |
| version  |   yes  |  v4  | <ul> <li>v4</li>  <li>v6</li> </ul> |  v4 for IPv4, v6 for IPv6  |
| password  |   yes  |  | <ul></ul> |  Password used to login to the switch  |
| port  |   yes  |  830  | <ul></ul> |  NETCONF port number  |
| addr  |   yes  |  | <ul></ul> |  The IPv4 or IPv6 address of the interface  |


 
#### Examples

```

# Basic IPv4 config
- comware_ipinterface: name=FortyGigE1/0/3 addr=192.168.3.5 mask=255.255.255.0 username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

# Basic IPv6 config
- comware_ipinterface: version=v6 name=FortyGigE1/0/3 addr=2001:DB8::1 mask=10 username={{ username }} password={{ password }} hostname={{ inventory_hostname }}


```


#### Notes

- If the interface is not configured to be a layer 3 port, the module will fail and the user should use the interface module to convert the interface with type=routed

- If state=absent, the specified IP address will be removed from the interface. If the existing IP address doesn't match the specified, the existing will not be removed.


---


## comware_switchport
Manages Layer 2 parameters on switchport interfaces

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Manages Layer 2 parameters on switchport interfaces

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| username  |   yes  |  | <ul></ul> |  Username used to login to the switch  |
| name  |   yes  |  | <ul></ul> |  Full name of the interface  |
| hostname  |   yes  |  | <ul></ul> |  IP Address or hostname of the Comware v7 device that has NETCONF enabled  |
| pvid  |   no  |  | <ul></ul> |  If link_type is set to trunk this will be used as the native native VLAN ID for that trunk. If link_type is set to access then this is the VLAN ID of the interface.  |
| state  |   no  |  present  | <ul> <li>present</li>  <li>absent</li> </ul> |  Desired state of the switchport  |
| permitted_vlans  |   no  |  | <ul></ul> |  If mode is set to trunk this will be the complete list/range of VLANs allowed on that trunk interface. Any VLAN not in the list will be removed from the interface.  |
| password  |   yes  |  | <ul></ul> |  Password used to login to the switch  |
| port  |   yes  |  830  | <ul></ul> |  NETCONF port number  |
| link_type  |   yes  |  | <ul> <li>access</li>  <li>trunk</li> </ul> |  Layer 2 mode of the interface  |


 
#### Examples

```

# Basic access config
- comware_switchport: name=FortyGigE1/0/2 link_type=access username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

# Basic trunk config
- comware_switchport: name=FortyGigE1/0/2 link_type=trunk username={{ username }} password={{ password }} hostname={{ inventory_hostname }}


```


#### Notes

- If the interface is configured to be a Layer 3 port, the module will fail and ask the user to use the comware_interface module to convert it to be a Layer 2 port first.

- If the interface is a member in a LAG, the module will fail telling the user changes hould be made to the LAG interface

- If VLANs are trying to be assigned that are not yet created on the switch, the module will fail asking the user to create them first.

- If state=default, the switchport settings will be defaulted. That means it will be set as an access port in VLAN 1.


---


## comware_install_config
Activate a new current-running config in realtime

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Activate a new current-running config in realtime

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| username  |   yes  |  | <ul></ul> |  Username used to login to the switch  |
| config_file  |   yes  |  | <ul></ul> |  File that will be sent to the device.  Relative path is location of Ansible playbook.  Recommended to use absolute path.  |
| hostname  |   yes  |  | <ul></ul> |  IP Address or hostname of the Comware 7 device that has NETCONF enabled  |
| diff_file  |   no  |  | <ul></ul> |  File that will be used to store the diffs.  Relative path is location of ansible playbook. If not set, no diffs are saved.  |
| password  |   yes  |  | <ul></ul> |  Password used to login to the switch  |
| port  |   yes  |  830  | <ul></ul> |  NETCONF port number  |
| commit_changes  |   yes  |  | <ul> <li>true</li>  <li>false</li> </ul> |  Used to determine the action to take after transferring the config to the switch.  Either activate using the rollback feature or load on next-reboot.  |


 
#### Examples

```

# install config file that will be the new running config
- comware_install_config:
    config_file='/home/ansible/projects/pyhpecw7comware/newconfig.cfg'
    diff_file='/home/ansible/projects/pyhpecw7comware/diffs.diff'
    commit_changes=true
    username={{ username }}
    password={{ password }}
    hostname={{ inventory_hostname }}


```


#### Notes

- Check mode copies config file to device and still generates diffs

- diff_file must be specified to write diffs to a file, otherwise, only summarized diffs are returned from the module

- commit_changes must be true to apply changes

- this module does an automatic backup of the existing config to the filename flash:/safety_file.cfg

- this module does an auto save to flash:/startup.cfg upon completion

- config_file MUST be a valid FULL config file for a given device.


---


## comware_vxlan_tunnel
Manages VXLAN tunnels on Comware 7 devices

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Manages VXLAN tunnels on Comware 7 devices

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| global_src  |   no  |  | <ul></ul> |  Global source address for VXLAN tunnels  |
| src  |   no  |  | <ul></ul> |  Source address or interface for the tunnel  |
| tunnel  |   yes  |  | <ul></ul> |  Tunnel interface identifier  |
| hostname  |   yes  |  | <ul></ul> |  IP Address or hostname of the Comware v7 device that has NETCONF enabled  |
| username  |   yes  |  | <ul></ul> |  Username used to login to the switch  |
| dest  |   no  |  | <ul></ul> |  Destination address for the tunnel  |
| state  |   no  |  present  | <ul> <li>present</li>  <li>absent</li> </ul> |  Desired state for the interface configuration  |
| password  |   yes  |  | <ul></ul> |  Password used to login to the switch  |
| port  |   yes  |  830  | <ul></ul> |  NETCONF port number  |


 
#### Examples

```

# ensure tunnel interface 20 exists for vxlan and configures a global source address (although it's not used here)
- comware_vxlan_tunnel: tunnel=20 global_src=10.10.10.10 src=10.1.1.1 dest=10.1.1.2 username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

# ensure tunnel interface 21
- comware_vxlan_tunnel: tunnel=21 src=10.1.1.1 dest=10.1.1.2 username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

# ensure tunnel interface 21 does not exist (does not have to be a vxlan tunnel)
- comware_vxlan_tunnel: tunnel=21 state=absent username={{ username }} password={{ password }} hostname={{ inventory_hostname }}


```


#### Notes

- state=absent removes the tunnel interface if it exists

- state=absent can also remove non-vxlan tunnel interfaces


---


## comware_command
Execute CLI commands on Comware 7 devices

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Execute CLI commands on Comware 7 devices

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| username  |   no  |  | <ul></ul> |  Username used to login to the switch  |
| hostname  |   yes  |  | <ul></ul> |  IP Address or hostname of the Comware 7 device that has NETCONF enabled  |
| command  |   yes  |  | <ul></ul> |  String (single command) or list of commands to be executed on the device.  Sending a list requires YAML format to be used in the playbook.  |
| password  |   no  |  | <ul></ul> |  Password used to login to the switch  |
| type  |   yes  |  | <ul> <li>display</li>  <li>config</li>  <li>show</li> </ul> |  State whether the commands are display (user view) or configure (system view) commands.  Display and show are the same thing.  |
| port  |   yes  |  830  | <ul></ul> |  NETCONF port number  |


 
#### Examples

```

# display vlan 10 passing in a string
- comware_command: command='display vlan 5' type=display username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

# display vlans passing in a list
- comware_command:
    command:
      - display vlan 10
      - display vlan 5
    type: display
    username: "{{ username }}"
    password: "{{ password }}"
    hostname: "{{ inventory_hostname }}"

# passing in config commands as a list
- comware_command:
    command:
      - vlan 5
      - name web_vlan
    type: config
    username: "{{ username }}"
    password: "{{ password }}"
    hostname: "{{ inventory_hostname }}"


```


#### Notes

- This module is not idempotent


---


## comware_interface
Manages physical interface attributes

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Manages administrative state and physical attributes of the interface

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| username  |   yes  |  | <ul></ul> |  Username used to login to the switch  |
| name  |   yes  |  | <ul></ul> |  Full name of the interface  |
| admin  |   no  |  up  | <ul> <li>up</li>  <li>down</li> </ul> |  Admin state of the interface  |
| speed  |   no  |  | <ul></ul> |  Speed of the interface in Mbps  |
| hostname  |   yes  |  | <ul></ul> |  IP Address or hostname of the Comware v7 device that has NETCONF enabled  |
| duplex  |   no  |  | <ul> <li>auto</li>  <li>full</li> </ul> |  Duplex of the interface  |
| state  |   no  |  present  | <ul> <li>present</li>  <li>absent</li>  <li>default</li> </ul> |  Desired state for the interface configuration  |
| password  |   yes  |  | <ul></ul> |  Password used to login to the switch  |
| type  |   no  |  | <ul> <li>bridged</li>  <li>routed</li> </ul> |  Type of interface, i.e. L2 or L3  |
| port  |   no  |  830  | <ul></ul> |  The Comware port used to connect to the switch  |
| description  |   no  |  | <ul></ul> |  Single line description for the interface  |


 

#### Notes

- Only logical interfaces can be removed with state=absent.

- If you want to configure type, run this module first with no other interface parameters. Then, remove the type parameter and include the other desired parameters. The type parameter defaults the other parameters.

- When state is set to default, the interface will be "defaulted" regardless of what other parameters are entered.

- When state is set to default, the interface must already exist.

- When state is set to absent, logical interfaces will be removed from the switch, while physical interfaces will be "defaulted"

- Tunnel interface creation and removal is not currently supported.


---


## comware_facts
Gathers facts of Comware 7 devices

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Gathers fact data (characteristics) of Comware 7 devices

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| username  |   no  |  | <ul></ul> |  Username used to login to the switch  |
| password  |   no  |  | <ul></ul> |  Password used to login to the switch  |
| hostname  |   yes  |  | <ul></ul> |  IP Address or hostname of the Comware 7 device that has NETCONF enabled  |
| port  |   yes  |  830  | <ul></ul> |  NETCONF port number  |


 
#### Examples

```

# get facts
- comware_facts: username={{ username }} password={{ password }} hostname={{ inventory_hostname }}


```



---


## comware_save
Save the running configuration

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Save the running configuration

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| username  |   yes  |  | <ul></ul> |  Username used to login to the switch  |
| password  |   yes  |  | <ul></ul> |  Password used to login to the switch  |
| hostname  |   yes  |  | <ul></ul> |  IP Address or hostname of the Comware 7 device that has NETCONF enabled  |
| filename  |   no  |  startup.cfg  | <ul></ul> |  Name of file that will be used when saving the current running conifg to flash.  |


 
#### Examples

```

# save as myfile.cfg (in flash)
- comware_save: filename=myfile.cfg username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

# save as startup.cfg (in flash)
- comware_save: username={{ username }} password={{ password }} hostname={{ inventory_hostname }}


```


#### Notes

- This modules saves the running config as startup.cfg in flash. or YOUR_FILENAME, which will also be saved to flash.  It is not changing the config file to load on next-boot.


---


## comware_portchannel
Manages port-channel (LAG) on Comware 7 devices

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Manages routed and bridged aggregation configurations on Comware 7 devices.  This includes physical interface configs for LACP.

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| min_ports  |   no  |  | <ul></ul> |  Minimum number of selected ports for the agg group  |
| username  |   yes  |  | <ul></ul> |  Username used to login to the switch  |
| hostname  |   yes  |  | <ul></ul> |  IP Address or hostname of the Comware v7 device that has NETCONF enabled  |
| group  |   yes  |  | <ul></ul> |  Group number to identify the Aggregate interface  |
| max_ports  |   no  |  | <ul></ul> |  Maximum number of selected ports for the agg group  |
| lacp_mode  |   no  |  active  | <ul> <li>active</li>  <li>passive</li> </ul> |  If mode is set to LACP, the type operating mode can be selected. This  mode will then be set for all members in the group.  |
| state  |   no  |  present  | <ul> <li>present</li>  <li>absent</li> </ul> |  Desired state for the interface configuration  |
| mode  |   no  |  dynamic  | <ul> <li>static</li>  <li>dynamic</li> </ul> |  Mode of the Aggregate interface  |
| members  |   no  |  | <ul></ul> |  COMPLETE Interface List that should be in the agg group. Full names should be used AND Interface names ARE case sensitive. For example, FortyGigE1/0/1 should NOT be written as fortygige1/0/1.  This is for safety.  |
| lacp_edge  |   no  |  | <ul> <li>enabled</li>  <li>disabled</li> </ul> |  Determine if an LACP agg group should be an edge aggregate interface  |
| password  |   yes  |  | <ul></ul> |  Password used to login to the switch  |
| type  |   yes  |  | <ul> <li>bridged</li>  <li>routed</li> </ul> |  Type of the Aggregate interface (L2 or L3)  |
| port  |   yes  |  830  | <ul></ul> |  NETCONF port number  |


 
#### Examples

```

  # Portchannel config
  - comware_portchannel:
      group: 100
      members:
        - FortyGigE1/0/27
        - FortyGigE1/0/28
        - FortyGigE1/0/29
        - FortyGigE1/0/30
      type: routed
      mode: static
      min_ports: 2
      max_ports: 4
      username: "{{ username }}"
      password: "{{ password }}"
      hostname: "{{ inventory_hostname }}"
      state: present


```


#### Notes

- When configuring a LAGG, the members param must be included

- Members is ALL members - it is ensuring that the members sent is the full list of all members.  This means to remove a member it just needs to be removed from the members list.

- When removing a LAGG, members is not required

- If mode is set to static, lacp_edge and lacp_mode are disregarded if those params are set


---


## comware_vrrp_global
Manages VRRP global configuration mode

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Manages VRRP global configuration mode

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| username  |   yes  |  | <ul></ul> |  Username used to login to the switch  |
| password  |   yes  |  | <ul></ul> |  Password used to login to the switch  |
| port  |   yes  |  830  | <ul></ul> |  NETCONF port number  |
| hostname  |   yes  |  | <ul></ul> |  IP Address or hostname of the Comware v7 device that has NETCONF enabled  |
| mode  |   yes  |  | <ul> <li>standard</li>  <li>load-balance</li> </ul> |  vrrp config mode for the switch  |


 
#### Examples

```

# configure load-balance mode
- comware_vrrp_global: mode=load-balance username={{ username }} password={{ password }} hostname={{ inventory_hostname }}


```



---


## comware_vxlan_vsi
Manages mapping of an Ethernet Service to a VSI (VXLAN ID)

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Manages the mapping of an Ethernet Service to a VSI (VXLAN ID)

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| username  |   yes  |  | <ul></ul> |  Username used to login to the switch  |
| password  |   yes  |  | <ul></ul> |  Password used to login to the switch  |
| hostname  |   yes  |  | <ul></ul> |  IP Address or hostname of the Comware v7 device that has NETCONF enabled  |
| vlanid  |   no  |  | <ul></ul> |  If encap is set to only-tagged or s-vid, vlanid must be set.  |
| instance  |   yes  |  | <ul></ul> |  Service instance id  |
| state  |   no  |  present  | <ul> <li>present</li>  <li>absent</li> </ul> |  Desired state for the interface configuration  |
| encap  |   no  |  default  | <ul> <li>default</li>  <li>tagged</li>  <li>untagged</li>  <li>only-tagged</li>  <li>s-vid</li> </ul> |  only-tagged also ensures s-vid  |
| interface  |   yes  |  | <ul></ul> |  Layer 2 interface or bridged-interface  |
| vsi  |   no  |  | <ul></ul> |  Name of the VSI  |
| access_mode  |   no  |  vlan  | <ul> <li>ethernet</li>  <li>vlan</li> </ul> |  Mapping Ethernet service instance to a VSI using Ethernet or VLAN mode (options for xconnect command)  |
| port  |   yes  |  830  | <ul></ul> |  NETCONF port number  |


 
#### Examples

```

# ensure the vsi is not mapped to the instance
- comware_vxlan_vsi: interface=Fo1/0/32 vsi=VSI_VXLAN_100 instance=100 state=absent username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

# ensure instance and vsi and configured with encap and access mode as specified
- comware_vxlan_vsi: interface=Fo1/0/32 vsi=VSI_VXLAN_100 instance=100 encap=default access_mode=vlan username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

# ensure instance and vsi and configured with encap and access mode as specified
- comware_vxlan_vsi: interface=Fo1/0/32 vsi=VSI_VXLAN_100 instance=100 encap=tagged access_mode=ethernet username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

# ensure instance and vsi and configured with encap and access mode as specified
- comware_vxlan_vsi: interface=Fo1/0/32 vsi=VSI_VXLAN_100 instance=100 encap=only-tagged vlanid=10 state=present username={{ username }} password={{ password }} hostname={{ inventory_hostname }}


```


#### Notes

- VSI needs to be created before using this module (comware_vxlan)

- encap and xconnect access_mode cannot be altered once set to change, use state=absent and re-configure

- state=absent removes the service instance for specified interface if if it exists

- This should be the last VXLAN module used after comware_vxlan_tunnel, and comware_vxlan.


---


## comware_clean_erase
Factory default HP Comware 7 device

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Reset system to factory default settings.  You will lose connectivity to the switch.  This module deletes all configuration files (.cfg files) in the root directories of the storage media. It Deletes all log files (.log files in the folder /logfile). Clears all log information (in the log buffer), trap information, and debugging information. Restores the parameters for the Boot ROM options to the factory-default settings. Deletes all files on an installed hot-swappable storage medium, such as a USB disk

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| username  |   yes  |  | <ul></ul> |  Username used to login to the switch  |
| password  |   yes  |  | <ul></ul> |  Password used to login to the switch  |
| factory_default  |   yes  |  | <ul> <li>true</li>  <li>false</li> </ul> |  Set to true if all logs and user-created files should be deleted and removed from the system and the device should be set to factory default settings  |
| hostname  |   yes  |  | <ul></ul> |  IP Address or hostname of the Comware 7 device that has NETCONF enabled  |
| port  |   yes  |  830  | <ul></ul> |  NETCONF port number  |


 
#### Examples

```


```

## comware_aaa
Manages mapping of an Ethernet Service to a VSI (VXLAN ID)

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Manages the mapping of an Ethernet Service to a VSI (VXLAN ID)

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| username  |   yes  |  | <ul></ul> |  Username used to login to the switch  |
| password  |   yes  |  | <ul></ul> |  Password used to login to the switch  |
| hostname  |   yes  |  | <ul></ul> |  IP Address or hostname of the Comware v7 device that has NETCONF enabled  |
| domain_name  |   yes  |  | <ul></ul> |  Configure SSL VPN access instance to use the specified ISP domain for AAA Authentication.  |
| aaa_type  |   no  |  | <ul> <li>authentication</li>  <li>authorization</li> <li>accounting</li></ul> |  Safety certification method  |
| state  |   no  |  present  | <ul> <li>present</li>  <li>absent</li> </ul> |  Desired state for the interface configuration  |
| access_type  |   no  |  default  | <ul> <li>LANaccess</li>  <li>login</li>    <li>portal</li>  <li>super</li>  <li>PPP</li>  <li>default</li> </ul> |  Configure authorization methods for LAN access users  |
| scheme_list  |   yes  |  | <ul> <li>radius</li> <li>hwtacacs</li><li>local</li></ul> |  Layer 2 interface or bridged-interface  |
| scheme_name_list  |   no  |  | <ul></ul> |  Name of the VSI  |
| port  |   yes  |  830  | <ul></ul> |  NETCONF port number  |


 
#### Examples

```

# create domain myserver and config it
- comware_aaa: domain_name=myserver aaa_type=authentication access_type=login scheme_list=radius scheme_name_list=test username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

# delete domain name myserver relates
- comware_aaa: domain_name=myserver state=default username={{ username }} password={{ password }} hostname={{ inventory_hostname }}


```


#### Notes

```


```

## comware_acl
Configure the acl issue to be applied to the interface

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Configure the acl issue to be applied to the interface

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| username  |   yes  |  | <ul></ul> |  Username used to login to the switch  |
| password  |   yes  |  | <ul></ul> |  Password used to login to the switch  |
| hostname  |   yes  |  | <ul></ul> |  IP Address or hostname of the Comware v7 device that has NETCONF enabled  |
| aclid  |   yes  |  | <ul></ul> |  The ID of ACL.  |
| name  |   no  |  | <ul></ul> |  Full name of the interface  |
| state  |   no  |  present  | <ul> <li>present</li>  <li>absent</li> </ul> |  Desired state for the interface configuration  |
| ruleid  |   no  |  | <ul> </ul> |  The ID of rule  |
| scripaddr  |   no  |  | <ul> </ul> |  Ip source address of rule  |
| action  |   no  |  | <ul><li>deny</li>  <li>permit</li></ul> |  Action of the rule  |
| appdirec  |   no  |  | <ul><li>inbound</li>  <li>outbound</li></ul> |  Action of the rule  |
| groupcg  |   no  |  | <ul><li>inbound</li>  <li>outbound</li></ul> |  Action of the rule  |
| port  |   yes  |  830  | <ul></ul> |  NETCONF port number  |


 
#### Examples

```

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


```


#### Notes


- When using this feature, "acliid" and "groupcg" are required parameters.
    - You must select a groupcategory when configurating the acl.
    - If you want to configure rule,you need to configure the acl first.
      The rule value range 0 to 65535.The value 65535 is an invalid rule ID.
      If you want to configure acl advanded,the acl id rang from 3000 to 3999.
    - If you want to configure acl basic,the acl id rang from 2000 to 2999.
    - When you want to create an rule, you must have a "aclid" and "action" and "scripaddr".
    - When you want to apply an rule to the interface, you must configure "aclid" and "groupcg".
    - You cannot have a "groupcg" parameter when deleting a rule.


---
## comware_bfd
Manage bfd config

  * Synopsis
  * Options
  * Examples

#### Synopsis
Manage bfd config

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| username  |   yes  |  | <ul></ul> |  Username used to login to the switch  |
| password  |   yes  |  | <ul></ul> |  Password used to login to the switch  |
| hostname  |   yes  |  | <ul></ul> |  IP Address or hostname of the Comware v7 device that has NETCONF enabled  |
| damp_max_wait_time  |   no  |  | <ul></ul> |  Configure the maximum dampening timer interval.  |
| damp_init_wait_time  |   no  |  | <ul></ul> |  Configure the initial dampening timer interval  |
| state  |   no  |  present  | <ul> <li>present</li>  <li>absent</li> </ul> |  Desired state for the interface configuration  |
| secondary  |   no  |  | <ul></ul> |  Configure the second dampening timer interval  |
| port  |   yes  |  830  | <ul></ul> |  NETCONF port number  |


 
#### Examples

```

- config bfd 
  comware_bfd: damp_max_wait_time=100 damp_init_wait_time=10 secondary=8 username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
- delete bfd related
  comware_bfd: damp_max_wait_time=100 damp_init_wait_time=10 secondary=8 state=default username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

```


#### Notes

```


```
 
## comware_bgp_af
Manage address family configs

  * Synopsis
  * Options
  * Examples

#### Synopsis
Manage address family configs

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| username  |   yes  |  | <ul></ul> |  Username used to login to the switch  |
| password  |   yes  |  | <ul></ul> |  Password used to login to the switch  |
| hostname  |   yes  |  | <ul></ul> |  IP Address or hostname of the Comware v7 device that has NETCONF enabled  |
| port  |   yes  |  830  | <ul></ul> |  NETCONF port number  |
| state  |   no  |  present  | <ul> <li>present</li>  <li>absent</li> </ul> |  Desired state for the interface configuration  |
| autonomous_system  |   yes  |  | <ul></ul> |  Autonomous system number <1-4294967295>.  |
| bgp_instance  |   no  |  | <ul></ul> |  Specify a BGP instance by its name  |
| address_familys_ipv4uni  |   no  | false | <ul><li>true</li>  <li>false</li> </ul> |   Specify the address-family ipv4 unicast |
| address_familys_ipv4uni  |   no  | false | <ul> <li>true</li>  <li>false</li></ul> |   Specify the address-family ipv6 unicast |
| address_familys_vpnv4  |   no  | false | <ul><li>true</li>  <li>false</li> </ul> |   Specify the VPNv4 address family |
| address_familys_vpnv6  |   no  | false | <ul><li>true</li>  <li>false</li> </ul> |   Specify the VPNv6 address family |
| default_ipv4_local_pref  |   no  |  | <ul></ul> |   Set the ipv4 default local preference value |
| default_ipv6_local_pref  |   no  |  | <ul></ul> |   Set the ipv6 default local preference value |
| fast_reroute_frr_policy  |   no  |  | <ul><li>true</li>  <li>false</li></ul> |   Set the ipv4 default local preference value |
| policy_vpn4_target  |   no  |  | <ul><li>true</li>  <li>false</li></ul> |   Filter VPN4 routes with VPN-Target attribute |
| policy_vpn6_target  |   no  |  | <ul><li>true</li>  <li>false</li></ul> |   Filter VPN6 routes with VPN-Target attribute |
| ipv4_route_select_delay  |   no  |  | <ul></ul> |   Set the delay time for optimal route selection of ipv4 |
| ipv6_route_select_delay  |   no  |  | <ul></ul> |   Set the delay time for optimal route selection of ipv6 |
| vpnv4_route_select_delay  |   no  |  | <ul></ul> |   Set the delay time for optimal route selection of vpnv4 |
| vpnv6_route_select_delay  |   no  |  | <ul></ul> |   Set the delay time for optimal route selection of vpnv6 |
| allow_invalid_as  |   no  |  | <ul></ul> |  Apply the origin AS validation state to optimal route selection.  |


 
#### Examples

```

# Basic bgp address-family config
- comware_bgp_af: autonomous_system=10 bgp_instance=test address_familys_ipv4uni=true ipv4_route_select_delay=20 allow_invalid_as=true username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
- comware_bgp_af: autonomous_system=10 bgp_instance=test address_familys_vpnv4=true policy_vpn4_target=true username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

```


#### Notes

```
    - address family setting include ipv4 ipv6 etc. some of the configs
      need address family ipv4 view , some need others , so ensure the 
      view you provided meets the config require
    - state default and absent are the same , if you want delete the setting configs , 
      the comware will undo the autonomous_system and instance .

```
 
 ## comware_bgp_global
config bgp configs in the bgp instance view such as routerid

  * Synopsis
  * Options
  * Examples

#### Synopsis
config bgp configs in the bgp instance view such as routerid

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| username  |   yes  |  | <ul></ul> |  Username used to login to the switch  |
| password  |   yes  |  | <ul></ul> |  Password used to login to the switch  |
| hostname  |   yes  |  | <ul></ul> |  IP Address or hostname of the Comware v7 device that has NETCONF enabled  |
| port  |   yes  |  830  | <ul></ul> |  NETCONF port number  |
| state  |   no  |  present  | <ul> <li>present</li>  <li>absent</li> </ul> |  Desired state for the interface configuration  |
| autonomous_system  |   yes  |  | <ul></ul> |  Autonomous system number <1-4294967295>.  |
| bgp_instance  |   no  |  | <ul></ul> |  Specify a BGP instance by its name  |
| router_id  |   no  | false | <ul></ul> |   Router ID in IP address format |
| advertise_rib_active  |   no  | false | <ul> <li>true</li>  <li>false</li></ul> |   Advertise the best route in IP routing table |
| timer_connect_retry  |   no  |  | <ul></ul> |   Configure the session retry timer for all BGP peers |
| timer_keepalive  |   no  |  | <ul></ul> |   Keepalive timer ,Value of keepalive timer in seconds |
| timer_hold  |   no  |  | <ul></ul> |   Hold timer , Value of hold timer in seconds |
| compare_as_med  |   no  | false | <ul><li>true</li>  <li>false</li></ul> |   Compare the MEDs of routes from different ASs |
| peer_ip  |   no  |  | <ul></ul> |  Specify BGP peers IPv4 address |
| peer_as_num  |   no  |  | <ul></ul> |   Specify BGP peers AS number |
| peer_ignore  |   no  |  | <ul></ul> |  Disable session establishment with the peers |


 
#### Examples

```

# bgp global views configs
-  comware_bgp_global: autonomous_system=10 bgp_instance=test router_id=192.168.1.185 advertise_rib_active=true timer_connect_retry=100 timer_keepalive=100 timer_hold=301 \
   compare_as_med=true peer_ip=1.1.1.3 peer_as_num=10 peer_ignore=true username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

```


#### Notes

```
    - all the configs except autonomous_system and bgp_instance are set in bgp instance view.
    - timer keepalive and time hold must be set together .
    - timer hold must be greater than 3 times timer keepalive.
    - peer relations are need peer ip first.
    - state default and absent are the same , if you want delete the setting configs , the comware
      will undo the autonomous_system and instance .
```
## comware_bgp_group
short_description: create and config bgp group 

  * Synopsis
  * Options
  * Examples

#### Synopsis
short_description: create and config bgp group 

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| username  |   yes  |  | <ul></ul> |  Username used to login to the switch  |
| password  |   yes  |  | <ul></ul> |  Password used to login to the switch  |
| hostname  |   yes  |  | <ul></ul> |  IP Address or hostname of the Comware v7 device that has NETCONF enabled  |
| port  |   yes  |  830  | <ul></ul> |  NETCONF port number  |
| state  |   no  |  present  | <ul> <li>present</li>  <li>absent</li> </ul> |  Desired state for the interface configuration  |
| bgp  |   yes  |  | <ul></ul> |  Autonomous system number <1-4294967295>.  |
| instance  |   no  |  | <ul></ul> |  Specify a BGP instance by its name  |
| group  |   no  |  | <ul></ul> |   Create a peer group |
| group_type  |   no  | false | <ul> <li>external</li>  <li>internal</li></ul> |   Group type , include external and internal |
| peer  |   no  |  | <ul></ul> |   Specify BGP peers , a group or peer ID |
| peer_connect_intf  |   no  | false | <ul></ul> |   Set interface name to be used as session's output interface |
| peer_in_group  |   no  |  | <ul></ul> |   Specify a peer-group |
| address_family  |   no  |  | <ul><li>l2vpn</li></ul> |   Specify an address family , only l2vpn can be config here |
| evpn  |   no  | false | <ul> <li>false</li>  <li>true</li> </ul> |  pecify the EVPN address family |
| policy_vpn_target  |   no  |enable  | <ul> <li>enable</li>  <li>disable</li> </ul> |  Filter VPN routes with VPN-Target attribute |
| reflect_client  |   no  | false | <ul> <li>true</li>  <li>false</li> </ul> |  Configure the peers as route reflectors |
| peer_group_state  |   no  |  | <ul> <li>true</li>  <li>false</li> </ul> |  Enable or disable the specified peers |

 
#### Examples

```

 # - name:  config bgp and create group
       # comware_bgp_group: bgp=200 group=evpn  group_type=internal   username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
     # - name:  config peer connet interface
       # comware_bgp_group: bgp=200 peer=evpn peer_connect_intf=LoopBack0  username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
     # - name:  join peer in the group
       # comware_bgp_group: bgp=200 peer=1.1.1.1 peer_in_group=evpn  username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
     # - name:  join peer in the group
       # comware_bgp_group: bgp=200 peer=3.3.3.3 peer_in_group=evpn  username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
     # - name:  create address-family view and config it
       # comware_bgp_group: bgp=200 address_family=l2vpn evpn=true policy_vpn_target=disable peer=evpn reflect_client=true  peer_group_state=true  \
       username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
     # - name:  remove bgp
       # comware_bgp_group: bgp=200 state=default username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
	   
```


#### Notes

```
- Connect interface must be exist in the device if you want use it.
    - If you want join a peer in a group , the group must be already exist.
    - bgp with and without instance are in different view , carefully config it
```
	
## comware_compare
Enter the configuration command and compare it with the expected result

  * Synopsis
  * Options
  * Examples

#### Synopsis
Enter the configuration command and compare it with the expected result

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| username  |   yes  |  | <ul></ul> |  Username used to login to the switch  |
| password  |   yes  |  | <ul></ul> |  Password used to login to the switch  |
| hostname  |   yes  |  | <ul></ul> |  IP Address or hostname of the Comware v7 device that has NETCONF enabled  |
| port  |   yes  |  830  | <ul></ul> |  NETCONF port number  |
| state  |   no  |  present  | <ul> <li>present</li>  <li>absent</li> </ul> |  Desired state for the interface configuration  |
| cmd  |   yes  |  | <ul></ul> |  command.  |
| result  |   yes  |  | <ul></ul> |  text path and name into the result parameter which include expected result  |

 
#### Examples

```

# - name: compare 
#   comware_compare: cmd='dis curr conf | include ssh' result='/root/ansible-hpe-cw7-master/gqy/result.txt' 
    username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
	   
```


#### Notes

```
- This modules Enter the configuration command and compare it with the expected result.
      For convenience, put the expected result into a text, and enter the text path and name into the result parameter.
      if display ok,it is consistent.
```
	
## comware_config
Back uo current configuration to the specified file

  * Synopsis
  * Options
  * Examples

#### Synopsis
Back uo current configuration to the specified file

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| username  |   yes  |  | <ul></ul> |  Username used to login to the switch  |
| password  |   yes  |  | <ul></ul> |  Password used to login to the switch  |
| hostname  |   yes  |  | <ul></ul> |  IP Address or hostname of the Comware v7 device that has NETCONF enabled  |
| port  |   yes  |  830  | <ul></ul> |  NETCONF port number  |
| state  |   no  |  present  | <ul> <li>present</li>  <li>absent</li> </ul> |  Desired state for the interface configuration  |
| filefolder  |   no  |  | <ul></ul> |  Full specified backup path on Comware v7 device, e.g. flash:/mypath/.  |
| arcstate  |   no  | absent | <ul> <li>present</li>  <li>absent</li> </ul> |  The switch of backup  |
| filename  |   no  | my_file | <ul></ul> |  Backup file  |
| replacefile  |   no  |  | <ul> </ul> |  Rolling file |
| repswitch  |   no  |  | <ul> <li>true</li>  <li>false</li> </ul> |  Configure rollback switch |
| y_or_no  |   no  |  | <ul><li>y</li>  <li>n</li>  </ul> |  Configure the switch to save the current configuration during rollback |

 
#### Examples

```

# backup config to flash:/llld/ans.cfg (in flash)
- comware_config: filename=ans arcstate=present filefolder=flash:/llld/ username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
# rollback config to netconf.cfg and save the current configuration(in flash)
- comware_config: repswitch=true replacefile=netconf.cfg y_or_no=y username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
# rollback config to netconf.cfg and do not save the current configuration
comware_config: replacefile=netconf.cfg  repswitch=true y_or_no=n username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
   
```


#### Notes

```
  - This modules backup the config to specified file in specified flash. 
    -You can use the specified file for configuration distribution.
```
	
## comware_dldp
Manage dldp authentication,interface,timeout and mode  on Comware 7 devices

  * Synopsis
  * Options
  * Examples

#### Synopsis
Manage dldp authentication,interface,timeout and mode  on Comware 7 devices

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| username  |   yes  |  | <ul></ul> |  Username used to login to the switch  |
| password  |   yes  |  | <ul></ul> |  Password used to login to the switch  |
| hostname  |   yes  |  | <ul></ul> |  IP Address or hostname of the Comware v7 device that has NETCONF enabled  |
| port  |   yes  |  830  | <ul></ul> |  NETCONF port number  |
| state  |   no  |  present  | <ul> <li>present</li>  <li>absent</li> </ul> |  Desired state for the interface configuration  |
| global_enable  |   no  | disable | <ul><li>disable</li>  <li>enable</li> </ul> |  global dldp enable or disable.  |
| auth_mode  |   no  |  | <ul> <li>md5</li>  <li>none</li> <li>simple</li></ul> |  Configure dldp authentication mode between current device and neighbor device  |
| pwd_mode  |   no  | | <ul><li>cipher</li>  <li>simple</li></ul> |  Configure the dldp authentication password mode between the current device and the neighbor device  |
| pwd  |   no  |  | <ul> </ul> |  Configure the dldp authentication password between the current device and the neighbor device |
| timeout  |   no  | 5 | <ul> </ul> |  Configure the sending interval of advertisement message(1~100) |
| shutdown_mode  |   no  | auto | <ul><li>auto</li>  <li>hybrid</li> <li>manual</li> </ul> |  Global configuration of interface shutdown mode after dldp discovers unidirectional link |
| name  |   no  |  | <ul> </ul> |  The full name of the interface |
| interface_enable  |   no  |  | <ul><li>disable</li>  <li>enable</li> </ul> |  Enable dldp function on the interface) |
| init_delay  |   no  |  | <ul></ul> |  Delay time of dldp blocking interface from initial state to single pass state.(1~5) |
| port_shutdown  |   no  |  | <ul><li>auto</li>  <li>hybrid</li> <li>manual</li> </ul> |  The interface shutdown mode after dldp discovers one-way link is configured on the interface |
 
#### Examples

```

  - name: config dldp
        comware_dldp: global_enable=enable auth_mode=md5 shutdown_mode=auto pwd_mode=cipher pwd=123456 timeout=10 name=HundredGigE1/0/27 
                      interface_enable=disable state=present username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
  - name: delete dldp configuration
        comware_dldp: global_enable=enable auth_mode=md5 shutdown_mode=auto pwd_mode=cipher pwd=123456 timeout=10 name=HundredGigE1/0/27 
                      interface_enable=disable state=absent username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

```


#### Notes

```
    - To enable the dldp feature, the dldp feature must be enabled on both the global and the interface.
	- when config interface_enable、init_delay and port_shutdown,name must be exit.
```
	
## comware_lldp_global
Manage global config state for LLDP.this funtion can be take effect only global and interface LLDP all open. 
The interface LLDP is open default.

  * Synopsis
  * Options
  * Examples

#### Synopsis
Manage global config state for LLDP.this funtion can be take effect only global and interface LLDP all open. 
The interface LLDP is open default.

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| username  |   yes  |  | <ul></ul> |  Username used to login to the switch  |
| password  |   yes  |  | <ul></ul> |  Password used to login to the switch  |
| hostname  |   yes  |  | <ul></ul> |  IP Address or hostname of the Comware v7 device that has NETCONF enabled  |
| port  |   yes  |  830  | <ul></ul> |  NETCONF port number  |
| state  |   yes  |  | <ul> <li>enable</li>  <li>disable</li> </ul> |  Desired state for LLDP global configuration  |

#### Examples

```

- name: manage lldp global enable 
- comware_lldp_global: state=enabled username={{ username }} password={{ password }} hostname={{ inventory_hostname }}


- name: manage lldp global disable 
- comware_lldp_global: state=disabled username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

```


#### Notes

```

```
	
## comware_lldp_interface
 Manage lldp enable on interfaces.The default state is enable

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Manage lldp enable on interfaces.The default state is enable

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| username  |   yes  |  | <ul></ul> |  Username used to login to the switch  |
| password  |   yes  |  | <ul></ul> |  Password used to login to the switch  |
| hostname  |   yes  |  | <ul></ul> |  IP Address or hostname of the Comware v7 device that has NETCONF enabled  |
| port  |   yes  |  830  | <ul></ul> |  NETCONF port number  |
| state  |   no  |  present  | <ul> <li>present</li>  <li>default</li> </ul> |  Desired state for the interface configuration  |
| name  |   yes  |  | <ul></ul> |  Full name of the interface  |
| interface_enable  |   yes  |  | <ul> <li>enable</li>  <li>disable</li></ul> | Layer 2 mode of the interface  |

#### Examples

```


# Basic interface lldp config
- comware_lldp_interface: name=FortyGigE1/0/2 interface_enable=enabled username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

```


#### Notes

```
- Before config interface lldp enable, the global lldp must be enable.

```
	
## comware_local_user
Manage local_user

  * Synopsis
  * Options
  * Examples

#### Synopsis
Manage local_user

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| username  |   yes  |  | <ul></ul> |  Username used to login to the switch  |
| password  |   yes  |  | <ul></ul> |  Password used to login to the switch  |
| hostname  |   yes  |  | <ul></ul> |  IP Address or hostname of the Comware v7 device that has NETCONF enabled  |
| port  |   yes  |  830  | <ul></ul> |  NETCONF port number  |
| state  |   no  |  present  | <ul> <li>present</li>  <li>absent</li> <li>default</li></ul> |  Desired state for the interface configuration  |
| localusername  |   yes  |  | <ul></ul> |  Local user name.  |
| group  |   no  |  | <ul> </ul> |  User group name |
| server_ftp  |   no  | | <ul><li>true</li>  <li>false</li></ul> |  enable or disable local user service-type ftp |
| server_http  |   no  |  | <ul><li>true</li>  <li>false</li></ul> |  enable or disable local user service-type http |
| server_https  |   no  |  | <ul><li>true</li>  <li>false</li></ul> |  enable or disable local user service-type https |
| server_pad  |   no  |  | <ul><li>true</li>  <li>false</li>  </ul> |  enable or disable local user service-type pad |
| server_ssh  |   no  |  | <ul><li>true</li>  <li>false</li></ul>  |  enable or disable local user service-type ssh |
| server_telnet  |   no  |  | <ul><li>true</li>  <li>false</li></ul> |  enable or disable local user service-type telnet |
| server_Terminal  |   no  |  |<ul><li>true</li>  <li>false</li></ul> |  enable or disable local user service-type Terminal |
| ftp_dir  |   no  |  | <ul> </ul> | Specify work directory of local user |
| local_user_level  |   no  |  | <ul> </ul> | Specify local user work level |
| localspassword  |   no  |  | <ul> </ul> | Password used to login to the local user|

 
#### Examples

```

# Basic Ethernet config
- Before using ftp_dir , ensure it already exist in the device.   e.g. flash:/
- comware_local_user: localusername=test server_ftp=True local_user_level=15 username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

```


#### Notes

```
    - Before using ftp_dir , ensure it already exist in the device.
    - Local user group specify the user group , if the device has the group then do the config , 
        if not , create group and config
```
	
## comware_log
get the device diagnostic information and upload to file server

  * Synopsis
  * Options
  * Examples

#### Synopsis
get the device diagnostic information and upload to file server

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| username  |   yes  |  | <ul></ul> |  Username used to login to the switch  |
| password  |   yes  |  | <ul></ul> |  Password used to login to the switch  |
| hostname  |   yes  |  | <ul></ul> |  IP Address or hostname of the Comware v7 device that has NETCONF enabled  |
| port  |   yes  |  830  | <ul></ul> |  NETCONF port number  |
| state  |   no  |    | <ul> <li>present</li>  <li>default</li> <li>loadtoserver</li></ul> |  Desired state for the interface configuration  |
| service_dir  |   no  |  | <ul></ul> |  the dir in server which you want to upload the diag file from device.  |
| diag_dir  |   no  |  | <ul> </ul> |  where the device diagnostic information storage , default is flash:/ |
| ftpupload  |   no  | true| <ul><li>true</li>  <li>false</li></ul> |  whether upload the diagnostic information to the servic |
| servertype  |   no  |  | <ul><li>ftp</li>  <li>scp</li></ul> |  choose the diagnostic file upload server type |
| server_hostname  |   no  |  | <ul></ul> |  the remote server hostname e.g.192.168.1.199. |
| server_name  |   no  |  | <ul></ul> |  the name to login in remote server |
| server_pwd  |   no  |  | <ul>></ul>  |  the password to login in remote server. |
| dst_dir  |   no  |  | <ul></ul> |  remote dir where the file save |
| server_Terminal  |   no  |  |<ul><li>true</li>  <li>false</li></ul> |  enable or disable local user service-type Terminal |
| ftp_dir  |   no  |  | <ul> </ul> | Specify work directory of local user |
| local_user_level  |   no  |  | <ul> </ul> | Specify local user work level |
| localspassword  |   no  |  | <ul> </ul> | Password used to login to the local user|

 
#### Examples

```
      - name: get diagnostic information to the file server
        comware_log:  diag_dir=flash:/diaglog service_dir=/root/ansible-hpe-cw7-master/diaglog/ ftpupload=true 
        username={{ username }} password={{ password }} hostname={{ inventory_hostname }}     
              
      - name: delete diagnostic information in device
        comware_log:  state=loadtoserver servertype=ftp server_hostname=192.168.1.199 server_name=fc server_pwd=111111 
        diag_dir=flash:/diaglog service_dir=/root/ansible-hpe-cw7-master/diaglog/ dst_dir= 
        username={{ username }} password={{ password }} hostname={{ inventory_hostname }} 
                                       
      # - name: delete diagnostic information in device
        # comware_log:  state=loadtoserver servertype=scp server_hostname=192.168.1.185 server_name=h3c server_pwd=h3c 
        diag_dir=flash:/diaglog service_dir=/root/ansible-hpe-cw7-master/diaglog/ dst_dir=flash:/ 
        username={{ username }} password={{ password }} hostname={{ inventory_hostname }} 
        
      - name: delete diagnostic information in device
        comware_log:  diag_dir=flash:/diaglog state=default username={{ username }} password={{ password }} hostname={{ inventory_hostname }} 
        
```


#### Notes

```
    - Getting device diagnostic information will take some time , here give 300s to get the information,
      if result goes to time out , check the timeout 300s first.
    - if state is present , you will get the diag file with .tar.gz , and it will upload to ansible 
      server.
```

## comware_log_source
Manage output rules for log information on V7 devices

  * Synopsis
  * Options
  * Examples

#### Synopsis
Manage output rules for log information on V7 devices

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| username  |   yes  |  | <ul></ul> |  Username used to login to the switch  |
| password  |   yes  |  | <ul></ul> |  Password used to login to the switch  |
| hostname  |   yes  |  | <ul></ul> |  IP Address or hostname of the Comware v7 device that has NETCONF enabled  |
| port  |   yes  |  830  | <ul></ul> |  NETCONF port number  |
| state  |   no  |  present  | <ul> <li>present</li>  <li>absent</li></ul> |  Desired state for the interface configuration  |
| channelID  |   yes  |  | <ul><li>1</li>  <li>2</li> <li>3</li><li>4</li><li>5</li></ul> |   Specifies syslog output destination.  |
| channelName  |   yes  |  | <ul> </ul> |  Specifies a module by its name |
| level  |   no  | | <ul><li>emergency</li>  <li>alert</li> <li>critical</li> <li>error</li> <li>warning</li> <li>notification</li> <li>informational</li><li>deny</li><li>debugging</li></ul> | A log output rule specifies the source modules and severity level of logs that can be output to a destination. Logs matching the output rule are output to the destination. |

 
#### Examples

```
# basic config
- comware_log_source: channelID=1 channelName=ARP level=critical username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

# delete config
- comware_log_source: channelID=1 channelName=ARP level=critical state=absent username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

```


#### Notes

```
 - If state=default, the config will be removed
```
	
## comware_loghost
Manage info-center log host and related parameters on V7 devices

  * Synopsis
  * Options
  * Examples

#### Synopsis
Manage info-center log host and related parameters on V7 devices

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| username  |   yes  |  | <ul></ul> |  Username used to login to the switch  |
| password  |   yes  |  | <ul></ul> |  Password used to login to the switch  |
| hostname  |   yes  |  | <ul></ul> |  IP Address or hostname of the Comware v7 device that has NETCONF enabled  |
| port  |   yes  |  830  | <ul></ul> |  NETCONF port number  |
| state  |   no  |  present  | <ul> <li>present</li>  <li>absent</li></ul> |  Desired state for the interface configuration  |
| loghost  |   yes  |  | <ul></ul> |   Address of the log host.  |
| VRF  |   yes  |  | <ul> </ul> |  VRF instance name |
| hostport  |   no  | 514| <ul></ul> | Port number of the log host. |
| facility  |   no  | 184 | <ul> <li>128</li>  <li>136</li><li>144</li><li>152</li><li>160</li><li>168</li><li>176</li><li>184</li></ul> |  Logging facility used by the log host |
| sourceID  |   no  | | <ul></ul> | Configure the source IP address of the sent log information.The default state is Using the primary IP address of the outgoing interface as the source IP address of the sent log information. |

 
#### Examples

```
# basic config
- comware_loghost: loghost=3.3.3.7 VRF=vpn2 hostport=512 facility=128 sourceID=LoopBack0 username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

# delete config
- comware_loghost: loghost=3.3.3.7 VRF=vpn2 hostport=512 facility=128 sourceID=LoopBack0 state=absent username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

```


#### Notes

```

```

## comware_mtu
Manage mtu and jumboframe of the interface

  * Synopsis
  * Options
  * Examples

#### Synopsis
Manage mtu and jumboframe of the interface

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| username  |   yes  |  | <ul></ul> |  Username used to login to the switch  |
| password  |   yes  |  | <ul></ul> |  Password used to login to the switch  |
| hostname  |   yes  |  | <ul></ul> |  IP Address or hostname of the Comware v7 device that has NETCONF enabled  |
| port  |   yes  |  830  | <ul></ul> |  NETCONF port number  |
| state  |   no  |  present  | <ul> <li>present</li>  <li>default</li></ul> |  Desired state for the interface configuration  |
| name  |   yes  |  | <ul></ul> |   Full name of the interface.  |
| mtu  |   no  |  | <ul> </ul> |  Specify Maximum Transmission Unit(MTU) of the interface |
| jumboframe  |   no  | | <ul></ul> | Specify Maximum jumbo frame size allowed of the interface. |

#### Examples

```
# Basic Ethernet config
- comware_mtu: name=Ten-GigabitEthernet1/0/7 jumboframe=1537 mtu=1600 username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

```


#### Notes

```
    - mtu can be set in interface type of ['GigabitEthernet','Ten-GigabitEthernet','FortyGigE',
      'Vlan-interface','Route-Aggregation','TwentyGigE','Twenty-FiveGigE','HundredGigE'] and 
      some of these must be set as route mode.
    - jumboframe can be set in interface type of ['GigabitEthernet','Ten-GigabitEthernet',
      'FortyGigE','Bridge-Aggregation','Route-Aggregation','TwentyGigE','Twenty-FiveGigE','HundredGigE']
```
	
## comware_netconf
Manage netconf log and xml function on Comware 7 devices.XML cfg not support enter xml view now,This is not normally done.

  * Synopsis
  * Options
  * Examples

#### Synopsis
Manage netconf log and xml function on Comware 7 devices.XML cfg not support enter xml view now,This is not normally done.

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| username  |   yes  |  | <ul></ul> |  Username used to login to the switch  |
| password  |   yes  |  | <ul></ul> |  Password used to login to the switch  |
| hostname  |   yes  |  | <ul></ul> |  IP Address or hostname of the Comware v7 device that has NETCONF enabled  |
| port  |   yes  |  830  | <ul></ul> |  NETCONF port number  |
| state  |   no  |  present  | <ul> <li>present</li>  <li>absent</li></ul> |  Desired state for the interface configuration  |
| source  |   no  |  | <ul><li>all</li>  <li>agent</li><li>soap</li><li>web</li></ul> |   NETCONF operation source requiring log output.Option 'all' means all source  |
| operation  |   no  |  | <ul>  <li>protocol-operation</li><li>row-operation</li><li>verbose</li></ul> |  Netconf operation option.If you chose protocol-operation,the opera_type option must be config. |
| opera_type  |   no  | | <ul><li>all</li><li>action</li><li>config</li><li>session</li><li>get</li><li>set</li><li>others</li><li>syntax</li></ul> | Protocol-operation option. |

#### Examples

```
  # netconf config
  - comware_netconf:
      source: all
      operation: protocol-operation
      opera_type: action
      username: "{{ username }}"
      password: "{{ password }}"
      hostname: "{{ inventory_hostname }}"

  # detele netconf config    
  - comware_netconf:
      source: all
      operation: protocol-operation
      opera_type: action
      username: "{{ username }}"
      password: "{{ password }}"
      hostname: "{{ inventory_hostname }}"
      state: absent

comware_netconf: soap=http ssh=enable username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
```


#### Notes

```

```
	
## comware_netstream
Manage ip netstream,rate,timeout, max_entry,vxlan udp-port,and interface enable and ip netstream aggregation destination-prefix enable, 
netstream statistics output message destination address and destination UDP port number configurationon Comware 7 devices

  * Synopsis
  * Options
  * Examples

#### Synopsis
Manage ip netstream,rate,timeout, max_entry,vxlan udp-port,and interface enable and ip netstream aggregation destination-prefix enable, 
netstream statistics output message destination address and destination UDP port number configurationon Comware 7 devices

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| username  |   yes  |  | <ul></ul> |  Username used to login to the switch  |
| password  |   yes  |  | <ul></ul> |  Password used to login to the switch  |
| hostname  |   yes  |  | <ul></ul> |  IP Address or hostname of the Comware v7 device that has NETCONF enabled  |
| port  |   yes  |  830  | <ul></ul> |  NETCONF port number  |
| state  |   no  |  present  | <ul> <li>present</li>  <li>absent</li></ul> |  Desired state for the interface configuration  |
| netstream  |   yes  |  | <ul><li>enable</li>  <li>disable</li></ul> |   global netstream enable or disable |
| rate  |   no  |  | <ul>  </ul> |  Configure output rate limit. |
| timeout  |   no  | | <ul><li>aging</li><li>disable-caching</li><li>max-entries</li></ul> |  Active aging time of configuration flow. |
| max_enter  |   no  |  | <ul>  </ul> |  Active aging time of configuration flow. |
| vxlan_udp  |   no  |  | <ul>  </ul> |  Enable vxlan message statistics function. |
| sampler  |   no  |  | <ul>  </ul> |  Create a sampler. |
| mode  |   no  |  | <ul> <li>fixed</li>  <li>random</li> </ul> |  Sampler mode.if config sampler,this parameter is must be exit. |
| sampler_rate  |   no  |  | <ul>  </ul> |  Sampler rate. if config sampler,this parameter is must be exit. |
| version  |   no  | 9 | <ul> <li>5</li>  <li>9</li>  <li>10</li></ul> |  Configure autonomous system options for netstream version. |
| bgp  |   no  |  | <ul> <li>origin-as</li>  <li>peer-as</li>  <li>bgp-nexthop</li></ul> |  BGP next hop option. |
| inactive  |   no  |  | <ul> </ul> |  Configure Inactive aging time of flow.(10~600). |
| source_intf  |   no  |  | <ul> </ul> |  Configure the source interface of netstream statistical output message. |
| aggregation  |   no  |  | <ul><li>as</li>  <li>destination-prefix</li>  <li>prefix</li><li>prefix-port</li>  <li>protocol-port</li>  <li>source-prefix</li><li>tos-as</li>  <li>tos-bgp-nexthop</li>  <li>tos-destination-prefix</li><li>tos-prefix</li>  <li>tos-protocol-port</li>  <li>tos-source-prefix</li></ul> |  Enter netstream aggregation view and enable it. |
| name  |   no  |  | <ul> </ul> |  Full name of the interface |
| interface_enable  |   no  |  | <ul><li>inbound</li> <li>outbound</li>  </ul> |  manage interface netstream enable.To config this, name parameter must be exit |
| interface_sampler  |   no  |  | <ul> </ul> |  manage interface sampler |
| host  |   no  |  | <ul> </ul> |  Configure the destination address of netstream statistical output message |
| udp  |   no  |  | <ul> </ul> |  manage interface sampler |
| vpn_name  |   no  |  | <ul> </ul> |  Specify the VPN to which the destination address of netstream statistical output message belongs |

#### Examples

```
# netstream config
  - comware_netstream: netstream=enable rate=10 timeout=1 max_entry=2 vxlan_udp=8000 aggregation=prefix host=192.168.1.43 udp=29 state=present username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
# delete netstream config
  - comware_netstream: netstream=enable rate=10 timeout=1 max_entry=2 vxlan_udp=8000 aggregation=prefix host=192.168.1.43 udp=29 state=absent username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

```


#### Notes

```
    - Before configuring netstream stream image, you need to enable the global netstream function.
    - The default state is not open global netstream function.If you want to config interface netstream enable,the name parameter
      must be exit.If you config netstream statistics output message,host and udp paramaters must be exit.
	  
```
	
## comware_ntp
Configure the ntp issue to be applied to the device

  * Synopsis
  * Options
  * Examples

#### Synopsis
Configure the ntp issue to be applied to the device

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| username  |   yes  |  | <ul></ul> |  Username used to login to the switch  |
| password  |   yes  |  | <ul></ul> |  Password used to login to the switch  |
| hostname  |   yes  |  | <ul></ul> |  IP Address or hostname of the Comware v7 device that has NETCONF enabled  |
| port  |   yes  |  830  | <ul></ul> |  NETCONF port number  |
| state  |   no  |  present  | <ul> <li>present</li>  <li>absent</li></ul> |  Desired state for the interface configuration  |
| name  |   no  |  | <ul></ul> |   Full name of the interface |
| ntpenable  |   no  | false | <ul> <li>true</li>  <li>false</li> </ul> |  The status of NTP. |
| ntpauthenable  |   no  |false | <ul><li>true</li>  <li>false</li> </ul> | The status of NTP authentication. |
| stratum  |   no  |  | <ul>  </ul> |  The stratum level of the local clock |
| service  |   no  |  | <ul><li>ntp</li>  <li>sntp</li>  </ul> |  The service of NTP . |
| keyid  |   no  |  | <ul>  </ul> |  The authentication-keys of NTP. |
| authmode  |   no  |  | <ul> <li>md5</li> <li>hmac_sha_384</li><li>hmac_sha_256</li><li>hmac_sha_384</li> <li>hmac_sha_1</li> </ul> |  Authentication mode |
| authkey  |   no  |  | <ul>  </ul> | Authentication key. |
| reliable  |   no  | false | <ul> <li>false</li>  <li>true</li> </ul> |  Whether the key is a trusted key. |
| ipadd  |   no  |  | <ul></ul> |  Remote IPv4 or IPv6 address. |
| addrtype  |   no  | ipv4 | <ul>  <li>ipv4</li>  <li>ipv6</li></ul> |  Address type. |
| del_rel_alone  |   no  |  | <ul><li>true</li>  <li>false</li> </ul> |  Whether delete trusted key alone. |
| del_auth_all  |   no  |  | <ul><li>true</li>  <li>false</li> </ul> |  Whether delete all trusted key configurations. |

#### Examples

```
# configure NTP authentication 
- comware_ntp: service=ntp keyid=42 authmode=md5 authkey=anicekey reliable=true username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
# configure NTP reference clock
- comware_ntp: stratum=2 username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
# configure NTP client
- comware_ntp: service=ntp keyid=42 hostmode=client ipadd=10.1.1.1 name=hun1/2/2 username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
# delete trusted keys alone
- comware_ntp: state=absent del_rel_alone=true service=ntp keyid=42 reliable=false  username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
# delete all verfication keys
- comware_ntp: state=absent service=ntp keyid=42 del_auth_all=true  username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

```


#### Notes

```

    - When configurating clients, IPv6 does not support.
    - The keyid is unsigned integer,and the value range is 1 to 4294967295.
    - The type of authkey is string,the length is 1 to 32 characters.
      The stratum is unsigned integer,and the value range is 1 to 15.
	  
```
	
## comware_ospf
Manage ospf

  * Synopsis
  * Options
  * Examples

#### Synopsis
Manage ospf

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| username  |   yes  |  | <ul></ul> |  Username used to login to the switch  |
| password  |   yes  |  | <ul></ul> |  Password used to login to the switch  |
| hostname  |   yes  |  | <ul></ul> |  IP Address or hostname of the Comware v7 device that has NETCONF enabled  |
| port  |   yes  |  830  | <ul></ul> |  NETCONF port number  |
| state  |   no  |  present  | <ul> <li>present</li> <li>default</li> <li>absent</li></ul> |  Desired state for the interface configuration  |
| ospfname  |   yes  |  | <ul></ul> |   Instance name.(1~65535) |
| routerid  |   no  |  | <ul> </ul> |  Router identifier. |
| area  |   no  | | <ul> </ul> | Area ID. |
| areatype  |   no  |  | <ul>  <li>NSSA</li>  <li>Stub</li> </ul> |  Area type |
| bandwidth  |   no  |  | <ul> </ul> |  Configure the bandwidth reference value by which link overhead is calculated(1~4294967) . |
| lsa_generation_max  |   no  |  | <ul>  </ul> |   Maximum time interval between OSPF LSA regenerations(1~60s) |
| lsa_generation_min  |   no  |  | <ul>  </ul> |  Minimum time interval between OSPF LSA regenerations(10~60000ms)|
| lsa_generation_inc  |   no  |  | <ul>  </ul> | Interval penalty increment for OSPF LSA regeneration(10~60000ms) |
| lsa_arrival  |   no  |  | <ul></ul> |  Configure the minimum time interval for repeat arrival of OSPF LSA(0~60000ms) |
| ipadd  |   no  |  | <ul></ul> |  Remote IPv4 or IPv6 address. |
| addrtype  |   no  | ipv4 | <ul>  <li>ipv4</li>  <li>ipv6</li></ul> |  Address type. |
| del_rel_alone  |   no  |  | <ul><li>true</li>  <li>false</li> </ul> |  Whether delete trusted key alone. |
| del_auth_all  |   no  |  | <ul><li>true</li>  <li>false</li> </ul> |  Whether delete all trusted key configurations. |

#### Examples

```
# Basic Ethernet config
- comware_ospf: ospfname=4 area=2.2.2.2 areatype=NSSA lsa_generation_max=20 lsa_generation_min=20 lsa_generation_inc=20 username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

```


#### Notes

```

	  
```
	
## comware_ospf_intf
Manage ospf in interface

  * Synopsis
  * Options
  * Examples

#### Synopsis
Manage ospf in interface

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| username  |   yes  |  | <ul></ul> |  Username used to login to the switch  |
| password  |   yes  |  | <ul></ul> |  Password used to login to the switch  |
| hostname  |   yes  |  | <ul></ul> |  IP Address or hostname of the Comware v7 device that has NETCONF enabled  |
| port  |   yes  |  830  | <ul></ul> |  NETCONF port number  |
| state  |   no  |  present  | <ul> <li>present</li> <li>default</li> <li>absent</li></ul> |  Desired state for the interface configuration  |
| name  |   yes  |  | <ul></ul> |   full name of interface |
| ospfname  |   no  |  | <ul> </ul> |  Instance name.(1~65535). |
| ospfcost  |   no  | | <ul> </ul> | Specify the OSPF area. |
| simplepwdtype  |   no  |  | <ul>  <li>cipher</li>  <li>plain</li> </ul> |  Specify the password type of ospf auth_mode simple |
| simplepwd  |   no  |  | <ul> </ul> |  Specify the password  of ospf auth_mode simple . |
| keyid  |   no  |  | <ul>  </ul> |  Specify the md5 or hwac-md5 key of ospf auth_mode |
| md5type  |   no  |  | <ul> <li>md5</li> <li>hwac-md5</li> </ul> |  Specify the ospf auth_mode md5 type|
| md5pwdtype  |   no  |  | <ul> <li>cipher</li><li>plain</li> </ul> | Specify the password type of ospf auth_mode md5 |
| md5pwd  |   no  |  | <ul></ul> |  Specify the password of ospf auth_mode md5 |
| network_type  |   no  |  | <ul><li>broadcast</li><li>nbma</li><li>p2p</li><li>p2mp</li></ul> |  Specify OSPF network type. |


#### Examples

```
  ensure name (interface name) exists in device and the interface support ospf setting.
- comware_ospf_intf: name=Ten-GigabitEthernet1/0/7 ospfname=1 area=0 ospfcost=10 network_type=p2p keyid=11 md5type=md5 md5pwdtype=plain md5pwd=1 username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
- comware_ospf_intf: name=Ten-GigabitEthernet1/0/7 state=default  username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

```


#### Notes

```
    - The module is used to config interface ospf setting , before using the module , please
      ensure the interface exists and is able to make ospf setting . 
    - Interface ospf auth mode can config as simple or md5 , however these two mode can not be
      set at the same time.
    - Some of the setting must be set together e.g. ospfname must together with area.
    - state default or absent will delete all the ospf settings , 
	  
```
	
## comware_patch
Rollback the running configuration

  * Synopsis
  * Options
  * Examples

#### Synopsis
Rollback the running configuration

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| username  |   yes  |  | <ul></ul> |  Username used to login to the switch  |
| password  |   yes  |  | <ul></ul> |  Password used to login to the switch  |
| hostname  |   yes  |  | <ul></ul> |  IP Address or hostname of the Comware v7 device that has NETCONF enabled  |
| port  |   yes  |  830  | <ul></ul> |  NETCONF port number  |
| patchname  |   no  |  | <ul></ul> |   Name of patch that will be used |
| activate  |   no  |  | <ul>  <li>true</li> <li>false</li> </ul> |  active patch or not |
| check_result  |   no  | | <ul><li>true</li> <li>false</li>  </ul> | check patch active success or not. |


#### Examples

```
      - name: copy version from ansible server into switch.
        comware_file_copy: file=/root/ansible-hpe-cw7-master/gqy/s6820-cmw710-system-weak-patch-f6205p05h16.bin remote_path=flash:/s6820-cmw710-system-weak-patch-f6205p05h16.bin username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

      - name: check bin is exit or not and active it.
        comware_patch: patchname=patch.bin activate=true username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
        async: 60
        poll: 0

      - name: check patch is active or not 
        comware_patch: patchname=s6805-cmw710-boot-r6607.bin check_result=true username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

```


#### Notes

```
    - This modules rollback the config to startup.cfg, or the supplied
      filename, in flash. It is not
      changing the config file to load on next boot.
	  
```
	
## comware_radius
create radius scheme

  * Synopsis
  * Options
  * Examples

#### Synopsis
create radius scheme

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| username  |   yes  |  | <ul></ul> |  Username used to login to the switch  |
| password  |   yes  |  | <ul></ul> |  Password used to login to the switch  |
| hostname  |   yes  |  | <ul></ul> |  IP Address or hostname of the Comware v7 device that has NETCONF enabled  |
| port  |   yes  |  830  | <ul></ul> |  NETCONF port number  |
| state  |   no  |  present  | <ul> <li>present</li>  <li>absent</li> </ul> |  Desired state for the interface configuration  |
| radius_scheme  |   yes  |  | <ul></ul> |   Specify RADIUS scheme |


#### Examples

```
# Basic radius config
- comware_radius: radius_scheme=test username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

# Delete radius config
- comware_radius: radius_scheme=test state=default username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

```


#### Notes

```

	  
```
	
## comware_rollback
Rollback the running configuration

  * Synopsis
  * Options
  * Examples

#### Synopsis
Rollback the running configuration

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| username  |   yes  |  | <ul></ul> |  Username used to login to the switch  |
| password  |   yes  |  | <ul></ul> |  Password used to login to the switch  |
| hostname  |   yes  |  | <ul></ul> |  IP Address or hostname of the Comware v7 device that has NETCONF enabled  |
| port  |   yes  |  830  | <ul></ul> |  NETCONF port number  |
| filename  |   no  | startup.cfg | <ul></ul> |   name of file that will be used when rollback the conifg to flash |
| comparefile  |   no  | startup.cfg | <ul></ul> |   Name of file that will be used when compared with filename file. if not set, no compared action executed. |
| clean  |   no  | false | <ul><li>true</li>  <li>false</li></ul> |   delete the rollback point |
| diff_file  |   no  |  | <ul></ul> |   File that will be used to store the diffs.  Relative path is location of ansible playbook. If not set, no diffs are saved |


#### Examples

```
# rollback config to myfile.cfg (in flash)
- comware_rollback: filename=myfile.cfg username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

# rollback config to startup.cfg (in flash)
- comware_rollback: username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

# delete rollback point 123.cfg (in flash)
- comware_rollback: filename=123.cfg clean=true username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

# files compared
- comware_rollback: filename=123.cfg comparefile=test.cfg username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
  diff_file='/root/ansible-hpe-cw7-master/diffs.diff'
```


#### Notes

```
    - This modules rollback the config to startup.cfg, or the supplied
      filename, in flash. It is not
      changing the config file to load on next boot.
	  
```
	
## comware_sflow
Manage sflow attributes for Comware 7 devices

  * Synopsis
  * Options
  * Examples

#### Synopsis
Manage sflow attributes for Comware 7 devices

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| username  |   yes  |  | <ul></ul> |  Username used to login to the switch  |
| password  |   yes  |  | <ul></ul> |  Password used to login to the switch  |
| hostname  |   yes  |  | <ul></ul> |  IP Address or hostname of the Comware v7 device that has NETCONF enabled  |
| port  |   yes  |  830  | <ul></ul> |  NETCONF port number  |
| state  |   no  |  present  | <ul> <li>present</li>  <li>absent</li> </ul> |  Desired state for the interface configuration  |
| collectorID  |   yes  |  | <ul></ul> |   the sflow collector id |
| addr  |   yes  |  | <ul></ul> |   the ipv4 or ipv6 address |
| vpn  |   no  |  | <ul></ul> |    Name to configure for the specified vpn-instance |
| descr  |   yes  | CLI Collector | <ul></ul> |   Description for the collectorID.must be exit|
| time_out  |   no  |  | <ul></ul> |    the collector's parameter aging time |
| Port  |   no  | 6343 | <ul></ul> |    UDP port |
| data_size  |   no  | 1400 | <ul></ul> |    the sflow datagram max size |
| agent_ip  |   no  |  | <ul></ul> |   Configure the IP address of the sFlow agent|
| sourceIpv4IP  |   no  |  | <ul></ul> |    Configure the source IPV4 address of the sFlow message |
| sourceIpv6IP  |   no  |  | <ul></ul> |    Configure the source IPV6 address of the sFlow message |

#### Examples

```
# Basic  config
- comware_sflow: collectorID=1 vpn=1 addr=1.1.1.1 data_size=500 descr=netconf time_out=1200 username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

# delete config
- comware_sflow: collectorID=1 addr=1.1.1.1 state=absent username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

```


#### Notes

```

	  
```
	
## comware_sflow_intf
Manage sflow interface flow collector and sampling_rate on Comware 7 devices.

  * Synopsis
  * Options
  * Examples

#### Synopsis
Manage sflow interface flow collector and sampling_rate on Comware 7 devices.

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| username  |   yes  |  | <ul></ul> |  Username used to login to the switch  |
| password  |   yes  |  | <ul></ul> |  Password used to login to the switch  |
| hostname  |   yes  |  | <ul></ul> |  IP Address or hostname of the Comware v7 device that has NETCONF enabled  |
| port  |   yes  |  830  | <ul></ul> |  NETCONF port number  |
| state  |   no  |  present  | <ul> <li>present</li>  <li>absent</li> </ul> |  Desired state for the interface configuration  |
| intf_name  |   yes  |  | <ul></ul> |  interface name |
| rate  |   no  |  | <ul></ul> |   Configure sampling_rate(>8192)|
| collector  |   no  |  | <ul></ul> |   sflow flow collector(1~4).  |


#### Examples

```
# netstream config
  - comware_sflow_intf: intf_name=xxxx rate=xxxx collector=xx username={{ username }} password={{ password }} hostname={{ inventory_hostname }} username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
# delete netstream config
  - comware_sflow_intf: intf_name=xxxx rate=xxxx collector=xx username={{ username }} password={{ password }} hostname={{ inventory_hostname }} state=absent username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

```


#### Notes

```
    - cli.  Netconf net surport.
	  
```
	
## comware_snmp_community
Manages SNMP community configuration on H3C switches.

  * Synopsis
  * Options
  * Examples

#### Synopsis
Manages SNMP community configuration on H3C switches.

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| username  |   yes  |  | <ul></ul> |  Username used to login to the switch  |
| password  |   yes  |  | <ul></ul> |  Password used to login to the switch  |
| hostname  |   yes  |  | <ul></ul> |  IP Address or hostname of the Comware v7 device that has NETCONF enabled  |
| port  |   yes  |  830  | <ul></ul> |  NETCONF port number  |
| state  |   no  |  present  | <ul> <li>present</li>  <li>absent</li> </ul> |  Desired state for the interface configuration  |
| acl_number  |  no |  | <ul></ul> |  Access control list number |
| community_name  |   no  |  | <ul></ul> |  Unique name to identify the community|
| access_right  |   no  |  | <ul><li>read</li>  <li>write</li></ul> |   Access right read or write..  
| community_mib_view  |   no  |  | <ul></ul> |   Mib view name.  |
| access_right  |   no  |  | <ul></ul> |   Access right read or write..  |

#### Examples

```
- name: "Config SNMP group"
    comware_snmp_group:
      comware_snmp_community: state=present access_right=read community_mib_view=view community_name=ansible_gqy  
      acl_number=3000 username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
      
- name: "Undo SNMP community"
    comware_snmp_community: state=absent access_right=write community_mib_view=view community_name=ansible_gqy  
    acl_number=2000 username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
```


#### Notes

```

	  
```
	
## comware_snmp_group
 Manages SNMP group configuration on H3C switches

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Manages SNMP group configuration on H3C switches

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| username  |   yes  |  | <ul></ul> |  Username used to login to the switch  |
| password  |   yes  |  | <ul></ul> |  Password used to login to the switch  |
| hostname  |   yes  |  | <ul></ul> |  IP Address or hostname of the Comware v7 device that has NETCONF enabled  |
| port  |   yes  |  830  | <ul></ul> |  NETCONF port number  |
| state  |   no  |  present  | <ul> <li>present</li>  <li>absent</li> </ul> |  Desired state for the interface configuration  |
| acl_number  |  no |  | <ul></ul> |  Access control list number |
| version  |   yes  |  | <ul></ul> |  The security model by this user is provided|
| group_name  |   no  |  | <ul></ul> |  Unique name for the group.  
| security_level  |   no  |  | <ul><li>noAuthNoPriv</li>  <li>authentication</li> </ul> |   Security level indicating whether to use authentication and encryption.  |
| read_view  |   no  |  | <ul></ul> |   Mib view name for read..  |
| write_view  |   no  |  | <ul></ul> |  Mib view name for write..  |
| notify_view  |   no  |  | <ul></ul> |   Mib view name for notification..  |


#### Examples

```
- name: "Config SNMP group"
   comware_snmp_group: state=present version=v2c group_name=wdz_group security_level=noAuthNoPriv acl_number=2000 
   username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
      
- name: "Undo SNMP group"
  comware_snmp_group: state=absent  version=v2c group_name=wdz_group security_level=noAuthNoPriv acl_number=2000 
   username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
    
- name: Config SNMP V3 group
    comware_snmp_group:
      state=present group_name=test_wl version=v3 security_level=authentication  acl_number=3000  write_view='testv3c'
      username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
      
- name: Config SNMP V3 group
    comware_snmp_group:
      state=absent group_name=test_wl version=v3 security_level=authentication  acl_number=3000  write_view='testv3c'
      username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
```


#### Notes

```

	  
```
	
## comware_snmp_target_host
Manages SNMP user configuration on H3c switches.

  * Synopsis
  * Options
  * Examples

#### Synopsis
Manages SNMP user configuration on H3c switches.

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| username  |   yes  |  | <ul></ul> |  Username used to login to the switch  |
| password  |   yes  |  | <ul></ul> |  Password used to login to the switch  |
| hostname  |   yes  |  | <ul></ul> |  IP Address or hostname of the Comware v7 device that has NETCONF enabled  |
| port  |   yes  |  830  | <ul></ul> |  NETCONF port number  |
| state  |   no  |  present  | <ul> <li>present</li>  <li>absent</li> </ul> |  Desired state for the interface configuration  |
| target_type  |  no |trap  | <ul><li>inform</li>  <li>trap</li> </ul> |  Notifications type |
| usm_user_name  |   yes  |  | <ul></ul> |  nique name for the user|
| server_address  |   yes  |  | <ul></ul> |  Address of the remote manage.  
| vpnname  |   no  |  | <ul> </ul> |   VRF instance name |
| user_group  |   yes  |  | <ul></ul> |  Unique name for the user group.  |
| sercurity_model  |   no  |  | <ul><li>v2</li>  <li>v2c</li><li>v3</li> </ul> |  The security model by this user is provided..  |
| security_level  |   no  | noAuthNoPriv | <ul><li>noAuthNoPriv</li>  <li>authentication</li><li>privacy</li></ul> |   The security level by this user is provided  |


#### Examples

```
- name: Config SNMP v3 TagetHost
  comware_snmp_target_host:
    state=absent target_type=trap server_address=10.1.1.1 usm_user_name=Uv3
    sercurity_model=v3 security_level=authentication vpnname=testvpn
    username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
          
- name: Undo SNMP v3 TagetHost
  comware_snmp_target_host:
    state=absent target_type=trap server_address=10.1.1.1 usm_user_name=Uv3
    vpnname=testvpn
    username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

- name: Config SNMP TagetHost
  comware_snmp_target_host:
    state=present target_type=trap server_address=100.1.1.1 usm_user_name=testuv2c 
    sercurity_model=v2c
    username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
          
- name: Undo SNMP TagetHost
  comware_snmp_target_host:
    state=present target_type=trap server_address=100.1.1.1 usm_user_name=testuv2c 
    sercurity_model=v2c vpnname=testvpn
    username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
```


#### Notes

```

	  
```
	
## comware_snmp_user
Manages SNMP user configuration on H3c switches..

  * Synopsis
  * Options
  * Examples

#### Synopsis
Manages SNMP user configuration on H3c switches.

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| username  |   yes  |  | <ul></ul> |  Username used to login to the switch  |
| password  |   yes  |  | <ul></ul> |  Password used to login to the switch  |
| hostname  |   yes  |  | <ul></ul> |  IP Address or hostname of the Comware v7 device that has NETCONF enabled  |
| port  |   yes  |  830  | <ul></ul> |  NETCONF port number  |
| state  |   no  |  present  | <ul> <li>present</li>  <li>absent</li> </ul> |  Desired state for the interface configuration  |
| acl_number  |  no |  | <ul> </ul> | Access control list number |
| usm_user_name  |   yes  |  | <ul></ul> |  nique name for the user|
| user_group  |   yes  |  | <ul></ul> |  Unique name for the user group..  
| sercurity_model  |   yes  |  | <ul><li>v2</li>  <li>v2c</li><li>v3</li> </ul>|  The security model by this user is provided|
| auth_protocol  |   yes  |  | <ul></ul> | Authentication algorithm.  |
| priv_protocol  |   no  |  | <ul> </ul> | Encryption algorithm privacy.  |
| auth_key  |   no  |  | <ul></ul> |   Authentication key. |
| priv_key  |   no  |  | <ul></ul> |   Privacy key.. |


#### Examples

```
- name: Config SNMP v3 User
    comware_snmp_user:
      state=present usm_user_name=gtest_w_ansbile sercurity_model=v3 user_group=gtest_w_ansbile
      auth_protocol=sha priv_protocol=3des auth_key=gtest_w_ansbile priv_key=gtest_w_ansbile
      username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

- name: undo SNMP v3 User
    comware_snmp_user:
      state=absent usm_user_name=gtest_w_ansbile sercurity_model=v3 user_group=gtest_w_ansbile
      auth_protocol=sha priv_protocol=3des auth_key=gtest_w_ansbile priv_key=gtest_w_ansbile
      username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

- name: Config SNMP v2c User
    comware_snmp_user:
      state=present usm_user_name=gtest_w_ansbile sercurity_model=v2c user_group=gtest_w_ansbile
      username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

- name: undo SNMP v2c User
    comware_snmp_user:
      state=absent usm_user_name=gtest_w_ansbile sercurity_model=v2c user_group=gtest_w_ansbile
      username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
```


#### Notes

```

	  
```
	
## comware_startup
config the next restart file or ipe .   patch function not available,please use patch module

  * Synopsis
  * Options
  * Examples

#### Synopsis
config the next restart file or ipe .   patch function not available,please use patch module

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| username  |   yes  |  | <ul></ul> |  Username used to login to the switch  |
| password  |   yes  |  | <ul></ul> |  Password used to login to the switch  |
| hostname  |   yes  |  | <ul></ul> |  IP Address or hostname of the Comware v7 device that has NETCONF enabled  |
| port  |   yes  |  830  | <ul></ul> |  NETCONF port number  |
| ipe_package  |  no |  | <ul> </ul> | File (including abs path path) of the local ipe package |
| boot  |   no  |  | <ul></ul> |  File (including abs path) of the local boot package (.bin)|
| system  |   no  |  | <ul></ul> | File (including abs path) of the local system package (.bin)  |
| patch  |   no  |  | <ul> </ul>|  File (including abs path) of the local patch package (.bin)|
| delete_ipe  |   yes  | false | <ul><li>true</li>  <li>false</li> <li>yes</li>  <li>no</li> </ul> | If ipe_package is used,this specifies whether the .ipe file is deleted from the device after it is unpacked.  |
| nextstartupfile  |   no  |  | <ul> </ul> | Name of file that will be used for the next start..  |
| filename  |   no  |  | <ul></ul> |   Name of file that will be show content. |
| show_file  |   no  |  | <ul></ul> |   File that will be used to store the config file content.  Relative path is location of ansible playbook. If not set, no file saved.. |


#### Examples

```
#Basic Install OS Bootsys
  comware_startup:
    boot='flash:/s9850_6850-cmw710-boot-r6555p01.bin'
    system='flash:/s9850_6850-cmw710-system-r6555p01.bin'
    patch='flash:/s9850_6850-cmw710-system-patch-r6555p01h31.bin'
    username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
      
#Basic Install OS IPE
  comware_startup: 
    ipe_package='flash:/s9850-h3c.ipe'
    username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
         
#Config next startup file
  comware_startup: 
    nextstartupfile='flash:/123.cfg'
    username={{ username }} password={{ password }} hostname={{ inventory_hostname }} 
      
#Show content for the existing config file
  comware_startup: filename='flash:/123.cfg' show_file='/root/ansible-hpe-cw7-master/123.cfg' username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

```


#### Notes

```
    - The parameters ipe_package and boot/system are
      mutually exclusive.
    - makesure the files are already existing on the device.
	  
```
	
## comware_stp
Manage stp global BPDU enable, working mode and tc-bpdu attack protection function.

  * Synopsis
  * Options
  * Examples

#### Synopsis
Manage stp global BPDU enable, working mode and tc-bpdu attack protection function.

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| username  |   yes  |  | <ul></ul> |  Username used to login to the switch  |
| password  |   yes  |  | <ul></ul> |  Password used to login to the switch  |
| hostname  |   yes  |  | <ul></ul> |  IP Address or hostname of the Comware v7 device that has NETCONF enabled  |
| port  |   yes  |  830  | <ul></ul> |  NETCONF port number  |
| state  |   no  |  present  | <ul> <li>present</li>  <li>absent</li> </ul> |  Desired state for the interface configuration  |
| bpdu  |  no |  | <ul><li>true</li>  <li>false</li> </ul> | Turn on the global BPDU protection function |
| mode  |   no  |  | <ul><li>MSTP</li>  <li>PVST</li> <li>RSTP</li>  <li>STP</li> </ul> |  Configure the working mode of the spanning tree|
| tc  |   no  |  | <ul><li>true</li>  <li>false</li></ul> | Enable anti tc-bpdu attack protection function  |
| patch  |   no  |  | <ul> </ul>|  File (including abs path) of the local patch package (.bin)|
| delete_ipe  |   yes  | false | <ul><li>true</li>  <li>false</li> <li>yes</li>  <li>no</li> </ul> | If ipe_package is used,this specifies whether the .ipe file is deleted from the device after it is unpacked.  |
| nextstartupfile  |   no  |  | <ul> </ul> | Name of file that will be used for the next start..  |
| filename  |   no  |  | <ul></ul> |   Name of file that will be show content. |
| show_file  |   no  |  | <ul></ul> |   File that will be used to store the config file content.  Relative path is location of ansible playbook. If not set, no file saved.. |


#### Examples

```
# Basic stp config
- comware_stp: bpdu=true mode=MSTP tc=true username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
# delete Basic stp config
- comware_stp: bpdu=true mode=MSTP tc=true state=absent username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
```


#### Notes

```
	
```
	
## comware_syslog_global
Manage system log timestamps and  terminal logging level on Comware 7 devices

  * Synopsis
  * Options
  * Examples

#### Synopsis
Manage system log timestamps and  terminal logging level on Comware 7 devices

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| username  |   yes  |  | <ul></ul> |  Username used to login to the switch  |
| password  |   yes  |  | <ul></ul> |  Password used to login to the switch  |
| hostname  |   yes  |  | <ul></ul> |  IP Address or hostname of the Comware v7 device that has NETCONF enabled  |
| port  |   yes  |  830  | <ul></ul> |  NETCONF port number  |
| state  |   no  |  present  | <ul> <li>present</li>  <li>absent</li> </ul> |  Desired state for the interface configuration  |
| timestamps  |  no | date | <ul><li>date</li>  <li>boot</li> <li>none</li></ul> | Configure the time stamp output format of log information sent to the console, monitoring terminal, log buffer and log file direction |
| level  |   no  | informational | <ul><li>informational</li>  <li>alert</li> <li>critical</li>  <li>debugging</li> <li>emergency</li> <li>error</li> <li>notification</li><li>warning</li> </ul> |  Configure the minimum level of log information that the current terminal allows to output.|
| tc  |   no  |  | <ul><li>true</li>  <li>false</li></ul> | Enable anti tc-bpdu attack protection function  |
| patch  |   no  |  | <ul> </ul>|  File (including abs path) of the local patch package (.bin)|
| delete_ipe  |   yes  | false | <ul><li>true</li>  <li>false</li> <li>yes</li>  <li>no</li> </ul> | If ipe_package is used,this specifies whether the .ipe file is deleted from the device after it is unpacked.  |
| nextstartupfile  |   no  |  | <ul> </ul> | Name of file that will be used for the next start..  |
| filename  |   no  |  | <ul></ul> |   Name of file that will be show content. |
| show_file  |   no  |  | <ul></ul> |   File that will be used to store the config file content.  Relative path is location of ansible playbook. If not set, no file saved.. |


#### Examples

```
  # timestamps and level config
  - comware_syslog_global: timestamps=boot  level=debugging username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

  # Restore timestamps and level to default state    
  - comware_syslog_global:timestamps=boot level=debugging username={{ username }} password={{ password }} hostname={{ inventory_hostname }} state=absent

```


#### Notes

```
    - Before configuring this,the global syslog need to be enabled.
    - The timestamps default state is data, terminal logging level default is 6.
	  
```
	
## comware_tele_stream
Manage telemetry global enable(disable) and telemetry stream timestamp enable(disable) and device-id on Comware 7 devices.Before config device-id,the timestamp must be enable

  * Synopsis
  * Options
  * Examples

#### Synopsis
Manage telemetry global enable(disable) and telemetry stream timestamp enable(disable) and device-id on Comware 7 devices.Before config device-id,the timestamp must be enable

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| username  |   yes  |  | <ul></ul> |  Username used to login to the switch  |
| password  |   yes  |  | <ul></ul> |  Password used to login to the switch  |
| hostname  |   yes  |  | <ul></ul> |  IP Address or hostname of the Comware v7 device that has NETCONF enabled  |
| port  |   yes  |  830  | <ul></ul> |  NETCONF port number  |
| state  |   no  |  present  | <ul> <li>present</li>  <li>default</li> </ul> |  Desired state for the interface configuration  |
| glo_enable  |  no | enable | <ul><li>enable</li>  <li>disable</li> </ul> |config global telemetry stream enable.The default state is enable |
| timestamp  |   no  | disable | <ul> <li>enable</li>  <li>disable</li> </ul> |  config telemetry stream timestamp enable.The default state is disable.|
| device-id  |   no  |  | <ul></ul> | config telemetry stream device-id  |


#### Examples

```
  # telemetry config
  - comware_tele_stream:
      glo_enable: enable
      timestamp: enable
	  deviceID: 10.10.10.1
      username: "{{ username }}"
      password: "{{ password }}"
      hostname: "{{ inventory_hostname }}"
      state: present
```


#### Notes

```

	  
```
	
## comware_teleFlowGroup_global
Manage telemetry flow group agingtime on Comware 7 devices.The default value is Varies by device.

  * Synopsis
  * Options
  * Examples

#### Synopsis
Manage telemetry flow group agingtime on Comware 7 devices.The default value is Varies by device.

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| username  |   yes  |  | <ul></ul> |  Username used to login to the switch  |
| password  |   yes  |  | <ul></ul> |  Password used to login to the switch  |
| hostname  |   yes  |  | <ul></ul> |  IP Address or hostname of the Comware v7 device that has NETCONF enabled  |
| port  |   yes  |  830  | <ul></ul> |  NETCONF port number  |
| state  |   no  |  present  | <ul> <li>present</li>  <li>default</li> </ul> |  Desired state for the interface configuration  |
| agtime  |  yes |  | <ul> </ul> |elemetry flow group agingtime |


#### Examples

```
  # telemetry Flow Group aging time config
  - comware_teteFlowGroup_global:
      agtime:20
      username: "{{ username }}"
      password: "{{ password }}"
      hostname: "{{ inventory_hostname }}"

 # config aging time into default state      
- comware_teteFlowGroup_global:
      agtime:20
      username: "{{ username }}"
      password: "{{ password }}"
      hostname: "{{ inventory_hostname }}"
      state: default
```


#### Notes

```

	  
```
	
## comware_TelemetryFlowTrace
 Manage Package information of the message sent to the collector on V7 devices

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Manage Package information of the message sent to the collector on V7 devices

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| username  |   yes  |  | <ul></ul> |  Username used to login to the switch  |
| password  |   yes  |  | <ul></ul> |  Password used to login to the switch  |
| hostname  |   yes  |  | <ul></ul> |  IP Address or hostname of the Comware v7 device that has NETCONF enabled  |
| port  |   yes  |  830  | <ul></ul> |  NETCONF port number  |
| state  |   no  |  present  | <ul> <li>present</li>  <li>absent</li> </ul> |  Desired state for the interface configuration  |
| sourceID  |  yes |  | <ul> </ul> |The source IP address of the packet package of the uplink collector |
| destinID  |  yes |  | <ul> </ul> |Destination IP address of the packet package of the uplink collector |
| sourcePort  |  yes |  | <ul> </ul> |The source port number of the message package of the up sending collector |
| destinPort  |  yes |  | <ul> </ul> |Destination port number of the message package of the uplink collector |

#### Examples

```
# basic config
- comware_TelemetryFlowTrace: sourceID=10.10.10.1 destinID=10.10.10.2 sourcePort=10 destinPort=30 username={{ username }} 
   password={{ password }} hostname={{ inventory_hostname }}

# delete config
 -comware_TelemetryFlowTrace: sourceID=10.10.10.1 destinID=10.10.10.2 sourcePort=10 destinPort=30 state=absent 
   username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
```


#### Notes

```
    - If state=absent, the config will be removed
	  
```
	
## comware_vpn_instance
config instance rely ensure some instance configs can be set

  * Synopsis
  * Options
  * Examples

#### Synopsis
config instance rely ensure some instance configs can be set

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| username  |   yes  |  | <ul></ul> |  Username used to login to the switch  |
| password  |   yes  |  | <ul></ul> |  Password used to login to the switch  |
| hostname  |   yes  |  | <ul></ul> |  IP Address or hostname of the Comware v7 device that has NETCONF enabled  |
| port  |   yes  |  830  | <ul></ul> |  NETCONF port number  |
| state  |   no  |  present  | <ul> <li>default</li>  <li>present</li>  <li>absent</li> </ul> |  Desired state for the interface configuration  |
| vpn_instance  |  yes |  | <ul> </ul> |Name of the VPN instance |
| vpn_instance_rd  |  no |  | <ul> </ul> |Route distinguisher, in the format ASN:nn or IP_address:nn |


#### Examples

```
     - name:  create and config ip vpn-instance
       comware_vpn_instance: vpn_instance=vpna vpn_instance_rd=1:1  address_family=ipv4  vpn_target=2:2 vpn_target_mode=both \
       username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

     - name:  create and config ip vpn-instance
       comware_vpn_instance: vpn_instance=vpna vpn_instance_rd=1:1  address_family=evpn  vpn_target=1:1 vpn_target_mode=both \
       username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

     - name:  create and config ip vpn-instance
       comware_vpn_instance: vpn_instance=vpna state=default username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
```


#### Notes

```
    - some of the instance configs can be set before ip vpn-instance and route-distinguisher already 
      exists . 
    - state default or absent will make the device default config , if you want delete instance insance
      autonomous_system and instance_instance are both required . if  you want delete vpn_instance, 
	  
```
## comware_vsi
Configure some command functions of vsi view

  * Synopsis
  * Options
  * Examples

#### Synopsis
Configure some command functions of vsi view

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| username  |   yes  |  | <ul></ul> |  Username used to login to the switch  |
| password  |   yes  |  | <ul></ul> |  Password used to login to the switch  |
| hostname  |   yes  |  | <ul></ul> |  IP Address or hostname of the Comware v7 device that has NETCONF enabled  |
| port  |   yes  |  830  | <ul></ul> |  NETCONF port number  |
| state  |   no  |  present  | <ul>  <li>present</li>  <li>absent</li> </ul> |  Desired state for the interface configuration  |
| vsi  |  yes |  | <ul> </ul> |Name of the VSI |
| gateway_intf  |  no |  | <ul> </ul> |vsi view Gateway configuration interface|
| gateway_subnet  |  no |  | <ul> </ul> |Name of the VSI |
| gateway_mask  |  no |  | <ul> </ul> |vsi view Gateway configuration subnet wild card mask |
| vxlan  |  no |  | <ul> </ul> |Specify a Virtual eXtensible LAN |
| encap  |  no |  | <ul><li>true</li>  <li>false</li>  </ul> |Ethernet virtual private network module |
| rd  |  no |  | <ul> </ul> |Configure a route distinguisher |
| vpn_target_auto  |  no |  | <ul> <li>both</li>  <li>import</li>  <li>export</li> </ul> |Configure route targets|


#### Examples

```
     # - name:  config vsi
       # comware_vsi: vsi=vpna gateway_intf=Vsi-interface1 gateway_subnet=10.1.1.0 gateway_mask=0.0.0.255 vxlan=10 \
       encap=true rd=auto vpn_target_auto=both username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
       
     # - name:  delelte vsi configs
       # comware_vsi: vsi=vpna state=default username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

```


#### Notes

```
    - l2vpn needs to enbled before config vsi view.
    - If you want to use vsi gateway interface, it must be exist , you can use interface module to create it.
    - when giving vsi and state is default , it will delete the given vsi config all.
	  
```
	
## comware_vsi_intf
Configure some functions of vsi-interface

  * Synopsis
  * Options
  * Examples

#### Synopsis
Configure some functions of vsi-interface

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| username  |   yes  |  | <ul></ul> |  Username used to login to the switch  |
| password  |   yes  |  | <ul></ul> |  Password used to login to the switch  |
| hostname  |   yes  |  | <ul></ul> |  IP Address or hostname of the Comware v7 device that has NETCONF enabled  |
| port  |   yes  |  830  | <ul></ul> |  NETCONF port number  |
| state  |   no  |  present  | <ul>  <li>present</li>  <li>absent</li> </ul> |  Desired state for the interface configuration  |
| vsi_intf  |  yes |  | <ul> </ul> |The vsi interface view to config |
| binding  |  no |  | <ul> </ul> |Bind the interface with a VPN instance|
| macaddr  |  no |  | <ul> </ul> |config MAC address information |
| local_proxy  |  no |  | <ul> <li>nd</li>  <li>arp</li> </ul> |Enable local proxy ARP or ND function|
| distribute_gateway  |  no |  | <ul> <li>local</li></ul> |Specify the VSI interface as a distributed gateway |



#### Examples

```
     # - name:  config vsi
       # comware_vsi_intf: vsi_intf=Vsi-interface1 binding=vpna macaddr=201a-101a-40fa  local_proxy=arp \
       distribute_gateway=local username={{ username }} password={{ password }} hostname={{ inventory_hostname }}
```


#### Notes

```
    - l2vpn needs to enbled before config vsi view.
    - vsi_intf must be vsi interface type , the module is only used for config vsi interface.
    - If you want to bind a interface with VPN instance, the VPN instance must be already exist.
	  
```
Created by Network to Code, LLC
For:
2015
