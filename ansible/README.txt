Automatic Cisco SSH & Network Configuration
=============================================

This repository is part of a project to automate the configuration of Cisco devices using Ansible. Once you have enabled SSH on all devices (using the Python script from Automatic-SSH-Setup: https://github.com/traaseth/Automatic-SSH-Setup.git), you can use this Ansible portion to further configure the devices via SSH. The setup includes:

• Configuration of two routers with HSRP and DHCP for each VLAN.
• Configuration of two switches, where SG3 is configured with EtherChannel.

The project is built to be reusable. All configuration is based on variables defined in YAML files.

------------------------------------------------------------
Directory Structure
------------------------------------------------------------
ansible-network-automation/
├── inventory/
│   └── hosts.ini         # Inventory file with IP addresses, usernames, and passwords for all devices.
├── playbooks/
│   └── site.yml          # Main playbook that includes roles for both routers and switches.
├── roles/
│   ├── router_config/    # Role for router configuration (HSRP, subinterfaces, DHCP).
│   │   └── tasks/
│   │       └── main.yml
│   └── switch_config/    # Role for switch configuration (trunk, EtherChannel).
│       └── tasks/
│           └── main.yml
├── host_vars/
│   ├── RG1.yml           # Variables for Router Green 1 (e.g., VLAN, HSRP, DHCP).
│   ├── RG2.yml           # Variables for Router Green 2.
│   ├── SG1.yml           # Variables for Switch Green 1.
│   └── SG3.yml           # Variables for Switch Green 3 (configured with EtherChannel).
├── requirements.yml      # Ansible-galaxy dependencies (cisco.ios collection).
└── README.txt            # This README file.

------------------------------------------------------------
Prerequisites
------------------------------------------------------------
1. SSH for all devices is already set up using the Python script 
   (see Automatic-SSH-Setup: https://github.com/traaseth/Automatic-SSH-Setup.git).
2. Ansible is installed (Ansible Core/Ansible 2.9+).
3. The Cisco IOS collection is installed:
   
   ansible-galaxy collection install cisco.ios

4. All devices are connected to the network with IP

------------------------------------------------------------
Configuration
------------------------------------------------------------
Inventory File (inventory/hosts.ini):
-------------------------------------
[routers]
RG1 ansible_host=172.16.0.2
RG2 ansible_host=172.16.0.3

[switches]
SG1 ansible_host=172.16.0.21
SG3 ansible_host=172.16.0.23

[routers:vars]
ansible_network_os=cisco.ios.ios
ansible_connection=network_cli
ansible_user=cisco
ansible_password=cisco
ansible_become=yes
ansible_become_method=enable
ansible_become_password=cisco

[switches:vars]
ansible_network_os=cisco.ios.ios
ansible_connection=network_cli
ansible_user=cisco
ansible_password=cisco
ansible_become=yes
ansible_become_method=enable
ansible_become_password=cisco

------------------------------------------------------------
Host Variables (host_vars/)
-------------------------------------
Example for RG1 (host_vars/RG1.yml):

vlan_interfaces:
  - vlan_id: 20
    ip: 172.16.0.2
    mask: 255.255.255.0
    hsrp_ip: 172.16.0.1
    hsrp_priority: 120
  - vlan_id: 30
    ip: 172.16.1.2
    mask: 255.255.255.0
    hsrp_ip: 172.16.1.1
    hsrp_priority: 120

dhcp_pools:
  - name: VLAN20
    network: 172.16.0.0
    mask: 255.255.255.0
    default_router: 172.16.0.1
    dns_server: 8.8.8.8
  - name: VLAN30
    network: 172.16.1.0
    mask: 255.255.255.0
    default_router: 172.16.1.1
    dns_server: 8.8.4.4

For RG2, SG1, and SG3, the variables are defined similarly. For SG3 (EtherChannel), variables include:
  port_channel_id: 1
  port_channel_mode: active
  etherchannel_members:
    - GigabitEthernet0/1
    - GigabitEthernet0/2

------------------------------------------------------------
How to Run the Setup
------------------------------------------------------------
1. Install dependencies:
   ansible-galaxy collection install -r requirements.yml
2. Update the inventory and host_vars files with appropriate values for your environment.
3. From the project root, run:
   ansible-playbook -i inventory/hosts.ini playbooks/site.yml
4. Verify the configuration:
   - On routers, check HSRP with: show standby and DHCP pools with: show ip dhcp pool.
   - On SG3, verify EtherChannel with: show etherchannel summary.


------------------------------------------------------------
License
------------------------------------------------------------
This project is available under the MIT license – free to use, modify, and distribute.
