from tkinter import *
import tkinter.ttk as ttk
from Devices.Temp.TempUtility.Utils import *
from GUI_Utility.Utilities import *
from Devices.Temp.FB100 import FB100

global Color
Color = dict(White="#f0f0f0", Black="#1e1e1e", test="red")

# class DeviceTopLevel(Toplevel):
#     def __init__(self):
#         self.title = "This is generic class. Call instance of Toplevel."
#         self.geometry("800x600")
#         # self.iconphoto(False, makeIconPhoto())
#         self.option_add("*tearOff", FALSE)
#         self.resizable(False, False) #if I fail managing geometry, I will block resizing
#         self.iconphoto(False, makeIconPhoto())
#         # widgets
#         self.rowconfigure((0, 1, 2, 3), weight=0, uniform="a")

class TempConnection(Toplevel):
    def __init__(self, parent):
        self.parent = parent
        #common across device widgets
        super().__init__(parent)
        self.root = getRoot(self)
        self.geometry("800x600")
        self.iconphoto(False, makeIconPhoto())
        self.option_add("*tearOff", FALSE)
        self.resizable(False, False) #if I fail managing geometry, I will block resizing
        self.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12), weight=1, uniform='a')
        self.columnconfigure((0, 2, 3, 4, 5, 6), weight = 1, uniform="a")
        self.columnconfigure(1, weight=3)
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        ttk.Button(self, text="Connect", command= self.connect_temp).grid(row=0, column=5, sticky="we")
        ttk.Button(self, text="DisConnect", command= self.disconnect_temp).grid(row=0, column=6, sticky="we")

        s = ttk.Style()
        s.configure("Device.TLabel", font=("Helvetica", 12), foreground=Color["Black"])
        ttk.Label(self, text="Connection", anchor="w", style="Device.TLabel").grid(row=0, column=0, sticky="nw")
        ttk.Label(self, text="Model", anchor="w", style="Device.TLabel").grid(row=1, column=0, sticky="nw")
        ttk.Label(self, text="Unit", anchor="w", style="Device.TLabel").grid(row=2, column=0, sticky="nw")
        ttk.Label(self, text="Device Info", anchor="w", style="Device.TLabel").grid(row=3, column=0, sticky="nw")

        self.tempModelVariable = StringVar()
        self.tempModel = ttk.Combobox(self, textvariable=self.tempModelVariable)
        self.tempModel.grid(row=1, column=6, sticky="ew")
        self.tempModel["values"] = ("CHU", "CHH", "CHL", "PT", "MPS", "LN")
        # self.tempModel.bind("<<ComboboxSelected>>", function)
        self.tempModel.state(["readonly"])

        self.tempUnit = StringVar()
        self.tempUnit = ttk.Combobox(self, textvariable=self.tempUnit)
        self.tempUnit.grid(row=2, column=6, sticky="ew")
        self.tempUnit["values"] = (f"\u00B0C", "K")
        # self.tempModel.bind("<<ComboboxSelected>>", function)
        self.tempUnit.state(["readonly"])

###########################
        self.text_widget = Text(self, wrap="word", font=("Helvetica", 12), state="normal")
        self.text_widget.grid(row=3, column=2, rowspan=3, columnspan=3, sticky="nsew")

        # Create a vertical scrollbar
        self.scrollbar = ttk.Scrollbar(self, command=self.text_widget.yview)
        self.scrollbar.grid(row=3, column=6, sticky="ns")

        # Configure the Text widget to use the scrollbar
        self.text_widget.config(yscrollcommand=self.scrollbar.set)

        # Add a lot of text to the widget (simulating large information)
        large_text = '''
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
        '''
        self.text_widget.insert("1.0", large_text)

        #different for each widgets
        self.title("Temperature Controller Setting")

    def on_close(self):
        self.destroy()
        self.master.temp_connection_window = None
        self.disconnect_temp()

    def connect_temp(self):
        s = ttk.Style()
        s.configure("on.TLabel", font=("Helvetica", 18), foreground=Color["White"],
                    background="blue")
        s.configure("off.TLabel", font=("Helvetica", 18), foreground=Color["White"],
                    background=Color["Black"])

        allPorts, _ = all_ports()
        if len(self.root.devices["Temp"]) > 0:
            print("a device is already connected")
            return

        for port in allPorts:
            device = FB100(port, 1) #channel is assumed to be 1
            if device.connected:
                self.root.devices["Temp"].append(device)
                self.parent.DeviceFrame[3][0].set("On")
                self.parent.DeviceFrame[2][0].config(style="on.TLabel")

                self.root.lift()
                self.root.focus()
                return

    def disconnect_temp(self):
        if self.root.devices["Temp"]:
            self.root.devices["Temp"][0].disconnect()
        self.root.devices["Temp"] = []
        self.parent.DeviceFrame[3][0].set("Off")
        self.parent.DeviceFrame[2][0].config(style="off.TLabel")



