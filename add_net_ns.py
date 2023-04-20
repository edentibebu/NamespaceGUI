import subprocess
from tkinter import *
import tkinter as tk
from tkinter import ttk
import utils

def add_ns(ns_name):
    command_str = "ip netns add " + str(ns_name)
    result = subprocess.run(command_str, text = True, stderr=subprocess.PIPE, shell=True)
    if result.returncode != 0:
        utils.show_alert(result.stderr)

def add_veth(netns, device1, device2):
    command_str = "sudo ip link add " +str(device1) +" type veth peer name " +str(device2)+"; sudo ip link set " +str(device2)+" netns "+str(netns)
    result = subprocess.run((command_str), text=True, stderr=subprocess.PIPE, shell=True)
    if result.returncode != 0:
        utils.show_alert(result.stderr)

def set_ips(netns, device1, device2, ip1, ip2):
    subprocess.check_output("sudo ip netns exec "+str(netns)+" ifconfig " +str(device2)+" "+str(ip2)+" up; sudo ifconfig "+str(device1)+" " +str(ip1)+" up; ping "+str(ip2)+"; sudo ip netns exec "+str(netns)+" ping "+str(ip2), shell=True)

def update_ns_list(root, net_namespace_frame):
    update_ns_list(net_namespace_frame)
    root.update()

def add(root, net_namespace_frame, ns_name, device1, device2, ip1, ip2):
    ns_name = ns_name.get()
    device1 = device1.get()
    device2 = device2.get()
    ip1 = ip1.get()
    ip2 = ip2.get()
    #case 1: adding net ns without any device/ip specifications
    if ns_name and not device1 and not device2 and not ip1 and not ip2:
        add_ns(ns_name)
        print("adding: " , ns_name)
        update_ns_list(root, net_namespace_frame)
    # elif: #TODO check if namespace name already exists and show alert accordingly
    #     show_alert

    if ns_name and device1 and device2:
        print("adding Veth pairs")
        add_veth(ns_name, device1, device2)
    if device1 and device2 and ip1 and ip2:
        set_ips(ns_name, device1, device2, ip1, ip2)
    if not ns_name:
        utils.show_alert("you must specify the namespace name in order to add a network namespace.")