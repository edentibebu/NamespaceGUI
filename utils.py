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

def list_namespaces(namespace_frame):
    # get namespaces as list from C code
    net_ns = get_net_namespaces()
    net_ns_list = net_ns.split('\n')[:-1]

    for i, ns in enumerate(net_ns_list):
        ns_btn = Button(namespace_frame, text=ns, command=lambda ns=ns: ns_view.net_ns_view(ns)) #TODO: clicking on button brings up NS-view.py for editing
        ns_btn.grid(row = i+1, column = 0) # TODO: row will change for each namespace, column will not. add padding around text

def add_ns(self, ns_name):
    command_str = "ip netns add " + str(ns_name)
    result = subprocess.run(command_str, text = True, stderr=subprocess.PIPE, shell=True)
    if result.returncode != 0:
        show_alert(result.stderr)

def add_veth(netns, device1, device2):
    command_str = "sudo ip link add " +str(device1) +" type veth peer name " +str(device2)+"; sudo ip link set " +str(device2)+" netns "+str(netns)
    result = subprocess.run((command_str), text=True, stderr=subprocess.PIPE, shell=True)
    if result.returncode != 0:
        show_alert(result.stderr)

def set_ips(netns, device1, device2, ip1, ip2):
    subprocess.check_output("sudo ip netns exec "+str(netns)+" ifconfig " +str(device2)+" "+str(ip2)+" up; sudo ifconfig "+str(device1)+" " +str(ip1)+" up; ping "+str(ip2)+"; sudo ip netns exec "+str(netns)+" ping "+str(ip2), shell=True)

def update_ns_list(ns_name, net_namespace_frame):
    net_ns = get_net_namespaces()
    num_ns = len(net_ns.split('\n')[:-1])
    ns_btn = Button(net_namespace_frame, text=ns_name, command=lambda ns=ns_name: ns_view.net_ns_view(ns)) #TODO: clicking on button brings up NS-view.py for editing
    ns_btn.grid(row = num_ns+1, column = 0) # TODO: row will change for each namespace, column will not. add padding around text


def top_5_cpu():
    output = subprocess.check_output("ps -eo pid,ppid,%cpu,%mem,cmd --sort=-%cpu | head -n 6", shell=True)
    cpu = output.decode()
    return cpu

def top_5_mem():
    output = subprocess.check_output("ps -eo pid,ppid,%cpu,%mem --sort=-%mem | head -n 6", shell=True)
    mem = output.decode()
    return mem

def get_cap(ns):
    output = []
    output = subprocess.check_output("sudo ip netns exec " + str(ns) + " capsh --print", shell=True)
    caps = output.decode()
    return caps

def get_procs(ns):
    output = subprocess.check_output("ps u $(ip netns pids " + str(ns) + ")", shell=True)
    procs = output.decode('utf-8').split('\n')
    return procs