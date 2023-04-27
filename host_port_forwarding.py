from ctypes import util
from dis import show_code
import subprocess
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter.font import names
import utils

unsafe_ports_chrome = [1719, 1720, 1723, 2049, 3659, 4045, 5060, 5061, 6000, 6566, 6665, 6666, 6667, 6668, 6669, 6697, 10080]

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

            Label(port_forward_window, text = "Port Forwarding with " + self.ns).grid(row=0, column=0)

            device1 = Entry(port_forward_window)
            device1.grid(row=1, column=1)
            device2 = Entry(port_forward_window)
            device2.grid(row=1, column=3)
            Label(port_forward_window, text="Host Device #").grid(row=1, column=0) 
            Label(port_forward_window, text="Namespace Device #").grid(row=1, column=2) 
            Label(port_forward_window, text = "Host Port").grid(row=2, column=0)
            forward_from = Entry(port_forward_window)
            forward_from.grid(row=2, column=1)
            forward_to = Entry(port_forward_window)
            forward_to.grid(row=2, column=3)
            Label(port_forward_window, text="Namespace Port").grid(row=2, column=2)

            host_port_fwd = Button(port_forward_window, text='Submit', command = lambda: self.host_ip_forwarding(device1, device2, forward_from, forward_to))
            host_port_fwd.grid(row=4, column=4)
    def host_ip_forwarding(self, device1, device2, forward_from, forward_to):

        if not device1.get().isdigit() or not device2.get().isdigit():
            utils.show_alert("Please make sure that both device number inputs are numeric.")
            return
        if not forward_from.get().isdigit() or not forward_to.get().isdigit():
            utils.show_alert("Please make sure that the port number is numeric.")
            return
        if forward_to.get() in unsafe_ports_chrome:
            utils.show_alert("The port you are forwarding to is deemed unsafe by Chrome. Please select a different one.")
            return
        utils.create_veth_host_to_namespace(self.ns, device1.get(), device2.get())
        utils.enable_ns_to_host_ip_forwarding(self.ns, device2.get(), forward_from.get(), forward_to.get())