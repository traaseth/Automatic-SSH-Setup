import serial
import time

def send_command(ser, command, wait=1):
    ser.write(b'\r\n')
    time.sleep(wait)
    ser.write((command + '\r\n').encode('utf-8'))
    time.sleep(wait)
    ser.flush()
    time.sleep(wait)
    output = []
    while ser.in_waiting > 0:
        line = ser.readline().decode('utf-8', errors='ignore').strip()
        output.append(line)
    return output

def main():
    print("starting")
    serial_port = '/dev/ttyS5'  # <-- Adjust to your port (e.g., COM4 on Windows or ttyUSB0 on Linux)
    baud_rate = 9600
    ser = serial.Serial(
        port=serial_port,
        baudrate=baud_rate,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        timeout=1
    )
    
    print("setting serial")
    time.sleep(2)
    ser.reset_input_buffer()
    
    send_command(ser, 'enable')
    time.sleep(1)
    send_command(ser, 'terminal length 0')
    send_command(ser, 'terminal dont-ask')
    send_command(ser, 'configure terminal')
    send_command(ser, 'hostname SG1')
    send_command(ser, 'ip domain name test.local')
    send_command(ser, 'interface Gig0/0/0')
    send_command(ser, 'ip address 192.168.0.4 255.255.254.0')


    # Start RSA key generation
    print("Sending 'crypto key generate rsa'")
    ser.write(b'crypto key generate rsa\r\n')
    time.sleep(2)

    # Look for overwrite prompt or modulus prompt
    response = b""
    start_time = time.time()
    while time.time() - start_time < 10:
        if ser.in_waiting > 0:
            response += ser.read(ser.in_waiting)
            if b"[yes/no]" in response:
                print("Detected key overwrite prompt. Sending 'yes'")
                ser.write(b'yes\r\n')
                time.sleep(2)
                break
            if b"bits in the modulus" in response or b"modulus [" in response:
                print("Modulus prompt detected.")
                break
        time.sleep(0.5)

    # Send modulus value (e.g. 2048)
    print("Sending modulus size: 2048")
    ser.write(b'2048\r\n')
    time.sleep(3)

    # Continue SSH setup
    send_command(ser, 'username cisco privilege 15 secret cisco', wait=2)
    send_command(ser, 'ip ssh version 2')
    send_command(ser, 'line vty 0 4')
    send_command(ser, 'transport input ssh')
    send_command(ser, 'login local')
    send_command(ser, 'end', wait=2)
    send_command(ser, 'write memory', wait=3)

    print("SSH setup complete.")
    ser.close()

if __name__ == '__main__':
    main()
