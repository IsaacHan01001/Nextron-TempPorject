from tkinter import *
import tkinter.ttk as ttk
from GUI_Utility.Utilities import *

global Color
Color = dict(White="#f0f0f0", Black="#1e1e1e", test="red")


class Display(Toplevel):
    def __init__(self, parent):
        self.root = getRoot(parent)
        super().__init__(parent)
        self.geometry("800x600")
        self.iconphoto(False, makeIconPhoto())
        self.option_add("*tearOff", FALSE)
        self.resizable(False, False) #if I fail managing geometry, I will block resizing
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.rowconfigure(0, weight=9999)
        self.columnconfigure(0, weight=9999)

        # Create the main container frame
        self.main_frame = ttk.Frame(self, padding="10")
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        self.tempUnit = "\u0080C"

        self.tempFields = {"CurrTemp": StringVar(value="00.01"+self.tempUnit), "SetTemp": StringVar(value="00.02"),
                           "RampingRate": StringVar(value="00.03"), "HotPower":StringVar(value="00.04"),
                           "CoolPower": StringVar(value="00.05")}



        # Create a LabelFrame for the temperature controller section
        temperatureController = ttk.LabelFrame(self.main_frame, text="Temperature Controller", padding="10")
        temperatureController.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # Add widgets to the temperatureController with padding between fields
        ttk.Label(temperatureController, text="Current Temperature:").grid(row=0, column=0, sticky="w", padx=5)
        ttk.Label(temperatureController, textvariable=self.tempFields["CurrTemp"]).grid(row=0, column=1, sticky="w", padx=5)

        ttk.Label(temperatureController, text="Set Temperature:").grid(row=0, column=2, sticky="w", padx=10)
        ttk.Label(temperatureController, textvariable=self.tempFields["SetTemp"]).grid(row=0, column=3, sticky="w", padx=5)

        ttk.Label(temperatureController, text="Ramping Rate").grid(row=0, column=4, sticky="w", padx=10)
        ttk.Label(temperatureController, textvariable=self.tempFields["RampingRate"]).grid(row=0, column=5, sticky="w", padx=5)

        ttk.Label(temperatureController, text="Hot Power").grid(row=0, column=6, sticky="w", padx=10)
        ttk.Label(temperatureController, textvariable=self.tempFields["HotPower"]).grid(row=0, column=7, sticky="w", padx=5)

        ttk.Label(temperatureController, text="Cool Power").grid(row=0, column=8, sticky="w", padx=5)
        ttk.Label(temperatureController, textvariable=self.tempFields["CoolPower"]).grid(row=0, column=9, sticky="w", padx=5)

        # Create a LabelFrame for another field section (address example)
        running = ttk.LabelFrame(self.main_frame, text="Running the temperature program", padding="10")
        running.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        # Add widgets to the address_frame with padding between fields
        ttk.Label(running, text="Desired Temp").grid(row=0, column=0, sticky="w", padx=5)
        ttk.Entry(running).grid(row=0, column=1, sticky="ew", padx=5)


        ttk.Label(running, text="Desired Ramping Rate").grid(row=1, column=0, sticky="w", padx=5)
        ttk.Entry(running).grid(row=1, column=1, sticky="ew", padx=5)


        ttk.Button(running, text="Click to start", command=print(1234)).grid(row=1, column=2, sticky="ew", padx=5)
        self.updateTempFields()

    def on_close(self):
        self.destroy()
        self.master.displayWindow = None

    def updateTempFields(self):
        aTempDevice = self.root.devices["Temp"]
        if len(aTempDevice) == 0:
            print("no device connected")
        elif len(aTempDevice) == 1:
            aTempDevice[0].updateFieldsInfo()
            theDevice = aTempDevice[0].temperature
            print(theDevice)
            self.tempFields["CurrTemp"].set(value=f"{theDevice["Temperature"]["CurrentTemp"]:.2f}" + self.tempUnit)
            self.tempFields["SetTemp"].set(value=f"{theDevice["Temperature"]["SetTemp"]:.2f}" + self.tempUnit)
            self.tempFields["RampingRate"].set(value=f"{theDevice["Temperature"]["RampingTemp"]:.2f}" + self.tempUnit + "/" + "s")
            self.tempFields["HotPower"].set(value=f"{theDevice["Temperature"]["HotPower"]:.2f}" + self.tempUnit)
            self.tempFields["CoolPower"].set(value=f"{theDevice["Temperature"]["CoolPower"]:.2f}" + self.tempUnit)
        else:
            print("more than 2 devices connected")

        self.root.after(1000, self.updateTempFields)

    def runTheHeater(self):



