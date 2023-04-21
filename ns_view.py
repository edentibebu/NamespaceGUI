from tkinter import *
import tkinter as tk
from tkinter import ttk
import utils

#new window to view a namespace (on click of namespace name)
class NSView:
    def __init__(self, root, ns):
        self.root = root
        self.frame = Frame(root)
        self.ns = ns
        self.net_ns_view()
    def net_ns_view(self):
        ns_view = Toplevel(self.root)
        ns_view.title("Namespace GUI: Namespace View")

        if(utils.checkuid[0] != "0"):
            Label(ns_view, text = "Sorry, you cannot access this window because you do not have root privileges").pack()
            return

        #list device pairs
        veth_list = utils.get_veth_pairs(self.ns)
        print(veth_list)
        #print(veth_list)

        # for veth in veth_list:
        #     print(utils.get_peer(veth))

        net_ns_header = Label(ns_view, text=self.ns)
        net_ns_header.grid(row=0,column=0)