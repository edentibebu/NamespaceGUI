from os import device_encoding
from re import sub
import re
import subprocess
from tkinter import *
import tkinter as tk
from tkinter import ttk
import ns_view

checkuid = subprocess.check_output("id -u", shell=True).decode()
occupied_devices = []
def show_alert(message):
    alert_window = Toplevel()
    alert_window.title("Alert")
    alert_label = Label(alert_window, text=message)
    alert_label.pack(padx=20, pady=20)
    ok_button = Button(alert_window, text="OK", command=alert_window.destroy)
    ok_button.pack(pady=10)

def get_net_namespaces():
    # print("get namespaces")
    output = []
    if(checkuid[0] == '0'):
        output = subprocess.check_output("sudo ip netns", shell=True)
    else:
        output = subprocess.check_output('ip netns', shell=True)

    net_namespaces = output.decode()
    return net_namespaces

def list_namespaces(root, namespace_frame):
    # get namespaces as list from C code
    # print("listing namespaces")
    net_ns = get_net_namespaces()
    net_ns_list = net_ns.split('\n')[:-1]

    for i, ns in enumerate(net_ns_list):
        ns_btn = Button(namespace_frame, text=ns, command=lambda ns=ns: ns_view.NSView(root, ns, namespace_frame))
        ns_btn.grid(row = i+1, column = 0)

### ADD NS WINDOW ###
def add_ns(ns_name, net_namespace_frame, root):
    print("add ns")
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
    print("DELETING")
    #command_str = "sudo ip netns exec " + str(ns_name) + " lsof -i | awk 'S1=="COMMAND" {next } {print S2}'"
    result = subprocess.run("sudo ip netns exec " + str(ns_name) + " lsof -i | awk 'S1==\"COMMAND\" {next } {print S2}'", text=True, capture_output = True, shell=True)
    if result.returncode != 0:
        show_alert(result.stderr)
        return
    pids = result.stdout
    print(pids)
    command_str = "ip netns delete " + ns_name.strip()
    result = subprocess.run(command_str, text=True, capture_output=True, shell=True)
    if result.returncode != 0:
        show_alert(result.stderr)
        return
    update_ns(net_namespace_frame, root)
    # command for removing namespace 
    update_ns(net_namespace_frame, root)
    # TODO: unoccupy_devices() ## Remove devices from our list
def add_veth(netns, device1, device2):
    command_str = "sudo ip link add " +str(device1) +" type veth peer name " +str(device2)+"; sudo ip link set " +str(device2)+" netns "+str(netns)
    result = subprocess.run((command_str), text=True, stderr=subprocess.PIPE, shell=True)
    if result.returncode != 0:
        show_alert(result.stderr)

def create_veth_pairs(ns, device1, device2, ip1, ip2):
    # subprocess.run("sudo ip link add "+str(device1)+" type veth peer name "+str(device2), shell=True)
    # subprocess.run("sudo ip link set "+str(device2)+" netns "+str(ns), shell=True)
    subprocess.run("sudo ip addr add "+str(ip1)+"/24 dev "+str(device1)+"; sudo ip netns exec "+str(ns)+" ip addr add "+str(ip2)+"/24 dev "+str(device2)+"", shell=True)
    subprocess.run("sudo ip link set "+str(device1)+" up; sudo ip netns exec "+str(ns)+" ip link set "+str(device2)+" up", shell=True)

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
    print("updating")
    for widget in net_namespace_frame.winfo_children():
        widget.destroy()
    #net_namespace_frame = LabelFrame(root, text="Network Namespaces", padx=5, pady=5)
    #net_namespace_frame.grid(row = 0, column = 0, padx=10, pady=10)
    # List namespaces 
    list_namespaces(root, net_namespace_frame)
#### NET NS VIEW ####
def disp_routing():
    output = subprocess.check_output("ip netns exec ns1 route", shell=True)
    routes = output.decode()
    print(routes)
    return routes

def list_sockets():
    output = subprocess.check_output("ip netns exec ns1 ss -n -a", shell=True)
    sockets = output.decode()
    print(sockets)
    return sockets

