This Python script automates the setup of SSH on a Cisco router via serial (console) connection. It handles RSA key generation (including overwrite prompts), sets hostname/domain, configures a local user, enables SSH version 2, and prepares VTY lines for SSH login.

⚙️ Requirements
WSL (Windows Subsystem for Linux) with Ubuntu (https://learn.microsoft.com/en-us/windows/wsl/install)

Python 3

pyserial installed
Install with:

bash
Copy
Edit
pip3 install pyserial

🖥️ How to Use
Connect your Cisco router to your PC using a serial console cable.

Find your serial port in WSL (typically /dev/ttyS#).
Example: /dev/ttyS4 maps to COM5 in Windows.

Edit the script:

On line 19, change the serial_port value to match your port (e.g. /dev/ttyS4).

On line 69, change the username and password in this command:

python
Copy
Edit
send_command(ser, 'username cisco privilege 15 secret cisco', wait=2)
Replace both cisco values with your desired SSH login credentials.

Run the script:

bash
Copy
Edit
sudo python3 setup_ssh.py

✅ What the Script Does
Enters privileged mode (enable)

Sets:

Hostname to RG1

IP domain to test.local

Handles RSA key generation and overwrites if needed

Creates a local SSH user

Enables SSH version 2

Configures VTY lines for SSH login

Saves the configuration (write memory)

💡 Tips
The script works best on Cisco IOS-based routers (e.g. 4221, ISR-series).

If you encounter a WinError 10060 or 10051 in earlier versions of the script, this version resolves it by using only the serial console to configure SSH — no Paramiko or IP is needed.

