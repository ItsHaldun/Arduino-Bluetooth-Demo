from arduinoSerial import Arduino
import signal
import sys
import tkinter as tk
from tkinter import ttk

# TODO:
# Add GUI with Tkinter
# Include a dropdown list for connections
# Connect button, disconnect button
# LED ON/OFF Buttons

def find_bluetooth(ports):
    bluetooth_modules = []
    for port, desc, hwid in sorted(ports):
        # If bluetooth module, add it to the list
        if(port.find("HC-05") != -1 or port.find("HC-06") != -1):
            bluetooth_modules.append(port)
    return bluetooth_modules


if __name__ == "__main__":
    # To catch keyboard Interrupt and close the port.
    def sigint_handler(signal, frame):
        arduino.close()
        print ("Interrupted, closing port.")
        sys.exit(0)
    signal.signal(signal.SIGINT, sigint_handler)

    arduino = Arduino()
    ports = arduino.get_available_ports(print_ports=False)

    print(ports[0])
    bluetooth_ports = find_bluetooth(ports)

    if len(bluetooth_ports) == 0:
        raise(Exception("No Bluetooth Modules found."))
    
    for port in bluetooth_ports:
        try:
            arduino.connect(port=port, baudrate=9600, timeout=0.2)
            print(f"Connected to {port} at baudrate {9600}.")
            break
        except:
            continue
    
    # Main program:
    while True:
        commd = input("Enter: ")
        if commd == 'q':
            arduino.close()
            print("Port closed, exiting.")
            sys.exit(0)
        elif commd == '1':
            arduino.write('1', end='')
            print(arduino.read_line())
        elif commd == '0':
            arduino.write('0', end='')
            print(arduino.read_line())