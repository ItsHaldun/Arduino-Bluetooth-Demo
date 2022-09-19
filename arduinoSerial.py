import serial
from time import sleep
from serial.tools import list_ports

class Arduino:
    def __init__(self) -> None:
        self.ports = self.get_available_ports()
        self.device = None
        self.isConnected = False
    
    def get_available_ports(self, print_ports:bool=False):
        if(print_ports):
            print("Available Ports:")

        ports = []
        for port, desc, hwid in sorted(list_ports.comports()):
            if(print_ports):
                print("{}: {} [{}]".format(port, desc, hwid))
            ports.append(port)
        return ports

    def connect(self, port:str, baudrate:int, timeout:float):
        try:
            self.device = serial.Serial(port=port, baudrate=baudrate, timeout=timeout)
            return True
        except:
            return False
        
    
    def write(self, msg:str, end:str='\n', encoding='ascii'):
        if(self.device is not None):
            msg = msg + end
            self.device.write(bytes(msg, encoding=encoding))
    
    def read_line(self):
        if(self.device is not None):
            data =self.device.readline().decode().rstrip('\n')
            return data

    def close(self):
        if self.device is not None:
            self.device.close()


if __name__ == "__main__":
    # This is a blinking light test over bluetooth serial
    arduino = Arduino()
    arduino.get_available_ports(print_ports=True)

    selected = input("Enter port: ")
    arduino.connect(port=selected, baudrate=9600, timeout=0.2)
    sleep(0.15)
    print(arduino.read_line())

    # '1' turns on LED
    # '0' turns off LED
    
    i=0
    while(i<5):
        arduino.write('1', end='')
        print(arduino.read_line())
        sleep(1)
        arduino.write('0', end='')
        print(arduino.read_line())
        sleep(1)
        i+=1
    arduino.close()