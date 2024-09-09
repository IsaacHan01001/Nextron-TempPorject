from tkinter import *
import tkinter.ttk as ttk
import os
from PIL import Image, ImageTk

def print_hierarchy(w, depth=0):
    print('  '*depth + w.winfo_class() + ' w=' + str(w.winfo_width()) + ' h=' + str(w.winfo_height()) +
          ' x=' + str(w.winfo_x()) + ' y=' + str(w.winfo_y()))
    for i in w.winfor_children():
        print_hierarchy(i, depth+1)

def makeIconPhoto():
    path = os.path.join(os.path.dirname(__file__), "../Images_logo/RootLogo.png")
    image = ImageTk.PhotoImage(Image.open(path).resize((180, 50), Image.Resampling.LANCZOS))
    return image
# Window Depth
def printWindowDepth(root, window):
    print(root.tk.eval("WM_stackorder " + str(window)))
