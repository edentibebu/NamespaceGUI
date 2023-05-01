from re import L
from tkinter import *
from tkinter import ttk
from ctypes import *
import subprocess
import os

import add_net_ns
import utils


class Home:
    def __init__(self, root):
        self.root = root
        self.frame = Frame(root)
        self.home()

    def home(self):
        # Add Namespace button
        net_namespace_frame = LabelFrame(self.root, text="Network Namespaces", padx=5, pady=5)
        net_namespace_frame.grid(row = 0, column = 0, padx=10, pady=10)
        add_ns_btn = Button(self.root, text="+", command = lambda \
            net_namespace_frame = net_namespace_frame: self.open_add_ns_window(net_namespace_frame))
        add_ns_btn.grid(row=0, column=1)
   
        self.display_ns(net_namespace_frame)

    def display_ns(self, net_namespace_frame):
        # List namespaces 
        for child in self.root.winfo_children():
            if isinstance(child,Toplevel) and child.title() == "Add New Network Namespace":
                    child.destroy()
        utils.update_ns(net_namespace_frame, self.root)
        #utils.list_namespaces(self.root, net_namespace_frame)

    def open_add_ns_window(self, net_namespace_frame):
        #top = Toplevel(self.root)
        add_net_ns.AddNS(self.root, net_namespace_frame)
