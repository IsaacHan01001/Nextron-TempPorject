import serial
from serial.tools.list_ports import *
import serial
import time

class Instrument:
    def __init__(self, aPort, chr):
        # Initialize the serial connection
        self.device = serial.Serial(aPort, timeout=0.5)
        self.chr = chr
        # Configure the serial connection parameters
        self.device.baudrate = 19200
        self.device.bytesize = serial.EIGHTBITS  # Use serial.EIGHTBITS for clarity
        self.device.stopbits = serial.STOPBITS_ONE  # Use serial.STOPBITS_ONE for clarity
        self.device.xonxoff = False
        self.device.rtscts = False
        self.device.dsrdtr = False
        self.device.parity = serial.PARITY_NONE  # Use serial.PARITY_NONE for clarity

    def close(self):
        self.device.close()

    def write(self, data):
        """Write data to the serial port."""
        self.device.write(data.encode())  # Ensure data is encoded as bytes

    def read(self, option=28):
        """Read data from the serial port."""
        return self.device.read(option)

    def __del__(self):
        """Ensure the serial connection is closed when the object is destroyed."""
        self.close()

    def isAlicat(self):
        self.device.write(f"{self.chr}??m*\r".encode())
        response = self.read()
        print(response)
        return "ALICAT" in str(response)

    def factoryReset(self):
        self.device.write(f"{self.chr}FACTORY RESTORE ALL\r".encode())
        print("Device is reset to factory setting")
        print("self.channel changed to A")
        self.chr = "A"

    def changeUnitID(self, toChr, fromChr=None):
        if fromChr is None:
            self.device.write(f"{self.chr}@ {toChr}\r".encode())
        else:
            self.device.write(f"{fromChr}@ {toChr}\r".encode())
        print("Critical: the device unit ID changed")
        self.chr = toChr


    def setGasN2(self):
        self.device.write(f"{self.chr}G 8\r".encode())

    def setSTANT(self):
        self.device.write(f"{self.chr}DCFRT S 10\r".encode())

    def getTempSetting(self):
        self.device.write(f"{self.chr}DCFRT S 10 20\r".encode())
        return self.read()
    def getFirmWareVersion(self):
        self.device.write(f"{self.chr}VE\r".encode())
        return self.read()

    def getTestReading(self):
        time.sleep(0.5)
        self.device.write(f"{self.chr}\r".encode())
        return self.read(100)

def all_ports(keyword = "CP210x"):
    # Get a list of available serial ports
    ports = grep(keyword)  # Empty string to match all ports

    # List to hold dictionaries of port details
    port_list = []

    for port in ports:
        # Create a dictionary for each port's details
        port_info = {
            "Device": port.device,
            "Name": port.name,
            "Description": port.description,
            "HWID": port.hwid,
            "VID": port.vid,
            "PID": port.pid,
            "Serial Number": port.serial_number,
            "Location": port.location,
            "Manufacturer": port.manufacturer,
            "Product": port.product,
            "Interface": port.interface
        }

        # Append the dictionary to the list
        port_list.append(port_info)

        # Optionally, print the details
        print(f"Device: {port.device}")
        print(f"Name: {port.name}")
        print(f"Description: {port.description}")
        print(f"HWID: {port.hwid}")
        print(f"VID: {port.vid}")
        print(f"PID: {port.pid}")
        print(f"Serial Number: {port.serial_number}")
        print(f"Location: {port.location}")
        print(f"Manufacturer: {port.manufacturer}")
        print(f"Product: {port.product}")
        print(f"Interface: {port.interface}")
        print("-" * 40)
    return port_list

def getALLALICAT():
    allPorts = all_ports()
    count = 0
    devices = []
    for i in range(len(allPorts)):
        for j in range(ord("A"), ord("Z") + 1):
            time.sleep(0.1)
            device = Instrument(allPorts[i]["Device"], chr(j))
            if device.isAlicat():
                devices.append((allPorts[i]["Device"], device, chr(j)))
                device.close()
            else:
                del device
    print(devices)
    return devices

if __name__ == "__main__":
    # devices = getALLALICAT()

    #testing unit change
    theTestingDevice = Instrument("COM18", "Z")



    # print(theTestingDevice.getFirmWareVersion())
    #
    # for i in range(20):
    #     print(theTestingDevice.getTestReading())
    # theTestingDevice.setGasN2()
    # theTestingDevice.factoryReset()
    # theTestingDevice.setSTANT()
    # theTestingDevice.AFactoryResetROUTINE()
    # theTestingDevice.close()
    # getALLALICAT()

    # testing factory rest
    # theTestingDevice = Instrument("COM18", "H")
    # theTestingDevice.factoryReset()
    # theTestingDevice.close()
    # getALLALICAT()


# device = Instrument("COM18", "Y")
# device.device.write("Y??m*\r".encode())
# a = device.device.read(28)
# print(a)