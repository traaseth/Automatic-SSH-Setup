README – Cisco Switch and Router Initial Configuration Scripts
==============================================================

These scripts and Ansible playbooks are designed to automate the base configuration
of Cisco switches and routers via serial connection and Ansible over SSH, enabling
VLAN, DHCP, and SSH setup for network devices in lab or production settings.

What You Need
-------------

Hardware:
- A Cisco router and/or switch with console access
- A serial connection (e.g., USB-to-serial cable or COM port)

Software:
- A working Linux system or WSL (Windows Subsystem for Linux)
  Guide: https://learn.microsoft.com/en-us/windows/wsl/install
- Python 3
- PIP (Python package manager)
- Ansible
- Ansible Galaxy collection for Cisco IOS:
    ansible-galaxy collection install cisco.ios

File Overview
-------------

Python Scripts (used for initial serial setup):
- SSHsetupSwitch.py  : Sets up a Cisco switch via serial. Adds VLAN 90, assigns IP,
                        enables SSH, and saves config.
- SSHsetupRuter.py   : Sets up a Cisco router via serial. Configures interface, domain,
                        SSH, and user login.

Ansible Playbooks (used after SSH is available):
- SwitchSG1.yml      : Configures a Cisco switch via SSH: creates VLAN 10, assigns access
                        ports, keeps VLAN 90 alive.
- config ruter.yml   : Configures a Cisco router via SSH: sets interface IPs and configures
                        a DHCP pool with exclusions.

System-Specific Changes You Must Make
-------------------------------------

1. Serial Port Adjustment:
   - In both SSHsetupSwitch.py and SSHsetupRuter.py:
     Edit line like this to match your COM port:
       serial_port = '/dev/ttyS5'  → change to your actual port

2. Hostname and Interface Configuration:
   - In SSHsetupRuter.py:
     Line 39: change the hostname to match your device naming
       send_command(ser, 'hostname SG1')
     Line 40, 44, 51: set your actual VLAN ID
       send_command(ser, 'vlan 90')
     Line 45: your actual IP address/subnet for MGMT interface
       send_command(ser, 'ip address 192.168.90.5 255.255.255.0')
     Line 49: the physical port to put in VLAN 90
     Line 55: set your network's correct default gateway
     Line 85: set your preferred username and password

   - In SSHsetupSwitch.py:
     Update lines as needed to match:
       - Serial port
       - VLAN ID, IP address
       - Gateway
       - SSH credentials

3. Ansible Inventory Configuration:
   Edit your `inventory.ini` or YAML inventory:

   [router]
   RG1 ansible_host=<your-router-ip>

   [switch]
   SG1 ansible_host=<your-switch-ip>

   [all:vars]
   ansible_user=cisco
   ansible_password=cisco
   ansible_network_os=cisco.ios
   ansible_connection=network_cli
   ansible_become=true
   ansible_become_method=enable
   ansible_enable_password=cisco

4. DHCP Variables (in config ruter.yml):
   Under `vars:` → update these:
     - pool_name
     - network and netmask
     - default_router
     - dns_server
     - excluded_ips (e.g. gateway and static devices)

5. VLAN Access Ports (in SwitchSG1.yml):
   - Update the `access_ports:` list to match the physical interfaces you want to use.

Running Steps
-------------

1. Connect via Serial and Run Python Script:
   python3 SSHsetupSwitch.py
   OR
   python3 SSHsetupRuter.py

2. Verify SSH:
   ssh cisco@192.168.X.X

3. Run Playbooks:
   ansible-playbook -i inventory.ini config\ ruter.yml
   ansible-playbook -i inventory.ini SwitchSG1.yml

Troubleshooting
---------------

- Permission Denied on Serial:
    - Ensure no other program (e.g., Putty) is using the COM port.
    - Try: sudo chmod 666 /dev/ttyS5 or configure /etc/wsl.conf for WSL.

- SSH Timeout:
    - Ensure SVI (e.g., Vlan90) is up/up with IP.
    - At least one interface (e.g., Gig1/0/1) must be in the same VLAN and up.

