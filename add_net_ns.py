import subprocess
from tkinter import *
import tkinter as tk
from tkinter import ttk
import utils, ns_view

class AddNS:
    def __init__(self, root, net_namespace_frame):
        self.root = root
        self.frame = tk.Frame(root)
        #self.label = tk.Label(self.frame, text="This is to Add Net Namespace")
        self.net_namespace_frame = net_namespace_frame
        self.add_net_ns_window(self.net_namespace_frame)

    def add_net_ns_window(self, net_namespace_frame):
        add_net_ns_window = Toplevel(self.root)
        add_net_ns_window.title("Add New Network Namespace")
        if(utils.checkuid[0] == "0"):
            Label(add_net_ns_window, text ="Name:").grid(row=0, column=0)
            ns_name = Entry(add_net_ns_window)
            ns_name.grid(row=0, column=1)

            #TODO: add functionality to make placeholder text grey that goes away after clicking in cell

            add_ns_btn = Button(add_net_ns_window, text='Submit', command = lambda: self.add(net_namespace_frame, ns_name))
            add_ns_btn.grid(row=5, column=4)
            
        else:
            Label(add_net_ns_window, text = "Sorry, you cannot access this window because you do not have root privileges").pack()
    def add(self, net_namespace_frame, ns_name):
        ns_name = ns_name.get()
        if not ns_name:
            utils.show_alert("you must specify the namespace name in order to add a network namespace.")
        else:
            utils.add_ns(ns_name)
            utils.update_ns(net_namespace_frame, self.root)
