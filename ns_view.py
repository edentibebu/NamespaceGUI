from tkinter import *
import tkinter as tk
from tkinter import ttk
import utils, add_device

#new window to view a namespace (on click of namespace name)
class NSView:
    def __init__(self, root, ns):
        self.root = root
        self.frame = Frame(root)
        self.ns = ns.split("(id")[0]
        self.net_ns_view()
    def net_ns_view(self):
        ns_view = Toplevel(self.root)
        ns_view.title("Namespace GUI: Namespace View")

        if(utils.checkuid[0] != "0"):
            Label(ns_view, text = "Sorry, you cannot access this window because you do not have root privileges").pack()
            return

        # list device pairs
        print(self.ns)
        utils.get_veths(self.ns.strip())
        # print("orig veth:", veth_list)
        # peer = utils.get_peer(veth_list)
        # print(peer)

        # # TODO: extend this to iterate through a list of device pairs

        # for veth in veth_list:
        #     peer = utils.get_peer(veth)
        #     print(veth, peer)

        #     #TODO: with each device pair, show associated ip address mappings



        net_ns_header = Label(ns_view, text=self.ns)
        net_ns_header.grid(row=0,column=0)

        add_device_btn = Button(ns_view, text="Add Device", command = lambda \
            ns_view = ns_view : self.open_add_device_window(ns_view))
        add_device_btn.grid(row=1, column=1)
    def open_add_device_window(self, ns_view):
        add_device.AddDevice(self.root, ns_view, self.ns)
