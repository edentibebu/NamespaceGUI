from ctypes import util
from dis import show_code
import subprocess
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter.font import names
import utils

class PortForwarding:
    def __init__(self, root, ns_view, ns):
        self.root = root
        self.frame = tk.Frame(root)
        #self.label = tk.Label(self.frame, text="This is to Add Net Namespace")
        self.ns_view = ns_view
        self.ns = ns.split("(id")[0]
        self.port_forwarding_window(self.ns_view)
    def port_forwarding_window(self, ns_view):
        if(utils.checkuid[0] == "0"):
            Label(self.ns_view, text = self.ns).grid(row=0, column=0)

            #get list of other namespaces in the same subnet
            namespaces_list = utils.get_ns(self.ns)
            if len(namespaces_list) < 1:
                utils.show_alert("you must have more than one namespace created in order to connect via Veth ports.")
                return
            else: 
                port_forward_window = Toplevel(self.root)
                port_forward_window.title("Port Forwarding")
                # Label(add_device_window, text ="VEth Pairs:").grid(row=2, column=0)
                # Label(add_device_window, text ="Device 1:").grid(row=1, column=1)
                # Label(add_device_window, text ="Device 2:").grid(row=1, column=2)
                # device1 = Label(add_device_window, text=self.ns, bg = 'white', relief="sunken", bd=2)
                # device1.grid(row=2, column=1)

                # create dropdown with list of other namespaces  
                veths_list = []
                for ns in namespaces_list:
                    veths = utils.get_veths(ns)
                    veths_list.append(veths)
                    print(veths)
                Label(port_forward_window, text = "Port Forwarding with " + self.ns).grid(row=0, column=0) 
                device2 = tk.StringVar()
                device2.set(namespaces_list[0])
                dropdown_menu = tk.OptionMenu(port_forward_window, device2, *veths_list) ## change namespaces list to something else
                Label(port_forward_window, text="Select Device: ").grid(row=1, column=0)
                dropdown_menu.grid(row=1, column=1)      
                #Label(port_forward_window, text ="Subnet: " + subnet).grid(row=3, column=0)
                Label(port_forward_window, text = "Forward from").grid(row=2, column=0)
                forward_from = Entry(port_forward_window)
                forward_from.grid(row=2, column=1)
                forward_to = Entry(port_forward_window)
                forward_to.grid(row=2, column=3)
                Label(port_forward_window, text="Forward to").grid(row=2, column=2)


                # #get subnet, leave entry for device numbers
                # device1_num = Entry(add_device_window)
                # device1_num.grid(row=4, column=1)
                # device2_num = Entry(add_device_window)
                # device2_num.grid(row=4, column=2)
                
                # add_ns_btn = Button(add_device_window, text='Submit', command = lambda: self.add_device(add_device_window, self.ns, device2, device1_num, device2_num, subnet))
                # add_ns_btn.grid(row=5, column=4)
