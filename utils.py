from os import device_encoding
from re import sub
import re
import subprocess
from sys import stderr
from tkinter import *
import tkinter as tk
from tkinter import ttk
from unicodedata import decimal
from webbrowser import get
import ns_view

checkuid = subprocess.check_output("id -u", shell=True).decode()
occupied_devices = []
def get_occupied_devices():
    net_ns = get_net_namespaces()
    ns_list = net_ns.split('\n')[:-1]
    for ns in ns_list:
        ns = ns.split('(id')[0].strip()
        veths = get_veths(ns)
        occupied_devices.extend(veths)

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

def list_namespaces(root, namespace_frame):
    # get namespaces as list from C code
    net_ns = get_net_namespaces()
    net_ns_list = net_ns.split('\n')[:-1]

    for i, ns in enumerate(net_ns_list):
        ns_btn = Button(namespace_frame, text=ns, command=lambda ns=ns: ns_view.NSView(root, ns, namespace_frame))
        ns_btn.grid(row = i+1, column = 0)

### ADD NS WINDOW ###
def add_ns(ns_name, net_namespace_frame, root):
    command_str = "ip netns add " + str(ns_name)
    result = subprocess.run(command_str, text = True, stderr=subprocess.PIPE, shell=True)
    if result.returncode != 0:
        show_alert(result.stderr)
        return
    ## Adding Loopback
    command_str = 'ip netns exec ' + str(ns_name) + ' ip link set dev lo up'
    result = subprocess.run(command_str, text = True, stderr=subprocess.PIPE, shell=True)
    if result.returncode != 0:
        show_alert(result.stderr)
        return
    update_ns(net_namespace_frame, root)

def rm_ns(ns_name, net_namespace_frame, root):
        # find devices in the namespace being deleted
   
    veths = get_veths(ns_name)
    for veth in veths:
        if(veth in occupied_devices):
            occupied_devices.remove(veth)

                
    # go through other namespaces and see if any other devices were connected to this namespace
    ns_list = get_ns(ns_name)
    for ns in ns_list:
        veths = get_veths(ns)
        for veth in veths:
            if(veth in occupied_devices):
                peer_ns = get_peer(ns, veth)
                if peer_ns == ns_name:
                    occupied_devices.remove(veth)
   
                             
    server_cleanup(ns_name)
    command_str = "ip netns delete " + ns_name.strip()
    result = subprocess.run(command_str, text=True, capture_output=True, shell=True)
    if result.returncode != 0:
        show_alert(result.stderr)
        return
      
    # command for removing namespace 
    update_ns(net_namespace_frame, root)
    # TODO: unoccupy_devices() ## Remove devices from our list
def add_veth(netns, device1, device2):
    command_str = "sudo ip link add " +str(device1) +" type veth peer name " +str(device2)+"; sudo ip link set " +str(device2)+" netns "+str(netns)
    result = subprocess.run((command_str), text=True, stderr=subprocess.PIPE, shell=True)
    if result.returncode != 0:
        show_alert(result.stderr)

def set_one_ip(netns, device1, device2, ip):
    command_str = "sudo ip addr add "+str(ip)+"/24 dev "+str(device2)+"; sudo ip link set "+str(device1)+" up; sudo ip netns exec "+str(netns)+" ip link set "+str(device2) +" up"
    result = subprocess.run(command_str, text=True, stderr=subprocess.PIPE, shell=True)
    if result.returncode != 0:
        show_alert(result.stderr)

def set_ips(netns, device1, device2, ip1, ip2):
    command_str = "sudo ip addr add "+str(ip1)+"/24 dev "+str(device1)+"; sudo ip netns exec "+str(netns)+" ip addr add "+str(ip2)+"/24 dev "+str(device2)+""
    result = subprocess.run(command_str, text=True, stderr=subprocess.PIPE, shell=True)
    if result.returncode != 0:
        show_alert(result.stderr)

def update_ns(net_namespace_frame, root):
    for widget in net_namespace_frame.winfo_children():
        widget.destroy()
    # List namespaces 
    list_namespaces(root, net_namespace_frame)
#### NET NS VIEW ####
def get_veths(ns):
    command_str = "sudo ip netns exec "+str(ns.strip())+" ip link show type veth;"
    result = subprocess.run(command_str, text = True, capture_output=True, shell=True)
    if result.returncode != 0:
        show_alert(result.stderr)
        return
    devs_list = (result.stdout).split("\n")[0::2]
    for i, dev in enumerate(devs_list):
        devs_list[i] = dev.split("@")[0]
    devs_list = [dev for dev in devs_list if dev.strip()]        
    for i, dev in enumerate(devs_list):
        if(dev.split(":")[1]):
            devs_list[i] = dev.split(":")[1]
    devs_list = [dev.strip() for dev in devs_list]
    return devs_list

