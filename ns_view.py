from tkinter import *
import tkinter as tk
from tkinter import ttk
#from test import delete_ns
import utils, add_device, port_forwarding

#new window to view a namespace (on click of namespace name)
class NSView:
    def __init__(self, root, ns, net_namespace_frame):
        self.root = root
        self.frame = Frame(root)
        self.ns = ns.split("(id")[0]
        self.net_namespace_frame = net_namespace_frame
        self.net_ns_view()
    def net_ns_view(self):
        ns_view = Toplevel(self.root)
        ns_view.title("Namespace GUI: Namespace View")

        if(utils.checkuid[0] != "0"):
            Label(ns_view, text = "Sorry, you cannot access this window because you do not have root privileges").pack()
            return

        # list device pairs
        devs = utils.get_veths(self.ns.strip())
        print(devs)
        utils.show_devices(ns_view, self.ns.strip())

        net_ns_header = Label(ns_view, text=self.ns)
        net_ns_header.grid(row=0,column=0)

        add_device_btn = Button(ns_view, text="Add Device", command = lambda \
            ns_view = ns_view : self.open_add_device_window(ns_view))
        add_device_btn.grid(row=1, column=1)

        delete_ns_btn = Button (ns_view, text = "Delete Namespace", command = lambda : 
            self.delete_ns(self.ns.strip(), self.net_namespace_frame, self.root, ns_view))
        delete_ns_btn.grid(row=2, column=1)

        port_forward_btn = Button(ns_view, text = "Add Port for Forwarding", command = lambda \
            ns = self.ns.strip() : self.open_port_forwarding_window(ns, ns_view))
        port_forward_btn.grid(row=3, column=1)

    def open_port_forwarding_window(self, ns, ns_view):
        print("window for port forwarding")
        port_forwarding.PortForwarding(self.root, ns_view, ns)

    def open_add_device_window(self, ns_view):
        add_device.AddDevice(self.root, ns_view, self.ns)

    def delete_ns(self, ns, net_namespace_frame, root, ns_view):
        utils.rm_ns(ns, net_namespace_frame, root)
        ns_view.destroy()        
        
