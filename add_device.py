from ctypes import util
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
        self.ns = ns.split("(id")[0]
        self.add_device_window(self.ns_view)
        #self.add_device_window()

    def add_device_window(self, ns_view):
        subnet = '10.1.1.'

        if(utils.checkuid[0] == "0"):
            Label(self.ns_view, text = self.ns).grid(row=0, column=0)

            #get list of other namespaces in the same subnet
            namespaces_list = utils.get_ns(self.ns)
            if len(namespaces_list) < 1:
                utils.show_alert("you must have more than one namespace created in order to connect via Veth ports.")
                return
            else: 
                add_device_window = Toplevel(self.root)
                add_device_window.title("Add Device to Namespace")
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
        if device1_num and device2_num:
            device2 = device2.get()
            device1_num = device1_num.get()
            device2_num = device2_num.get()

            port1 = device1 + "_" + device2
            port2  = device2 + "_" + device1

            ip1 = subnet + device1_num
            ip2 = subnet + device2_num

            utils.create_veth_pairs(device1, device2, port1, port2, ip1, ip2)
            utils.update_device_list(device2, ip2, self.ns_view, self.root)
        else: 
            utils.show_alert("you must provide a device number for both namespaces inorder to make the connection.")