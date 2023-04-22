import subprocess
from tkinter import *
import tkinter as tk
from tkinter import ttk
import utils

class AddDevice:
    def __init__(self, root, ns_view, ns):
        self.root = root
        self.frame = tk.Frame(root)
        self.ns_view = ns_view
        #self.label = tk.Label(self.frame, text="This is to Add Net Namespace")
        self.ns = ns
        self.add_device_window()

    def add_device_window(self):
        add_net_ns_window = Toplevel(self.root)
        add_net_ns_window.title("Add Device to Namespace")
        if(utils.checkuid[0] == "0"):
            Label(self.ns_view, text = self.ns).grid(row=0, column=1)

            #TODO: add functionality to make placeholder text grey that goes away after clicking in cell
            
            Label(add_net_ns_window, text ="VEth Pairs:").grid(row=2, column=0)
            Label(add_net_ns_window, text ="Device 1:").grid(row=1, column=1)
            Label(add_net_ns_window, text ="Device 1:").grid(row=1, column=2)
            device1 = Entry(add_net_ns_window)
            device1.grid(row=2, column=1)
            device2 = Entry(add_net_ns_window)
            device2.grid(row=2, column=2)

            Label(add_net_ns_window, text ="IP Addresses:").grid(row=4, column=0)
            Label(add_net_ns_window, text ="Address 1:").grid(row=3, column=1)
            Label(add_net_ns_window, text ="Address 2:").grid(row=3, column=2)

            ip1 = Entry(add_net_ns_window)
            ip1.grid(row=4, column=1)
            ip2 = Entry(add_net_ns_window)
            ip2.grid(row=4, column=2)
            add_ns_btn = Button(add_net_ns_window, text='Submit', command = lambda: self.add_device(self.ns, device1, device2, ip1, ip2))
            add_ns_btn.grid(row=5, column=4)
            
        else:
            Label(add_net_ns_window, text = "Sorry, you cannot access this window because you do not have root privileges").pack()
    def add_device(self, ns_name, device1, device2, ip1, ip2):
        print(ns_name)
        # device1 = device1.get()
        # device2 = device2.get()
        # ip1 = ip1.get()
        # ip2 = ip2.get()
        # # elif: #TODO check if namespace name already exists and show alert accordingly
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
