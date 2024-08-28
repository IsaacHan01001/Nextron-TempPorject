from pymodbus.client.sync import ModbusSerialClient as ModbusClient

# Create a Modbus client
client = ModbusClient(
    method='rtu',
    port='COM4',  # Update with your serial port
    baudrate=9600,
    parity='N',
    stopbits=1,
    bytesize=8
)

# Connect to the client
client.connect()

# Read a register (example register address 0x0001)
response = client.read_holding_registers(address=0x0001, count=1, unit=1)

# Check for a successful response
if not response.isError():
    print(f'Register Value: {response.registers[0]}')
else:
    print('Error:', response)

# Close the connection
client.close()
