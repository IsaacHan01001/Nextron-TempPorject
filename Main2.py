import sys
from tkinter import  *
import tkinter.ttk as ttk
from PIL import Image, ImageTk
import os
from tkinter import messagebox

from Temp.FB100 import FB100
from Temp.TempUtility.Utils import *

class MainWindow(Frame, controller):
    def __init__(self, parent):
        self.Color_Black = "#1e1e1e" #black
        self.Color_White = "#f0f0f0" #white
        self.Color_test = "red"
        super().__init__(parent)
        self.parent = parent
        self.grid(row=0, column=0, sticky="nsew")

        # Top frame with a black background
        self.topFrame = tk.Frame(self, bg=self.Color_Black, width= 1366, height=100)
        self.topFrame.grid(row=0, column=0, sticky="nsew")
        self.topFrame.grid_propagate(False)
        self.topFrame.rowconfigure(0, weight=1)  # Make row 0 expandable
        self.topFrame.rowconfigure(1, weight=0)  # Keep row 1 fixed

        # Bottom frame with a light gray background
        self.bottomFrame = tk.Frame(self, bg=self.Color_White, width=1366, height=100)
        self.bottomFrame.grid(row=1, column=0, sticky="nsew")
        self.bottomFrame.grid_propagate(False)

        #constructing Top and Bottom Frame
        self.constructTopFrame()
        # self.constructBottomFrame()

    def constructTopFrame(self):
        '''
        Constructs Upper Layer with transparent logo image, button widget,
        :return: None
        '''
        try:
            logo_path = os.path.join(os.path.dirname(__file__), "Images_logo/logo.png")
            self.topFrame.Logo = ImageTk.PhotoImage(Image.open(logo_path).resize((180, 50), Image.Resampling.LANCZOS))
            aCanvas = tk.Canvas(self.topFrame, bg=self.Color_Black, width=200, height=55, highlightthickness=0)
            aCanvas.grid(row=0, sticky="nw")
            aCanvas.create_image(100, 30, image=self.topFrame.Logo)
        except tk.TclError as err:
            tk.messagebox.showwarning(f'After 8 seconds this window expires: \nEncountered error with finding the file \n the error message is given as: {err}')
            self.quit()
        except Exception as err:
            tk.messagebox.showwarning("Unaccounted error {}".format(err))
            self.quit()

        self.topFrame.frameButtons = tk.Frame(self.topFrame, width= 450, height=28, bg=self.Color_Black)
        self.topFrame.frameButtons.grid(row=0, sticky=tk.SW)
        self.topFrame.frameButtons.propagate(False)

        self.topFrame.frameButtons.Buttons = []
        buttons = [
            ("Home", lambda: print("Home clicked")),
            ("Display", lambda: print("Display clicked")),
            ("Recipe", lambda: print("Recipe clicked")),
            ("Manual", lambda: print("Manual clicked")),
            ("I-V", lambda: print("I-V clicked")),
            ("Setting", lambda: print("Setting clicked"))
        ]

        for i, (text, command) in enumerate(buttons):
            self.topFrame.frameButtons.Buttons.append(tk.Button(self.topFrame.frameButtons, width=8, text=text, command=command,
                               bg=self.Color_Black, fg=self.Color_White, font=("Helvetica", 12), highlightthickness=0, bd=0))
        for i in range(len(self.topFrame.frameButtons.Buttons)):
            self.topFrame.frameButtons.Buttons[i].grid(row=0, column=i, sticky="ew")

    def constructBottomFrame(self):
        self.bottomFrame.Label_ChooseDevices = tk.Label(self.bottomFrame, text="Select Controller or Instrument", font=("Helvetica", 17), bg=self.Color_test, fg=self.Color_Black)
        self.bottomFrame.Label_ChooseDevices.grid(row=)
    def quit(self, event=None):
        self.parent.destroy()

if __name__ == "__main__":
    application = tk.Tk()
    application.title("Nextron Program")
    application.geometry("1367x770")
    # application.resizable(False, False)

    # Define the path for the icon
gf
    if sys.platform.startswith("win"):
        icon = path + "RootLogo.png"
    else:
        tk.messagebox.showwarning(
            f"This program is intended for Windows users. Your platform is detected to be {sys.platform}. \nThe program will terminate after 5 seconds.")
        application.quit()

    # Set the window icon
    application.iconphoto(False, ImageTk.PhotoImage(Image.open(icon)))

    # Initialize the main window
    window = MainWindow(application)

    # Handle window close event
    application.protocol("WM_DELETE_WINDOW", window.quit)

    # Start the Tkinter event loop
    application.mainloop()
