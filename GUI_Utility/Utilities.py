from tkinter import *
from tkinter import ttk

def print_hierarchy(w, depth=0):
    print('  '*depth + w.winfo_class() + ' w=' + str(w.winfo_width()) + ' h=' + str(w.winfo_height()) +
          ' x=' + str(w.winfo_x()) + ' y=' + str(w.winfo_y()))
    for i in w.winfor_children():
        print_hierarchy(i, depth+1)