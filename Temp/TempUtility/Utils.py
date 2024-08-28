from serial.tools.list_ports import grep
import serial

def all_ports():
    # Get a list of available serial ports
    ports = grep("RS485")  # Empty string to match all ports

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

def find(aPort):
    '''
    requires channel to be set up in the class. Moved assigning channel to class init for code maintenance.
    :param aPort:
    :return:
    '''
    try:
        aPort["Channel"]
    except KeyError:
        print("the port does not have field 'Channel'")
        return
    try:
        device = serial.Serial(aPort["Device"], timeout=0.2)
        device.write(f'\x04{aPort["Channel"]:0>2}ID\x05\x04'.encode())
        comm_out = device.read(100)
        print(comm_out)
        if b"IDFB100" in comm_out:
            return device
    except:
        import traceback
        traceback.print_exc()
    print("No Device Detected")
    return None

def bcc_check(data):
    '''
    FB100 uses Block Check Character to detect error by using horizontal parity. Manual p# 23
    the STX at the beginning of the communication is not used.
    :return: bcc_result
    tested using bcc("M100100.0\03") == 80
    '''
    bcc = 0x00
    for byte in data:
        bcc ^= byte
    return chr(byte)

def crc16_ccitt_false(data: bytes, poly=0xA001, init_crc=0xFFFF):
    """
    Calculate CRC16-CCITT-FALSE checksum for the given data.

    :param data: Input data as bytes.
    :param poly: Polynomial for CRC calculation (default is 0xA001 for CRC-16-CCITT-FALSE).
    :param init_crc: Initial CRC value (default is 0xFFFF).
    :return: Computed CRC16 checksum.
    """
    crc = init_crc
    for byte in data:
        crc ^= byte
        for _ in range(8):  # Process each bit of the byte
            if crc & 0x01:  # Check if the low bit is set
                crc = (crc >> 1) ^ poly  # Shift and XOR with polynomial
            else:
                crc >>= 1  # Just shift
            crc &= 0xFFFF  # Keep CRC as 16-bit value
    return crc

# def crcCheck():
if __name__ == "__main__":
    number = b'\x01\x03\x00\x00\x00\x01'
    result = crc16_ccitt_false(number)
    quo, rem = result//256, result % 256
    print("{0:#x} {1:#x}".format(quo, rem))