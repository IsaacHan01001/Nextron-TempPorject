from tkinter import *
import tkinter.ttk as ttk
from GUI_Utility.Utilities import *

class DeviceTopLevel(Toplevel):
    def __init__(self, size):
        #Color and Size constant that we use for main widget
        global Color
        Color = dict(White="#f0f0f0", Black="#1e1e1e", test="red")

        #main setup
        super().__init__()
        self.title = "This is generic class. Call instance of Toplevel."
        self.geometry("800x600")
        # self.iconphoto(False, makeIconPhoto())
        self.option_add("*tearOff", FALSE)
        self.resizable(False, False) #if I fail managing geometry, I will block resizing

        # widgets
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=5)
        self.menu = Menu(self)
        self.main = Main(self)
