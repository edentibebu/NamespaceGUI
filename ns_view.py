from tkinter import *
import tkinter as tk
from tkinter import ttk
import utils

#new window to view a namespace (on click of namespace name)
def net_ns_view(ns):

    #TODO: make this page scrollable!!
    ns_view = Toplevel(root)
    #ns_view = tk.Canvas(root)
    ns_view.title("Namespace GUI: Namespace View")
    #scrollbar = ttk.Scrollbar(root, orient="vertical", command=ns_view.yview)

    if(utils.checkuid[0] != "0"):
        Label(ns_view, text = "Sorry, you cannot access this window because you do not have root privileges").pack()
        return

    net_ns_header = Label(ns_view, text=ns)