def create_veth_pairs(ns1, ns2, device1, device2, ip1, ip2, ns_view):
    ##check if device is already connected to a different device
    if(device1 in occupied_devices):
        show_alert("First device is already connected to something else. choose another device number.")
        return
    if(device2 in occupied_devices):
        show_alert("Second device is already connected to something else. choose another device number.")
        return

    command_str = "ip link add "+str(device1)+" type veth peer name "+str(device2)
    result = subprocess.run(command_str, text=True, capture_output =True, shell=True) # create devices
    if result.returncode != 0:
        show_alert(result.stderr)
        return
    #link devices to respective namespaces
    command_str = "ip link set "+str(device1)+" netns "+str(ns1)
    result = subprocess.run(command_str, text=True, capture_output =True, shell=True)
    if result.returncode != 0:
        show_alert(result.stderr)
        return
    command_str = "ip link set "+str(device2)+" netns "+str(ns2)
    result = subprocess.run(command_str, text=True, capture_output =True, shell=True)
    if result.returncode != 0:
        show_alert(result.stderr)
        return
    #in NS1, set ipaddr for device 1 (same for NS2)
    command_str = "ip netns exec "+str(ns1)+" ip addr add "+str(ip1)+" dev "+str(device1)
    result = subprocess.run(command_str, text=True, capture_output =True, shell=True)
    if result.returncode != 0:
        show_alert(result.stderr)
        return
    command_str = "ip netns exec "+str(ns2)+" ip addr add "+str(ip2)+" dev "+str(device2)
    result = subprocess.run(command_str, text=True, capture_output =True, shell=True)
    if result.returncode != 0:
        show_alert(result.stderr)
        return

    #set up network interfaces
    command_str = "ip netns exec "+str(ns1)+" ifconfig "+str(device1)+" "+str(ip1)+" up"
    result = subprocess.run(command_str, text=True, capture_output =True, shell=True)
    if result.returncode != 0:
        print(result.stderr)
        return
    command_str = "ip netns exec "+str(ns2)+" ifconfig "+str(device2)+" "+str(ip2)+" up"
    result = subprocess.run(command_str, text=True, capture_output =True, shell=True)
    if result.returncode != 0:
        print(result.stderr)
        return
    occupied_devices.append(device1)
    occupied_devices.append(device2)
    update_device_list(device1, ns1, ns2, ns_view)

def show_devices(ns_view, ns):
    veths = get_veths(ns)
    for i, veth in enumerate(veths): 
        peer_ns = get_peer(ns, veth)
        device = Label(ns_view, text= "device " + veth + " is connected to " + peer_ns)
        device.grid(row = i+1, column = 0)

def update_device_list(device1_num, ns1, ns2, ns_view):
    num_veths = len(get_veths(ns1))
    text = "device " + device1_num + " is connected to " + ns2

    ns_btn = Label(ns_view, text=text)
    ns_btn.grid(row = num_veths+1, column = 0)
    
def get_peer(ns, veth):
    peer = None
    command_str = "sudo ip netns exec "+str(ns.strip())+" ip link show " + str(veth)
    result = subprocess.run(command_str, text=True, capture_output=True, shell=True)
    if(result.returncode != 0):
        show_alert(result.stderr)
        return
    devices = result.stdout.split('\n')[1:]
    devices = [s.strip() for s in devices if s.strip()]
    for device in devices:
        if "link-netns" in device:
            peer = device.split(' ')[-1]
    return peer
        
def get_ns(ns_name): # for dropdowns
    result = subprocess.run("ip netns list", text=True, capture_output =True, shell=True)
    ns_list = result.stdout.split('\n')

    for i, ns in enumerate(ns_list):
        ns_list[i] = ns.split('(id')[0].strip() #clean up outputs
    #list of all namespaces
    ns_list = list(filter(lambda s: s != "", ns_list))
    if ns_name in ns_list:
        ns_list.remove(ns_name)        
    return ns_list

def enable_ns_to_host_ip_forwarding(ns, device, port1, port2):
    subprocess.run("sysctl -w net.ipv4.ip_forward=1", shell=True)
    subprocess.run("iptables -t nat -A PREROUTING -p tcp --dport "+str(port1)+" -j DNAT --to-destination 10.1.1."+str(device)+":"+str(port2)+"", shell=True)
    subprocess.run("iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE", shell=True)
    subprocess.run("ip netns exec "+str(ns)+" nohup python -m http.server "+str(port2)+" > /dev/null 2>&1 &", text=True, capture_output=True, shell=True)

def server_cleanup(ns):
    pid = subprocess.check_output("sudo ip netns exec "+str(ns)+" ps -ef | grep 'python -m http.server' | grep -v grep | awk '{print $2}'", shell=True)
    pid = pid.decode()
    if pid:
        result = subprocess.run("kill "+str(pid)+"", text=True, capture_output=True, shell=True)
        if(result.returncode != 0):
            show_alert(result.stderr)
            return
def create_veth_host_to_namespace(ns, device1, device2):
    subprocess.run("ip link add "+str(device1)+" type veth peer name "+str(device2)+"", shell=True)
    subprocess.run("ip link set "+str(device2)+" netns "+str(ns)+"", shell=True)
    subprocess.run("ip addr add 10.1.1."+str(device1)+"/24 dev "+str(device1)+"", shell=True)
    subprocess.run("ip link set dev "+str(device1)+" up", shell=True)
    subprocess.run("ip netns exec "+str(ns)+" ip addr add 10.1.1."+str(device2)+"/24 dev "+str(device2)+"", shell=True)
    subprocess.run("ip netns exec "+str(ns)+" ip link set dev "+str(device2)+" up", shell=True)
    subprocess.run("ip netns exec "+str(ns)+" ip route add default via 10.1.1."+str(device1)+"", shell=True)
