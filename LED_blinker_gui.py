from arduinoSerial import Arduino
import signal
import sys
import tkinter as tk
from tkinter import ttk


# Some functions for buttons
def port_connect(port):
    arduino.close()
    connected = arduino.connect(port=port, baudrate=9600, timeout=1)
    if connected:
        info_label.config(text=f"Connected to {port}!", fg='green')
    else:
        info_label.config(text=f"Could not connect to {port}!", fg='red')

def port_disconnect():
    arduino.close()
    info_label.config(text=f"Disconnected.", fg='red')


if __name__ == "__main__":
    # To catch keyboard Interrupt and close the port.
    def sigint_handler(signal, frame):
        arduino.close()
        print ("Interrupted, closing port.")
        sys.exit(0)
    signal.signal(signal.SIGINT, sigint_handler)
        
    arduino = Arduino()
    ports= arduino.get_available_ports(print_ports=False)
    
    root = tk.Tk()
    root.title('Arduino Bluetooth')
    height, width = 240, 280
    root.geometry(f'{width}x{height}')
    root.resizable(False, False)

    options = {'padx': 5, 'pady': 5}

    # Container for bluetooth connection widgets
    connection_frame = ttk.Frame(root)
    connection_frame.pack()

    # Datatype of menu text
    selected_port = tk.StringVar()
    # Initial menu text
    selected_port.set(ports[0])
    
    # Create Dropdown menu
    port_menu = tk.OptionMenu(connection_frame, selected_port, *ports)
    port_menu.pack(side=tk.LEFT, 
                   padx=options['padx'], pady=options['pady'])
    port_menu.configure(width=16)

    # Port Connect button:
    connect_button = tk.Button(connection_frame, 
                               text="Connect", 
                               command= lambda: port_connect(selected_port.get()))
    connect_button.pack(side=tk.LEFT, 
                        padx=options['padx'], pady=options['pady'])

    # Info Message
    info_frame = tk.LabelFrame(root)
    info_frame.pack(fill='x', padx=8)
    info_label = tk.Label(info_frame, text="Select a port")
    info_label.pack()

    # LED Button Frame
    led_frame = tk.Frame(root)
    led_frame.pack(padx=0, pady=16)
    # LED Buttons
    on_button = tk.Button(led_frame, 
                          text="ON", height=2, width=4, 
                          highlightbackground='#529b22',
                          font = ("TkDefaultFont", 34),
                          command=lambda: arduino.write('1'))
    on_button.pack(side=tk.LEFT,
                   padx=6, pady=0)
    
    off_button = tk.Button(led_frame, 
                           text="OFF", height=2, width=4, 
                           highlightbackground='#5f0000',
                           font = ("TkDefaultFont", 34),
                           command=lambda: arduino.write('0'))
    off_button.pack(side=tk.RIGHT, 
                    padx=6, pady=0)
    
    # Disconnect Button
    disconnect_frame = tk.Frame(root)
    disconnect_frame.pack(padx=5, pady=5, fill='x')

    disconnect_button = tk.Button(disconnect_frame, 
                                  text='Disconnect', 
                                  fg='red', 
                                  command=port_disconnect)
    disconnect_button.pack(fill='x')

    # Execute tkinter
    root.mainloop()
    arduino.close()