from Alicat import *

def APP():
    userOption = getUserOption()
    isConnected = False
    while userOption != 10:
        if userOption == 1:
            print("Searching ports whose keyword is {CP210x}")
            all_ports()
        elif userOption == 2:
            print("Finding all Alicat Devices from all ports named {CP210x} with all alphabet [A-z]...")
            getALLALICAT()
        elif userOption == 3:
            port, ID, device, version = getInstrument()
            isConnected = True
            print(f"Your firmware version is {version}")
        elif userOption == 4:
            print(f"port: {port} ID: {ID} Version: {version} Device: {device}")
            print("Testing Reading starts...")
            for i in range(20):
                print(device.getTestReading())
        elif userOption == 5:
            toChar = getCharInput()
            device.changeUnitID(toChar)
            ID = toChar
            print(f"ID changed to {toChar}")
        elif userOption == 6:
            print(f"Critical: Factory mode reset with device: {device} with ID {ID}")
            print("Enter YES to continue")
            if input() == "YES":
                device.factoryReset()
            else:
                print("Factory reset aborted")
        elif userOption == 7:
            print("set gas option to N2 instead of default ch4 or any other gases")
            for i in range(10):
                time.sleep(0.5)
                device.setGasN2()
            print("Due to unoptimized ascynchronious lock algorithm setGasN2 may not be applied. Try again if that happens.")

        userOption = getUserOption() #at the end of cycle asks user options
    print("The End of Program")




def printOption():
    print("-"*20)
    print("Option 1: Find All Available Ports with list info")
    print("Option 2: Find All ALICAT Devices from all Ports named {CP210x}. All ports must be closed, or only run at the start")
    print("Option 3: Connect to a device specified by Port: {i.e. COM18} and Unit ID: {i.e. Z}")
    print("Option 4: TestReading. Only Valid when a device is connected")
    print("Option 5: Change Current Device to another Unit ID: Caution: It might break communication and may require manual device setting")
    print("Option 6: Factory Reset: Caution: It might break communication and may require manual device setting")
    print("Option 7: Change Gas to N2 instead of CH4 or other gases")

    print("Option 10: Quit")
    print("-"*20)

def getUserOption(mode="int"):
    def checkUserOption(argin):
        if 1 <= argin <= 10:
            return True
        else:
            return False

    while True:
        try:
            printOption()
            userOption = int(input().strip())
            if checkUserOption(userOption):
                return userOption
        except ValueError:
            print("Enter a valid integer in range of [1-10]")

def getInstrument():
    while True:
        try:
            print("Type your port: ")
            port = str(input().strip())
            print("Type your Device ID: ")
            ID = str(input().strip())
            device = Instrument(port, ID)
            if device.isAlicat():
                return port, ID, device, device.getFirmWareVersion()
            print()
            print()
            print()
            print(f"Invalid port: {port} and ID: {ID}.")
            print("Please check the port and ID. Your device does not response with M00 ALICAT SCIENTIFIC")
        except ValueError:
            print("Your inputs are invalid type. Please enter string for both port and ID")

def getCharInput():
    while True:
        try:
            print("Desired output UNIT id [A-Z]. Caution: Duplicate Unit ID requries manual device setting")
            userOption = input().strip().upper()
            if (len(userOption) == 1) and ("A" <= userOption <= "Z"):
                return userOption
            print("Input type check failed: ")
            print("Length of char != 1 or letter is not inside [A-Z].")

        except ValueError:
            print("Your inputs are invalid type. Please enter string for desire output Device Unit ID")

if __name__ == "__main__":
    APP()





