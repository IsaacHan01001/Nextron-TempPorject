from tkinter import *
import tkinter.ttk as ttk
from GUI_Utility.Utilities import *

global Color
Color = dict(White="#f0f0f0", Black="#1e1e1e", test="red")


class Display(Toplevel):
    def __init__(self, parent):
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
        # Create a LabelFrame for the personal details section
        temperatureController = ttk.LabelFrame(self.main_frame, text="Temperature Controller", padding="10")
        temperatureController.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # Add widgets to the personal_frame
        ttk.Label(temperatureController, text="Current Temperature:").grid(row=0, column=0, sticky="w")
        self.current_temp = StringVar()
        self.current_temp.set("00.00")
        ttk.Label(temperatureController, textvariable= self.current_temp).grid(row=0, column=1, sticky="w")

        ttk.Label(temperatureController, text="Current Set Temperature:").grid(row=0, column=2, sticky="w")
        self.current_setValue = StringVar()
        self.current_setValue.set("00.00")
        ttk.Label(temperatureController, textvariable=self.current_setValue).grid(row=0, column=3, sticky="w")

        ttk.Label(temperatureController, text="Current Ramping Rate").grid(row=1, column=0, sticky="w")
        self.current_ramping_rate = StringVar()
        self.current_setValue.set("00.00")
        ttk.Label(temperatureController, textvariable=self.current_setValue).grid(row=1, column=1, sticky="w")

        ttk.Label(temperatureController, text="Set Desired Ramping Rate").grid(row=1, column=2, sticky="w")
        ttk.Entry(temperatureController).grid(row=1, column=3, sticky="w")

        # ttk.Label(temperatureController, text="Set Desired Temperature:").grid(row=1, column=2, sticky="w")
        # self.desired_temp = StringVar()
        # self.desired_temp.set("00.00")
        # ttk.Label(temperatureController, textvariable= self.desired_temp).grid(row=1, column=3, sticky="w")

        # Create a LabelFrame for the address section
        address_frame = ttk.LabelFrame(self.main_frame, text="Another Field or entry... example", padding="10")
        address_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        # Add widgets to the address_frame
        ttk.Label(address_frame, text="Street:").grid(row=0, column=0, sticky="w")
        ttk.Entry(address_frame).grid(row=0, column=1, sticky="ew")

        ttk.Label(address_frame, text="City:").grid(row=1, column=0, sticky="w")
        ttk.Entry(address_frame).grid(row=1, column=1, sticky="ew")

        ttk.Label(address_frame, text="State:").grid(row=2, column=0, sticky="w")
        ttk.Entry(address_frame).grid(row=2, column=1, sticky="ew")

    def on_close(self):
        self.destroy()
        self.master.displayWindow = None






