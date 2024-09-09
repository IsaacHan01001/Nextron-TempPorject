import sys
from tkinter import *
from tkinter import messagebox
import tkinter.ttk as ttk
from PIL import Image, ImageTk
import os

class APP(Tk):
    def __init__(self, title, size):
        global Color
        global SIZE
        SIZE = size
        Color = dict(White="#f0f0f0", Black="#1e1e1e", test="red")
        # main setup
        super().__init__()
        self.checkWindow()
        self.title(title)
        self.geometry(f"{size[0]}x{size[1]}")
        self.iconphoto(False, self.makeIconPhoto())
        self.option_add("*tearOff", FALSE)
        # self.protocol("WM_DELETE_WINDOW", self.quit) # turned off during development
        self.resizable(False, False) # if I fail managing geometry, I will block resizing

        # widgets
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=5)
        self.menu = Menu(self)
        self.main = Main(self)

        # run
        self.mainloop()

    def makeIconPhoto(self):
        path = os.path.join(os.path.dirname(__file__), "Images_logo/RootLogo.png")
        image = ImageTk.PhotoImage(Image.open(path).resize((180, 50), Image.Resampling.LANCZOS))
        return image

    def checkWindow(self):
        if sys.platform.startswith("win"):
            return
        else:
            messagebox.showwarning(f"This is for Window Users: You are {sys.platform}.")
            self.destroy()

    def quit(self):
        if messagebox.askokcancel("Quit", "Do you really want to quit?"):
            self.destroy()

class Menu(ttk.Frame):
    def __init__(self, parent):
        s = ttk.Style()
        s.configure("TFrame", background= Color["Black"], width=SIZE[0] , height=300)
        super().__init__(parent, style="TFrame")
        self.parent = parent
        self.grid(row=0, column=0, sticky="nsew")

        self.label = ttk.Label(self, background= Color["Black"], anchor="nw")
        self.image = self.makeImage()
        self.label['image'] = self.image
        self.label.grid(row=0, column=0, rowspan=3, columnspan=2, pady=(10, 20))
        self.buttons = self.makeButtons()
        self.columnconfigure((0, 1, 2, 3, 4, 5), uniform="b")
        self.rowconfigure(1, uniform="b")

    def makeImage(self):
        logo_path = os.path.join(os.path.dirname(__file__), "Images_logo/logo.png")
        image = ImageTk.PhotoImage(Image.open(logo_path).resize((180, 50), Image.Resampling.LANCZOS))
        return image

    def makeButtons(self):
        s = ttk.Style()
        s.configure("Menu.TButton", font=("Helvetica", 12), foreground=Color["Black"])
        ans = []
        buttons = [
            ("Home", lambda: print("Home clicked")),
            ("Display", lambda: print("Display clicked")),
            ("Recipe", lambda: print("Recipe clicked")),
            ("Manual", lambda: print("Manual clicked")),
            ("I-V", lambda: print("I-V clicked")),
            ("Setting", lambda: print("Setting clicked"))
        ]

        for i, (text, command) in enumerate(buttons):
            ans.append(ttk.Button(self, text=text, command=command, style="Menu.TButton"))
        for i in range(len(ans)):
            ans[i].grid(row=3, column=i, sticky="sew", padx=0, pady=(0, 2))
        return ans

class Main(ttk.Frame):
    def __init__(self, parent):
        s = ttk.Style()
        s.configure("Main.TFrame", background= Color["White"], width=SIZE[0])
        super().__init__(parent, style="Main.TFrame")
        self.parent = parent
        self.grid(row=1, column=0, sticky="nsew")

        s.configure("Menu.TLabel", font=("Helvetica", 12, "bold"), foreground=Color["Black"])
        self.label = ttk.Label(self, background= Color["White"], anchor="nw", style="Menu.TLabel", text= "Select Controller or Instrument")
        self.label.grid(row=0, column=0, padx=5, pady=20)

        # DeviceFrame is a nested list where it contains :
        #   Device_Label : i.e. temperature
        #   Device_Image : i.e. mfc-image
        #   Device_Status_Label
        #   Device_Status_String : i.e. On or off
        self.DeviceFrame = self.makeDevices()
        self.gridDevices()
        self.columnconfigure((0, 1, 2, 3, 4, 5), uniform="a")

    def makeDevices(self):
        s = ttk.Style()
        s.configure("Main.TButton", font=("Helvetica", 12), foreground=Color["Black"])
        s.configure("Main_Device_Title.TLabel", font=("Helvetica", 12), foreground=Color["Black"])
        s.configure("Main_Device_Image.TLabel", font=("Helvetica", 12), foreground=Color["Black"])

        # Label Name, Image, Click function
        Devices = [
            ("Temperature", ImageTk.PhotoImage(Image.open(r".\Images_svg\Temperature.png")), lambda: print("Temperature")),
            ("Mass Flow", ImageTk.PhotoImage(Image.open(r".\Images_svg\Mass Flow.png")), lambda: print("Mass Flow")),
            ("Humidity", ImageTk.PhotoImage(Image.open(r".\Images_svg\Humidity.png")), lambda: print("Humidity")),
            ("Pressure", ImageTk.PhotoImage(Image.open(r".\Images_svg\Pressure.png")), lambda: print("Pressure")),
            ("Measure", ImageTk.PhotoImage(Image.open(r".\Images_svg\Measure.png")), lambda: print("Measure")),
            ("Sample Feeder", ImageTk.PhotoImage(Image.open(r".\Images_svg\SampleFeeder.png")), lambda: print("Sample Feeder")),
        ]

        labels = []
        deviceImages = []
        onOffLabel = []
        onOffStatus = [StringVar() for x in range(len(Devices))]

        # Store image references to prevent garbage collection
        self.device_images = [img for _, img, _ in Devices]

        for i, (labelText, labelImage, command) in enumerate(Devices):
            labels.append(ttk.Label(self, text=labelText, style="Main_Device_Title.TLabel"))
            deviceImages.append(ttk.Label(self, image=labelImage, style="Main_Device_Image.TLabel"))
            onOffLabel.append(ttk.Label(self, textvariable=onOffStatus[i], style="Inverse.TLabel"))
        return labels, deviceImages, onOffLabel, onOffStatus

    def gridDevices(self):
        for i in range(len(self.DeviceFrame[0])):
            self.DeviceFrame[0][i].grid(row=1, column=i, pady=15, sticky="nw")
            self.DeviceFrame[1][i].grid(row=2, column=i)
            if len(self.DeviceFrame) > 2:
                self.DeviceFrame[2][i].grid(row=3, column=i, sticky="sw")

if __name__ == "__main__":
    APP("Nextron Program", (1367, 770))