def get_veths(ns):
    command_str = "sudo ip netns exec "+str(ns.strip())+" ip link show type veth;"
    result = subprocess.run(command_str, text = True, capture_output=True, shell=True)
    if result.returncode != 0:
        show_alert(result.stderr)
        return
    print(result.stdout)
    devs_list = (result.stdout).split("\n")[0::2]
    for i, dev in enumerate(devs_list):
        devs_list[i] = dev.split("@")[0]
    devs_list = [dev for dev in devs_list if dev.strip()]        
    for i, dev in enumerate(devs_list):
        if(dev.split(":")[1]):
            devs_list[i] = dev.split(":")[1]
    devs_list = [dev.strip() for dev in devs_list]
    return devs_list

def create_veth_pairs(ns1, ns2, device1, device2, ip1, ip2):
    ##check if device is already connected to a different device
    if(device1 in occupied_devices):
        show_alert("this device is already connected to something else. choose another device number.")
    print("creating dev pair")
    command_str = "ip link add "+str(device1)+" type veth peer name "+str(device2)
    result = subprocess.run(command_str, text=True, capture_output =True, shell=True) # create devices
    if result.returncode != 0:
        show_alert(result.stderr)
        return
    #link devices to respective namespaces
    print("link device1 to ns")
    command_str = "ip link set "+str(device1)+" netns "+str(ns1)
    result = subprocess.run(command_str, text=True, capture_output =True, shell=True)
    if result.returncode != 0:
        show_alert(result.stderr)
        return
    print("link device2 to ns2")
    command_str = "ip link set "+str(device2)+" netns "+str(ns2)
    result = subprocess.run(command_str, text=True, capture_output =True, shell=True)
    if result.returncode != 0:
        show_alert(result.stderr)
        return

    #in NS1, set ipaddr for device 1 (same for NS2)
    print("set ipaddr 1")
    command_str = "ip netns exec "+str(ns1)+" ip addr add "+str(ip1)+" dev "+str(device1)
    result = subprocess.run(command_str, text=True, capture_output =True, shell=True)
    if result.returncode != 0:
        show_alert(result.stderr)
        return
    print("set ipaddr 2")
    command_str = "ip netns exec "+str(ns2)+" ip addr add "+str(ip2)+" dev "+str(device2)
    result = subprocess.run(command_str, text=True, capture_output =True, shell=True)
    if result.returncode != 0:
        show_alert(result.stderr)
        return

    #set up network interfaces
    print("set up network interface1")
    command_str = "ip netns exec "+str(ns1)+" ifconfig "+str(device1)+" "+str(ip1)+" up"
    result = subprocess.run(command_str, text=True, capture_output =True, shell=True)
    if result.returncode != 0:
        print(result.stderr)
        return
    print("set up network interface2")
    command_str = "ip netns exec "+str(ns2)+" ifconfig "+str(device2)+" "+str(ip2)+" up"
    result = subprocess.run(command_str, text=True, capture_output =True, shell=True)
    if result.returncode != 0:
        print(result.stderr)
        return
    occupied_devices.append(device1)
    occupied_devices.append(device2)

def show_devices(ns_view, ns):
    veths = get_veths(ns)
    for i, veth in enumerate(veths): 
        print("GETTING PEERS for " + veth)
        peer_ns = get_peer(ns, veth)
        print(peer_ns)
        device = Label(ns_view, text= "device " + veth + " is connected to " + peer_ns)
        device.grid(row = i+1, column = 0)

def update_device_list(device1_num, ns1, ns2, ns_view):
    num_veths = len(get_veths(ns1))
    text = "device " + device1_num + " is connected to " + ns2

    ns_btn = Label(ns_view, text=text)
    ns_btn.grid(row = num_veths+1, column = 0)
    
def get_peer(ns, veth):
    peer = None
    command_str = "sudo ip netns exec " + str(ns) + " ethtool -S "+str(veth)+" | awk '/peer_ifindex/ {print $2}'"
    peer_ifindex = int(subprocess.check_output(command_str, shell=True))
    print(ns)

    command_str = "sudo ip netns exec "+str(ns.strip())+" ip link show | grep " +str(peer_ifindex)
    result = subprocess.run(command_str, text=True, capture_output=True, shell=True)
    if(result.returncode != 0):
        show_alert(result.stderr)
        return
    print(result.stdout)
    devices = result.stdout.split('\n')[1:]
    devices = [s.strip() for s in devices if s.strip()]
    print(devices, len(devices))
    for device in devices:
        print(device)
        if "link-netns" in device:
            peer = device.split(' ')[-1]
    return peer
        
