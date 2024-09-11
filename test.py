import tkinter as tk
from tkinter import ttk

class MyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ttk.LabelFrame Example")
        self.geometry("400x300")

        # Create the main container frame
        main_frame = ttk.Frame(self, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")

        # Create a LabelFrame for the personal details section
        personal_frame = ttk.LabelFrame(main_frame, text="Personal Details", padding="10")
        personal_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # Add widgets to the personal_frame
        ttk.Label(personal_frame, text="Name:").grid(row=0, column=0, sticky="w")
        ttk.Entry(personal_frame).grid(row=0, column=1, sticky="ew")

        ttk.Label(personal_frame, text="Age:").grid(row=1, column=0, sticky="w")
        ttk.Entry(personal_frame).grid(row=1, column=1, sticky="ew")

        # Create a LabelFrame for the address section
        address_frame = ttk.LabelFrame(main_frame, text="Address", padding="10")
        address_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        # Add widgets to the address_frame
        ttk.Label(address_frame, text="Street:").grid(row=0, column=0, sticky="w")
        ttk.Entry(address_frame).grid(row=0, column=1, sticky="ew")

        ttk.Label(address_frame, text="City:").grid(row=1, column=0, sticky="w")
        ttk.Entry(address_frame).grid(row=1, column=1, sticky="ew")

        ttk.Label(address_frame, text="State:").grid(row=2, column=0, sticky="w")
        ttk.Entry(address_frame).grid(row=2, column=1, sticky="ew")

        # Adjust column weights so that the LabelFrames expand with the window
        main_frame.columnconfigure(0, weight=1)
        personal_frame.columnconfigure(1, weight=1)
        address_frame.columnconfigure(1, weight=1)

if __name__ == "__main__":
    app = MyApp()
    app.mainloop()
