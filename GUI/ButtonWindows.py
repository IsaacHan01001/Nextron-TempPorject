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

        # Create a LabelFrame for the temperature controller section
        temperatureController = ttk.LabelFrame(self.main_frame, text="Temperature Controller", padding="10")
        temperatureController.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # Add widgets to the temperatureController with padding between fields
        ttk.Label(temperatureController, text="Current Temperature:").grid(row=0, column=0, sticky="w", padx=5)
        self.current_temp = StringVar(value="00.00")
        ttk.Label(temperatureController, textvariable=self.current_temp).grid(row=0, column=1, sticky="w", padx=5)

        ttk.Label(temperatureController, text="Set Temperature:").grid(row=0, column=2, sticky="w", padx=10)
        self.current_setValue = StringVar(value="00.00")
        ttk.Label(temperatureController, textvariable=self.current_setValue).grid(row=0, column=3, sticky="w", padx=5)

        ttk.Label(temperatureController, text="Ramping Rate").grid(row=0, column=4, sticky="w", padx=10)
        self.current_ramping_rate = StringVar(value="00.00")
        ttk.Label(temperatureController, textvariable=self.current_ramping_rate).grid(row=0, column=5, sticky="w", padx=5)

        ttk.Label(temperatureController, text="Hot Power").grid(row=0, column=6, sticky="w", padx=10)
        self.current_hot_power = StringVar(value="00.00")
        ttk.Label(temperatureController, textvariable=self.current_hot_power).grid(row=0, column=7, sticky="w", padx=5)

        ttk.Label(temperatureController, text="Cool Power").grid(row=0, column=8, sticky="w", padx=5)
        self.current_cool_power = StringVar(value="00.00")
        ttk.Label(temperatureController, textvariable=self.current_cool_power).grid(row=0, column=9, sticky="w", padx=5)

        # Create a LabelFrame for another field section (address example)
        address_frame = ttk.LabelFrame(self.main_frame, text="Another Field or Entry... example", padding="10")
        address_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        # Add widgets to the address_frame with padding between fields
        ttk.Label(address_frame, text="Street:").grid(row=0, column=0, sticky="w", padx=5)
        ttk.Entry(address_frame).grid(row=0, column=1, sticky="ew", padx=5)

        ttk.Label(address_frame, text="City:").grid(row=1, column=0, sticky="w", padx=5)
        ttk.Entry(address_frame).grid(row=1, column=1, sticky="ew", padx=5)

        ttk.Label(address_frame, text="State:").grid(row=2, column=0, sticky="w", padx=5)
        ttk.Entry(address_frame).grid(row=2, column=1, sticky="ew", padx=5)

    def on_close(self):
        self.destroy()
        self.master.displayWindow = None
