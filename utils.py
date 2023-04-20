import subprocess
from tkinter import *
import tkinter as tk
from tkinter import ttk
import ns_view

checkuid = subprocess.check_output("id -u", shell=True).decode()

def show_alert(message):
    alert_window = Toplevel()
    alert_window.title("Alert")
    alert_label = Label(alert_window, text=message)
    alert_label.pack(padx=20, pady=20)
    ok_button = Button(alert_window, text="OK", command=alert_window.destroy)
    ok_button.pack(pady=10)

def get_net_namespaces():
    output = []
    if(checkuid[0] == '0'):
        output = subprocess.check_output("sudo ip netns", shell=True)
    else:
        output = subprocess.check_output('ip netns', shell=True)

    net_namespaces = output.decode()
    return net_namespaces

def list_namespaces(net_namespace_frame):
    # get namespaces as list from C code
    net_ns = get_net_namespaces()
    net_ns_list = net_ns.split('\n')[:-1]

    for i, ns in enumerate(net_ns_list):
        ns_btn = Button(net_namespace_frame, text=ns, command=lambda ns=ns: ns_view.net_ns_view(ns)) #TODO: clicking on button brings up NS-view.py for editing
        ns_btn.grid(row = i+1, column = 0) # TODO: row will change for each namespace, column will not. add padding around text