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
            namespaces_list = utils.get_ns(self.ns.strip())
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
                # devs1_list, devs2_list = [], []
            
                # for ns in namespaces_list:
                #     veths = utils.get_veths(ns)
                #     if veths:
                #         devs2_list.extend(veths)
                # devices1 = utils.get_veths(self.ns)
                devs1_list = utils.get_veths(self.ns)
                #devs1_list.extend(devices1)
                Label(port_forward_window, text = "Port Forwarding with " + self.ns).grid(row=0, column=0) 

         

                dropdown_list = []

                for dev in devs1_list:
                    peer_ns = utils.get_peer(self.ns, dev)
                    dropdown_list.append("add " + dev + " to " +  peer_ns)
                device1 = tk.StringVar()
                device1.set(dropdown_list[0])
                dropdown_menu = tk.OptionMenu(port_forward_window, device1, *dropdown_list)
                
                Label(port_forward_window, text="Select Devices: ").grid(row=1, column=0)
   
                dropdown_menu.grid(row=1,column=1)   
                #Label(port_forward_window, text ="Subnet: " + subnet).grid(row=3, column=0)
                Label(port_forward_window, text = "Forward from").grid(row=2, column=0)
                forward_from = Entry(port_forward_window)
                forward_from.grid(row=2, column=1)
                forward_to = Entry(port_forward_window)
                forward_to.grid(row=2, column=3)
                Label(port_forward_window, text="Forward to").grid(row=2, column=2)
                
                ## get namespace associated to a device


                #add_ns_btn = Button(port_forward_window, text='Submit', command = lambda: utils.enable_ns_to_ns_ip_forwarding('10.1.1.', device1.get(), device2.get(), forward_from.get(), forward_to.get(), ns2))
                #add_ns_btn.grid(row=4, column=4)
