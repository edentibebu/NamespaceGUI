from ctypes import util
from dis import show_code
import subprocess
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter.font import names
import utils

class HostPortForwarding:
    def __init__(self, root, ns_view, ns):
        self.root = root
        self.ns_view = ns_view
        self.ns = ns
        self.host_port_forwarding_window(self.ns_view)
        
    def host_port_forwarding_window(self, ns_view):
        
        if(utils.checkuid[0] == "0"):
            Label(self.ns_view, text = self.ns).grid(row=0, column=0)

            #get list of other namespaces in the same subnet
            namespaces_list = utils.get_ns(self.ns.strip())
 
            port_forward_window = Toplevel(self.root)
            port_forward_window.title("Host Port Forwarding")

            devs1_list = []
            devices1 = utils.get_veths(self.ns)
            devs1_list.extend(devices1)
            Label(port_forward_window, text = "Port Forwarding with " + self.ns).grid(row=0, column=0)

            device1 = Entry(port_forward_window)
            device1.grid(row=1, column=1)
            
            Label(port_forward_window, text="Select Devices: ").grid(row=1, column=0) 

            Label(port_forward_window, text = "Forward from").grid(row=2, column=0)
            forward_from = Entry(port_forward_window)
            forward_from.grid(row=2, column=1)
            forward_to = Entry(port_forward_window)
            forward_to.grid(row=2, column=3)
            Label(port_forward_window, text="Forward to").grid(row=2, column=2)

            host_port_fwd = Button(port_forward_window, text='Submit', command = lambda: utils.enable_ns_to_host_ip_forwarding(self.ns, device1.get(), forward_from.get(), forward_to.get()))
            host_port_fwd.grid(row=4, column=4)