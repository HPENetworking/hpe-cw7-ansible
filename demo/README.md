# hpe-cw7-ansible - demo

## Environment
- CentOS: CentOS Linux release 7.9.2009 (Core)
- Python: 3.7.4
- Ansible: 2.10.4

## Getting started

### Install CentOS
During demo, the CentOS-7-x86_64-DVD-2009.iso was used. It can be downloaded from [here](http://yum.tamu.edu/centos/7.9.2009/isos/x86_64/CentOS-7-x86_64-DVD-2009.iso) or 
[other mirros](http://isoredirect.centos.org/centos/7/isos/x86_64/).  

### Install Python-3.7.4
1. Install dependent packages  
```
yum install gcc make zlib  zlib-devel openssl openssl-devel libffi-devel bzip2-devel ncurses-devel gdbm-devel readline-devel xz-devel sqlite-devel tk-devel -y
```

2. Download the compressed package  
Download [Python-3.7.4](https://www.python.org/ftp/python/3.7.4/Python-3.7.4.tgz)  
```
wget https://www.python.org/ftp/python/3.7.4/Python-3.7.4.tgz
```

3. Unzip and install  
```
tar -zxvf Python-3.7.4.tgz
cd Python-3.7.4/
./configure prefix=/usr/local/python3
make && make install
```

4. Create soft links  
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

### Install Ansible
1. Installation
```
pip3 install markupsafe
pip3 install ansible==2.10.4
```

2. Check  
After installation, run the below command
```
anbible --version
```
to check if Ansible can be executed directly. Otherwise, create a soft link to Ansible.  
```
ln -s /usr/local/python3/bin/ansible /usr/bin/ansible
```
The installation path to ansible varies. The below command can help to find out the real path.
```
find / -name ansible
```

### Library installation
1. Downlaod the library  
Download the [hpe-cw7-ansible](https://github.com/HPENetworking/hpe-cw7-ansible) library.
```
wget https://github.com/HPENetworking/hpe-cw7-ansible/archive/refs/heads/main.zip
```

2. Install dependencies  
Some dependency packages are not self-contained by the library. They should be installed manually. The dependencies and corresponding versions are:  
```
ncclient==0.6.9
scp==0.13.3
textfsm==1.1.0
ipaddr==2.2.0
```

Install the dependencies by pip3.
```
pip3 instanll ncclient==0.6.9
pip3 instanll scp==0.13.3
pip3 instanll textfsm==1.1.0
pip3 instanll ipaddr==2.2.0
```

3. Decompress the library file  
```
unzip main.zip
```

4. Replace files of ncclient
```
cd hpe-cw7-ansible-main/
cp ./for-ncclient/rpc.py /usr/local/lib/python3.7/site-packages/ncclient/operations/rpc.py
cp ./for-ncclient/manager.py /usr/local/python3/lib/python3.7/site-packages/ncclient/manager.py
```
Note: The paths of the two files 'rpc.py' and 'manager.py' vary with installation.

5. Install the library
```
cd hpe-cw7-ansible-main/
chmod 777 setup.py
python3 setup.py install
```

### Switch configuration

please help to fill the switch configuration necessary for anbible testing

### Test connection to switch
```
python3
from pyhpecw7.comware import HPCOM7
args = dict(host='hpe1', username='hpe', password='test123456', port=830)
device = HPCOM7(**args) 
device.open()
```

Please help to send me the logs

### Ansible configuration
1. etc/host file

please help to fill the content

2. ansible.conf file

please help to fill the content

### Playbook execution

please help to send me the logs for the 3 playbooks

hp-interfaces.yml
hp-portchannel.yml
hp-vlans.yml