def get_ns(ns_name):
    result = subprocess.run("ip netns list", text=True, capture_output =True, shell=True)
    ns_list = result.stdout.split('\n')

    for i, ns in enumerate(ns_list):
        ns_list[i] = ns.split('(id')[0].strip() #clean up outputs

    #list of all namespaces
    ns_list = list(filter(lambda s: s != "", ns_list))
    print(ns_list, ns_name)
    if ns_name in ns_list:
        ns_list.remove(ns_name)
    return ns_list

# def enable_ns_to_host_ip_forwarding(ns1, device1, port1, port2):
#     print("enable_ns_to_host_ip_forwarding")
#     subprocess.run("sysctl -w net.ipv4.ip_forward=1", shell=True)
#     result = subprocess.run("iptables -t nat -A PREROUTING -i "+str(device1)+" -p tcp --dport "+str(port1)+" -j DNAT --to-destination 127.0.0.1:"+str(port2), text= True, capture_output = True, shell=True)
#     if result.returncode != 0:
#         show_alert(result.stderr)
def enable_ns_to_host_ip_forwarding(ns, device, port1, port2):
    subprocess.run("sysctl -w net.ipv4.ip_forward=1", shell=True)
    subprocess.run("iptables -t nat -A PREROUTING -p tcp --dport "+str(port1)+" -j DNAT --to-destination 10.1.1."+str(device)+":"+str(port2)+"", shell=True)
    subprocess.run("iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE", shell=True)
    subprocess.run("ip netns exec "+str(ns)+" nohup python -m http.server "+str(port2)+" > /dev/null 2>&1 &", text=True, capture_output=True, shell=True)

# def enable_ns_to_ns_ip_forwarding(subnet, device1, device2, port1, port2):
#     print(subnet, type(device1), type(device2), port1, port2)
#     print("enable_ns_to_ns_ip_forwarding")
#     ip2 = subnet + device2
#     subprocess.run("sysctl -w net.ipv4.ip_forward=1", shell=True)
#     result = subprocess.run("iptables -t nat -A PREROUTING -i "+str(device1)+" -p tcp --dport "+str(port1)+" -j DNAT --to-destination "+str(ip2)+":"+str(port2), text=True, capture_output=True, shell=True)
#     if result.returncode != 0:
#         show_alert(result.stderr)
#         return

def create_veth_host_to_namespace(ns, device1, device2):
    subprocess.run("ip link add "+str(device1)+" type veth peer name "+str(device2)+"", shell=True)
    subprocess.run("ip link set "+str(device2)+" netns "+str(ns)+"", shell=True)
    subprocess.run("ip addr add 10.1.1."+str(device1)+"/24 dev "+str(device1)+"", shell=True)
    subprocess.run("ip link set dev "+str(device1)+" up", shell=True)
    subprocess.run("ip netns exec "+str(ns)+" ip addr add 10.1.1."+str(device2)+"/24 dev "+str(device2)+"", shell=True)
    subprocess.run("ip netns exec "+str(ns)+" ip link set dev "+str(device2)+" up", shell=True)
    subprocess.run("ip netns exec "+str(ns)+" ip route add default via 10.1.1."+str(device1)+"", shell=True)
# ### TOP 5 PROCESSES ###
# def top_5_cpu():
#     output = subprocess.check_output("ps -eo pid,ppid,%cpu,%mem,cmd --sort=-%cpu | head -n 6", shell=True)
#     cpu = output.decode()
#     return cpu

# def top_5_mem():
#     output = subprocess.check_output("ps -eo pid,ppid,%cpu,%mem --sort=-%mem | head -n 6", shell=True)
#     mem = output.decode()
#     return mem

# def get_cap(ns):
#     output = []
#     output = subprocess.check_output("sudo ip netns exec " + str(ns) + " capsh --print", shell=True)
#     caps = output.decode()
#     return caps

# def get_procs(ns):
#     output = subprocess.check_output("ps u $(ip netns pids " + str(ns) + ")", shell=True)
#     procs = output.decode('utf-8').split('\n')
#     return procs