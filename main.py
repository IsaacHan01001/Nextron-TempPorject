import sys
import tkinter as tk
from PIL import Image, ImageTk
import os



root = tk.Tk()
root.title("Nextron Program")
root.iconphoto(False, ImageTk.PhotoImage(Image.open(r'./Images_logo/RootLogo.png')))
root.geometry("1367x770")

# Top Frame
topFrame = tk.Frame(root, width=1366, height=100, bg="#1e1e1e")
topFrame.pack(side=tk.TOP, fill=tk.BOTH)
topFrame.pack_propagate(False)

image_path = r".\Images_logo\logo.png"
image = Image.open(image_path).resize((180, 50), Image.Resampling.LANCZOS)
photo = ImageTk.PhotoImage(image)
canvas = tk.Canvas(topFrame, bg="#1e1e1e", width=200, height=55, highlightthickness=0)
canvas.pack(side=tk.LEFT, anchor=tk.NW)
canvas.create_image(100, 30, image=photo)

subTopFrame = tk.Frame(topFrame, width=450, height=28, bg="yellow")
subTopFrame.place(x=0, y=72)
subTopFrame.pack_propagate(False)

# Buttons in subTopFrame
buttons = [
    ("Home", lambda: print("Home clicked")),
    ("Display", lambda: print("Display clicked")),
    ("Recipe", lambda: print("Recipe clicked")),
    ("Manual", lambda: print("Manual clicked")),
    ("I-V", lambda: print("I-V clicked")),
    ("Setting", lambda: print("Setting clicked"))
]

for i, (text, command) in enumerate(buttons):
    button = tk.Button(subTopFrame, text=text, command=command,
                       bg="#1e1e1e", fg="#f0f0f0", font=("Helvetica", 12), highlightthickness=0, bd=0)
    button.grid(row=0, column=i, sticky="ew")
    subTopFrame.grid_columnconfigure(i, weight=1, uniform="equal")

# Bottom Frame
bottomFrame = tk.Frame(root, width=1360, height=662, bg="#f0f0f0")
bottomFrame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
bottomFrame.pack_propagate(False)

#label-Select Controller or Instrument
label = tk.Label(bottomFrame, text="Select Controller or Instrument", font=("Helvetica", 17), bg="#f0f0f0", fg="#1e1e1e")
label.pack(anchor="w", padx=10, pady=0)

# Devices frames -setting up basic arrays
Devices = [
    ("Temperature", lambda: print("Temperature clicked")),
    ("Mass Flow", lambda: print("Mass Flow clicked")),
    ("Humidity", lambda: print("Humidity clicked")),
    ("Pressure", lambda: print("Pressure clicked")),
    ("Measure", lambda: print("Measure clicked")),
    ("Sample Feeder", lambda: print("Sample Feeder clicked"))
]

Photos = [
    (Image.open(r".\Images_svg\Temperature.png"), lambda: print("Temperature")),
    (Image.open(r".\Images_svg\Mass Flow.png"), lambda: print("Mass Flow")),
    (Image.open(r".\Images_svg\Humidity.png"), lambda: print("Humidity")),
    (Image.open(r".\Images_svg\Pressure.png"), lambda: print("Pressure")),
    (Image.open(r".\Images_svg\Measure.png"), lambda: print("Measure")),
    (Image.open(r".\Images_svg\SampleFeeder.png"), lambda: print("Sample Feeder")),
]

Photos = [(ImageTk.PhotoImage(photo.resize((224, 240), Image.Resampling.LANCZOS)), command) for photo, command in Photos]
Photo_On = ImageTk.PhotoImage(Image.open(r".\Images_svg\Button_On.png").resize((224, 41), Image.Resampling.LANCZOS))
Photo_Off = ImageTk.PhotoImage(Image.open(r".\Images_svg\Button_Off.png").resize((224, 41), Image.Resampling.LANCZOS))

OnOffButtons = []
status_button = tk.StringVar(value="off") #for controlling on off switch of main

#configuring grid layout and creating device frame, device_label(text), and OnOffSwitch(Status)
bottomFrame.grid_rowconfigure(1, weight=1)  # Ensure the row is configured for expansion
for i, (text, command) in enumerate(Devices):
    # Create a frame for each device
    device_frame = tk.Frame(bottomFrame, width=224, height=400, bg="#f0f0f0", bd=0)
    if i == 0:
        device_frame.grid(row=1, column=i, padx=(10, 1), sticky="nwe",
                          pady=30)  # 20 pixels padding before the first frame
    else:
        device_frame.grid(row=1, column=i, padx=1, sticky="nwe", pady=30)  # Standard padding for the others\

    device_frame.pack_propagate(False)

    # Add a label to each device frame
    device_label = tk.Label(device_frame, text=text, font=("Helvetica", 15), bg="#f0f0f0", fg="black", width=224, anchor="w")
    device_label.pack(pady = (50, 40))

    #Clickable Images
    png_button = tk.Button(device_frame, image=Photos[i][0], command=Photos[i][1], bd=0, highlightthickness=0, anchor="n")
    png_button.pack(side=tk.TOP, pady=0)

    #Image Showing status
    status_image = tk.Label(device_frame, image=Photo_Off, width=224, bd=0, highlightthickness=0)
    status_image.pack(expand = True, fill=tk.BOTH)

    # # Add a button to each device frame
    # device_button = tk.Button(device_frame, text="Select", command=command, bg="lightblue", fg="black")
    # device_button.pack()

# Adjust column weights to ensure frames expand evenly
# for i in range(len(Devices)):
#     bottomFrame.grid_columnconfigure(i, weight=1)
root.mainloop()
