from cgi import test
from re import sub
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

def list_namespaces(root, namespace_frame):
    # get namespaces as list from C code
    net_ns = get_net_namespaces()
    net_ns_list = net_ns.split('\n')[:-1]

    for i, ns in enumerate(net_ns_list):
        ns_btn = Button(namespace_frame, text=ns, command=lambda ns=ns: ns_view.NSView(root, ns))
        ns_btn.grid(row = i+1, column = 0)
### ADD NS WINDOW ###
def add_ns(ns_name):
    command_str = "ip netns add " + str(ns_name)
    result = subprocess.run(command_str, text = True, stderr=subprocess.PIPE, shell=True)
    if result.returncode != 0:
        show_alert(result.stderr)
    ## Adding Loopback
    command_str = 'ip netns exec ' + str(ns_name) + ' ip link set dev lo up'
    result = subprocess.run(command_str, text = True, stderr=subprocess.PIPE, shell=True)
    if result.returncode != 0:
        show_alert(result.stderr)

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

def update_ns_list(ns_name, net_namespace_frame, root):
    net_ns = get_net_namespaces()
    num_ns = len(net_ns.split('\n')[:-1])
    ns_btn = Button(net_namespace_frame, text=ns_name, command=lambda ns=ns_name: ns_view.NSView(root, ns_name))
    ns_btn.grid(row = num_ns+1, column = 0)

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

def bridge(bridge):
    output = subprocess.check_output("sudo ip link add name "+str(bridge)+" type bridge", shell=True)
    return output

def get_veths(ns):
    command_str = "sudo ip netns exec "+str(ns)+"; ip link show type veth;"
    result = subprocess.run(command_str, text = True, capture_output=True, shell=True)
    if result.returncode != 0:
        show_alert(result.stderr)
        return
    print(result.stdout)

def create_veth_pairs(ns1, ns2, device1, device2, ip1, ip2):
    print("creating dev pair")
    print(device1, device2)
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
#def update_device_list():

    
# def get_peer(veth):
#     command_str = 'ip link show ' + str(veth) + " | grep peer"
#     result = subprocess.run(command_str, text=True, stderr = subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
#     if(result.returncode != 0):
#         show_alert(result.stderr)
#     else:
#         print(result.stdout)
        
def get_ns(ns_name):
    result = subprocess.run("ip netns list", text=True, capture_output =True, shell=True)
    ns_list = result.stdout.split('\n')

    for i, ns in enumerate(ns_list):
        ns_list[i] = ns.split('(id')[0] #clean up outputaa

    #list of all namespaces
    ns_list = list(filter(lambda s: s != "", ns_list))
    ns_list.remove(ns_name)
    return ns_list

def port_forward(ns, device1, device2, ip1, ip2, port1, port2):
    output = subprocess.check_output("sudo sysctl -w net.ipv4_forward=1; sudo iptables -t nat -A PREROUTING -p tcp --dport "+str(port1)+" -j DNAT --to-destination "+str(ip1)+ ":"+str(port2)+"", shell=True)
    print("port forwarded")
    return output



### TOP 5 PROCESSES ###
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
