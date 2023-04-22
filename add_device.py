import subprocess
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter.font import names
import utils

class AddDevice:
    def __init__(self, root, ns_view, ns):
        self.root = root
        self.frame = tk.Frame(root)
        #self.label = tk.Label(self.frame, text="This is to Add Net Namespace")
        self.ns_view = ns_view
        self.ns = ns
        self.add_device_window(self.ns_view)
        #self.add_device_window()

    def add_device_window(self, ns_view):
        subnet = '10.1.1.'
        add_device_window = Toplevel(self.root)
        add_device_window.title("Add Device to Namespace")
        if(utils.checkuid[0] == "0"):
            Label(self.ns_view, text = self.ns).grid(row=0, column=0)

            #device 1 should just be listed
            #TODO: get list of other namespaces in the same subnet
            namespaces_list = utils.get_ns(self.ns)
            if len(namespaces_list) < 1:
                utils.show_alert("you must have more than one namespace created in order to connect via Veth ports.")
                return
            Label(add_device_window, text ="VEth Pairs:").grid(row=2, column=0)
            Label(add_device_window, text ="Device 1:").grid(row=1, column=1)
            Label(add_device_window, text ="Device 2:").grid(row=1, column=2)
            device1 = Label(add_device_window, text=self.ns, bg = 'white', relief="sunken", bd=2)
            device1.grid(row=2, column=1)

            #create dropdown with list of other namespaces   
            device2 = tk.StringVar()
            device2.set(namespaces_list[0])
            dropdown_menu = tk.OptionMenu(add_device_window, device2, *namespaces_list)
            dropdown_menu.grid(row=2, column=2)      
            Label(add_device_window, text ="Subnet: " + subnet).grid(row=3, column=0)
            Label(add_device_window, text = "Device numbers").grid(row=4, column=0)

            #get subnet, leave entry for device numbers
            device1_num = Entry(add_device_window)
            device1_num.grid(row=4, column=1)
            device2_num = Entry(add_device_window)
            device2_num.grid(row=4, column=2)
            
            add_ns_btn = Button(add_device_window, text='Submit', command = lambda: self.add_device(add_device_window, self.ns, device2, device1_num, device2_num, subnet))
            add_ns_btn.grid(row=5, column=4)
            
        else:
            Label(add_device_window, text = "Sorry, you cannot access this window because you do not have root privileges").pack()
    def add_device(self, add_device_window, device1, device2, device1_num, device2_num, subnet):
        print("adding device")

        device2 = device2.get()
        print(device2)
        device1_num = device1_num.get()
        device2_num = device2_num.get()

        port1 = device1 + "_" + device2
        port2  = device2 + "_" + device1
        # elif: #TODO check if namespace name already exists and show alert accordingly
        # #     show_alert
        # #case 2: add ns_name and make veth pair
        # if device1 and device2 and (ip1 or ip2):
        #     utils.add_ns(ns_name)
        #     utils.add_veth(ns_name, device1, device2)
        #     if ip1:
        #         utils.set_one_ip(ns_name, device1, device2, ip1)
        #     else:
        #         utils.set_one_ip(ns_name, device1, device2, ip2)
        #     utils.update_ns_list(ns_name, self.ns_view, self.root)
            
        # elif ns_name and device1 and device2:
        #     utils.add_ns(ns_name)
        #     utils.add_veth(ns_name, device1, device2)
        #     utils.update_ns_list(ns_name, self.ns_view, self.root)
        # #case 3: add ns_name, make veth pair, add ip addresses
        # elif ns_name and device1 and device2 and ip1 and ip2:
        #     utils.add_ns(ns_name)
        #     utils.add_veth(ns_name, device1, device2)
        #     utils.set_ips(ns_name, device1, device2, ip1, ip2)
        #     utils.update_ns_list(ns_name, self.ns_view, self.root)
        # elif not ns_name:
        #     utils.show_alert("you must specify the namespace name in order to add a network namespace.")
