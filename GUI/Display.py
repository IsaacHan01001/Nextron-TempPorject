from tkinter import *
import tkinter.ttk as ttk
from GUI_Utility.Utilities import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import pandas as pd
from datetime import datetime

global Color
Color = dict(White="#f0f0f0", Black="#1e1e1e", test="red")

class Display(Toplevel):
    def __init__(self, parent):
        self.root = getRoot(parent)
        self.data = pd.DataFrame(columns=["Timestamp", "CurrentTemp", "SetTemp", "RampingRate", "HotPower", "CoolPower"])
        self.data.set_index('Timestamp', inplace=True)

        super().__init__(parent)
        self.geometry("800x700")
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
        self.timeUnit = "Default"
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
        self.entry1 = ttk.Entry(running)
        self.entry1.grid(row=0, column=1, sticky="ew", padx=5)

        ttk.Label(running, text="Desired Ramping Rate").grid(row=1, column=0, sticky="w", padx=5)
        self.entry2 = ttk.Entry(running)
        self.entry2.grid(row=1, column=1, sticky="ew", padx=5)

        ttk.Button(running, text="Click to start", command=self.runHeater).grid(row=1, column=2, sticky="ew", padx=5)
        Graph = ttk.LabelFrame(self.main_frame, text="MatPlotLib Graph", padding="10")
        Graph.grid(row=2, column=0, rowspan=4, columnspan=4)

        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=Graph)
        self.canvas.get_tk_widget().grid(row=0, column=0)

        self.updateTempFields()

    def on_close(self):
        if self.Regularupdate:
            self.after_cancel(self.Regularupdate)

        for i in range(len(self.root.devices["Temp"])):
            self.root.devices["Temp"][i].setRunOrStop(1)
        self.destroy()
        self.master.displayWindow = None

    def updateTempFields(self):
        aTempDevice = self.root.devices["Temp"]
        if len(aTempDevice) == 0:
            print("no device connected")
        elif len(aTempDevice) == 1:
            aTempDevice[0].updateFieldsInfo()
            theDevice = aTempDevice[0].temperature
            timestamp = pd.to_datetime(datetime.now())
            current_temp = theDevice["Temperature"]["CurrentTemp"]
            set_temp = theDevice["Temperature"]["SetTemp"]
            ramping_rate = theDevice["Temperature"]["RampingTemp"]
            hot_power = theDevice["Temperature"]["HotPower"]
            cool_power = theDevice["Temperature"]["CoolPower"]

            self.data = pd.concat([self.data, pd.DataFrame([{
                "Timestamp": timestamp,
                "CurrentTemp": current_temp,
                "SetTemp": set_temp,
                "RampingRate": ramping_rate,
                "HotPower": hot_power,
                "CoolPower": cool_power
            }])], ignore_index=True)

            self.timeUnit = aTempDevice[0].getSettingChangeRateLimiterUnitTime()
            print("Ramping Rate Time Unit: ", self.timeUnit)

            self.tempFields["CurrTemp"].set(value=f"{current_temp:.2f}" + self.tempUnit)
            self.tempFields["SetTemp"].set(value=f"{set_temp:.2f}" + self.tempUnit)
            self.tempFields["RampingRate"].set(value=f"{ramping_rate:.2f}" + self.tempUnit + "/" + "s")
            self.tempFields["HotPower"].set(value=f"{hot_power:.2f}" + self.tempUnit)
            self.tempFields["CoolPower"].set(value=f"{cool_power:.2f}" + self.tempUnit)
            self.plot()
        else:
            print("more than 2 devices connected")

        self.Regularupdate = self.root.after(1500, self.updateTempFields)

    def plot(self):
        self.ax.clear()
        self.data.plot(x="Timestamp", y="CurrentTemp", ax=self.ax)
        self.canvas.draw()

    def runHeater(self):
        if len(self.root.devices["Temp"]) > 0:
            theDevice = self.root.devices["Temp"][0]
        else:
            theDevice = None

        if theDevice:
            try:
                theDevice.setSetValue(float(self.entry1.get()))
                theDevice.setSingleRampingRate(float(self.entry2.get()))
            except ValueError:
                print("Input floats for the value")
                return

            if theDevice.getRunOrStop() == 1:
                theDevice.setRunOrStop(0)