# Environment
- CentOS: CentOS Linux release 7.9.2009 (Core)
- Python: 3.7.4
- Ansible: 2.10.4

# Getting started

## Install CentOS
During demo, the CentOS-7-x86_64-DVD-2009.iso was used. It can be downloaded from [here](http://yum.tamu.edu/centos/7.9.2009/isos/x86_64/CentOS-7-x86_64-DVD-2009.iso) or 
[other mirros](http://isoredirect.centos.org/centos/7/isos/x86_64/).  

## Install Python-3.7.4
### 1. Install dependent packages  
```
yum install gcc make zlib  zlib-devel openssl openssl-devel libffi-devel bzip2-devel ncurses-devel gdbm-devel readline-devel xz-devel sqlite-devel tk-devel -y
```

### 2. Download the compressed package  
Download [Python-3.7.4](https://www.python.org/ftp/python/3.7.4/Python-3.7.4.tgz)  
```
wget https://www.python.org/ftp/python/3.7.4/Python-3.7.4.tgz
```

### 3. Unzip and install  
```
tar -zxvf Python-3.7.4.tgz
cd Python-3.7.4/
./configure prefix=/usr/local/python3
make && make install
```

### 4. Create soft links  
Test the Python3 path:  
```
/usr/local/python3/bin/python3 --version
```
The command  
```
find / -name python3
```
can be used to find the path to Python 3.  

Create soft links:
```
ln -s /usr/local/python3/bin/python3 /usr/bin/python3
ln -s /usr/local/python3/bin/pip3 /usr/bin/pip3
```

## Install Ansible
### 1. Installation
```
pip3 install markupsafe
pip3 install ansible==2.10.4
```

### 2. Check  
After installation, run the below command
```
ansible --version
```
to check if Ansible can be executed directly. Otherwise, create a soft link to Ansible.  
```
ln -s /usr/local/python3/bin/ansible /usr/bin/ansible
```
The installation path to ansible varies. The below command can help to find out the real path.
```
find / -name ansible
```

## Library installation
### 1. Download the library  
Download the [hpe-cw7-ansible](https://github.com/HPENetworking/hpe-cw7-ansible) library.
```
wget https://github.com/HPENetworking/hpe-cw7-ansible/archive/refs/heads/main.zip
```

### 2. Install dependencies  
Some dependent packages are not self-contained by the library. They should be installed manually. The dependencies and corresponding versions are:  
```
ncclient==0.6.9
scp==0.13.3
textfsm==1.1.0
ipaddr==2.2.0
```

Install the dependencies by pip3.
```
pip3 install ncclient==0.6.9
pip3 install scp==0.13.3
pip3 install textfsm==1.1.0
pip3 install ipaddr==2.2.0
```

### 3. Decompress the library file  
```
unzip main.zip
```

### 4. Replace files of ncclient
```
cd hpe-cw7-ansible-main/
cp ./for-ncclient/rpc.py /usr/local/python3/lib/python3.7/site-packages/ncclient/operations/rpc.py
cp ./for-ncclient/manager.py /usr/local/python3/lib/python3.7/site-packages/ncclient/manager.py
```
**Note:** The paths of the two files 'rpc.py' and 'manager.py' vary with installation.

### 5. Install the library
```
cd hpe-cw7-ansible-main/
chmod 777 setup.py
python3 setup.py install
```

## Switch configuration
```
local-user hpe
 password simple hpe
 authorization-attribute user-role network-admin
 service-type ssh

netconf ssh server enable
 line vty 0 15
 authentication-mode scheme
 user-role network-admin

ssh server enable
ssh user hpe service-type all authentication-type password
scp server enable
```
## Add switch dns name into etc/host file
### etc/host file
Add the dns mapping into etc/host file, i.e.
```
172.17.8.10 hpe1
172.17.8.12 hpe2
172.17.8.11 hpe3
```

## Test reachability
Use Ping to test the reachability, i.e.
```
[admin@demo]# ping hpe1
PING hpe1 (172.17.8.10) 56(84) bytes of data.
64 bytes from hpe1 (172.17.8.10): icmp_seq=1 ttl=255 time=0.585 ms
64 bytes from hpe1 (172.17.8.10): icmp_seq=2 ttl=255 time=0.455 ms
^C
--- hpe1 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1001ms
rtt min/avg/max/mdev = 0.455/0.520/0.585/0.065 ms
```

## Test connection to switch
```
[root@demo]# python3
Python 3.7.4 (default, Jan  6 2022, 14:21:40) 
[GCC 4.8.5 20150623 (Red Hat 4.8.5-44)] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from pyhpecw7.comware import HPCOM7
>>> args = dict(host='hpe1', username='hpe', password='hpe', port=830)
>>> device = HPCOM7(**args)
>>> device.open()
<ncclient.manager.Manager object at 0x7f3ed5953150>
```

## Ansible configuration
### ansible.conf file
Add the path of Ansible library, in order to execute playbooks at anywhere.
1. Create the ansible config file, if it does not exist.
```
vim /etc/ansible/ansible.cfg
```
2. Fill the config file with the library path.
```
[defaults]
library = /root/hpe-cw7-ansible-main/library
```

## Playbook execution
### 1. Prepare host file
```
[all:vars]
username=hpe
password=hpe
ansible_python_interpreter=/usr/bin/python3
[switches]
hpe1
hpe2
hpe3
```

### 2. Prepare playbook
Take the hp-vlans.yml for example:
```
---

  - name: VLAN Automation with Ansible on HP Com7 Devices
    hosts: hpe1 hpe2
    gather_facts: no
    connection: local

    tasks:

      - name: ensure VLAN 10 exists
        comware_vlan: vlanid=10 name=VLAN10_WEB descr=LOCALSEGMENT username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

      - name: ensure VLAN 20 exists
        comware_vlan: vlanid=20 name=VLAN20 state=present username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

      - name: ensure VLAN 10 does not exist
        comware_vlan: vlanid=10 state=absent username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

```

### 3. Execute the playbooks
Run the ansible-playbook command to test the scripts, i.e.
```
ansible-playbook -i hosts hp-vlans.yml 
```
**Note:** 
* Error - ansible-playbook: command not found
The command below can help to find the correct path. Run the command in the directory or create a soft link to the file. 
```
find / -name ansible-playbook
```
* Make sure the hosts file and playbook files in the correct directory.

The result is similar to below.
```
[admin@demo]#ansible-playbook -i hosts hp-vlans.yml 

PLAY [VLAN Automation with Ansible on HP Com7 Devices] *****************************************************************************

TASK [ensure VLAN 10 exists] *******************************************************************************************************
[WARNING]: Module did not set no_log for password
changed: [hpe1]
changed: [hpe2]

TASK [ensure VLAN 20 exists] *******************************************************************************************************
changed: [hpe1]
changed: [hpe2]

TASK [ensure VLAN 10 does not exist] ***********************************************************************************************
changed: [hpe1]
changed: [hpe2]

PLAY RECAP *************************************************************************************************************************
hpe1                       : ok=3    changed=3    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
hpe2                       : ok=3    changed=3    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0 
```

## Demo log
The log of the demo can be found in the file [demo-log](demo/demo-log).  





