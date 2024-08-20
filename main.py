import tkinter as tk
from PIL import Image, ImageTk

# Initialize the main window
root = tk.Tk()
root.title("Nextron Program")
root.geometry("1367x770")

# Load and set the window icon
image = Image.open(r".\Images_logo\RootLogo.png")
root.iconphoto(False, ImageTk.PhotoImage(image))

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

# Sub frame for label
subBottomFrame_Label = tk.Frame(bottomFrame, width=1360, height=90, bg="blue")
subBottomFrame_Label.pack(side=tk.TOP, fill=tk.X)
subBottomFrame_Label.pack_propagate(False)

label = tk.Label(subBottomFrame_Label, text="Select Controller or Instrument", font=("Helvetica", 17), bg="blue", fg="#1e1e1e")
label.pack(anchor="w", padx=10, pady=10)

# Grid setup for device frames
bottomFrame.grid_rowconfigure(1, weight=1)  # Ensure the row is configured for expansion

# Devices frames
Devices = [
    ("Temperature", lambda: print("Temperature clicked")),
    ("Mass Flow", lambda: print("Mass Flow clicked")),
    ("Humidity", lambda: print("Humidity clicked")),
    ("Pressure", lambda: print("Pressure clicked")),
    ("Measure", lambda: print("Measure clicked")),
    ("Sample Feeder", lambda: print("Sample Feeder clicked"))
]

for i, (text, command) in enumerate(Devices):
    # Create a frame for each device
    device_frame = tk.Frame(bottomFrame, width=200, height=100, bg="blue", bd=2)
    device_frame.grid(row=1, column=i, padx=10, pady=10, sticky="ew")

    # Add a label to each device frame
    device_label = tk.Label(device_frame, text=text, font=("Helvetica", 12), bg="red", fg="black", width=224, height=2)
    device_label.pack(expand=True, fill=tk.BOTH)

    # Add a button to each device frame
    device_button = tk.Button(device_frame, text="Select", command=command, bg="lightblue", fg="black")
    device_button.pack()

# Adjust column weights to ensure frames expand evenly
for i in range(len(Devices)):
    bottomFrame.grid_columnconfigure(i, weight=1)

root.mainloop()
