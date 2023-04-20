from ctypes import *
import subprocess
import os


# this function lists the existing namespaces
def get_namespaces():
    output = []
    output = subprocess.check_output("ip netns", shell=True)

    namespaces = output.decode()
    print(namespaces)
    print(type(namespaces))
    return namespaces

def get_cap(): 
    output = []
    NS = "testing"
    output = subprocess.check_output("sudo ip netns exec testing capsh --print", shell=True)
    caps = output.decode()
    print(caps)
    return caps

def add_ns(ns_name):
    output = []
    NS = "added"
    output = subprocess.check_output("ip netns add" + str(ns_name), shell=True)
    add = output.decode()
    return add

def add_veth(netns, device1, device2):
    ouput = []
    device1 = "veth0"
    device2 = "veth1"
    output = subprocess.check_output("sudo ip link add" +str(device1) +"type veth peer name" +str(device2)+"; sudo ip link set" +str(device2)+" netns "+str(netns)+"", shell=True)
    add = output.decode()
    return add

def set_ips(netns, device1, device2):
    output = []
    ip1 = "10.1.1.1"
    ip2 = "10.1.1.2"
    output = subprocess.check_output("sudo ip netns exec "+str(netns)+" ifconfig" +str(device2)+" "+str(ip2)+" up; sudo ifconfig"+str(device1)+" " +str(ip1)+" up; ping "+str(ip2)+"; sudo ip netns exec "+str(netns)+" ping "+str(ip2)+"", shell=True)
    ips = output.decode()
    return ips

def delete_ns():
    output = []
    NS = "deleted"
    output = subprocess.check_output("ip netns delete deleted", shell=True)
    delete = output.decode()
    return delete

def remove_cap():
    output = []
    network = subprocess.check_output("sudo ip netns exec newns setcap -r /home/eden/NamespaceGUI cap_perfmon+ep", shell=True)
    #  "sudo lsns -t net | grep testing | awk '{print $1}'", shell=True)
    ID = network
    # print(ID)
    # output = subprocess.check_output("sudo setcap -r CAP_SYS_TIME+ep /proc/"+ str(ID) +"/ns/net", shell=True)
    # remove = output.decode()
    return ID

def get_procs():
    output = subprocess.check_output("ps u $(ip netns pids testing)", shell=True)
    procs = output.decode()
    print(output)
    return procs

def top_5_cpu(ns):
    output = subprocess.check_output("ip netns exec "+str(ns)+" ps -eo pid,ppid,%cpu,%mem,cmd --sort=-%cpu | head -n 6", shell=True)
    cpu = output.decode()
    print(cpu)
    return cpu

def top_5_mem(ns):
    output = subprocess.check_output("ip netns exec "+str(ns)+" ps -eo pid,ppid,%cpu,%mem --sort=-%mem | head -n 6", shell=True)
    mem = output.decode()
    print(mem)
    return mem

def disp_routing():
    output = subprocess.check_output("ip netns exec ns1 route", shell=True)
    routes = output.decode()
    print(routes)
    return routes

def list_sockets():
    output = subrocess.check_output("ip netns exec ns1 ss -n -a", shell=True)
    sockets = output.decode()
    print(sockets)
    return sockets

def bridge(bridge):
    output = subprocess.check_output("sudo ip link add name "+str(bridge)+" type bridge", shell=True)
    return output

def list_veth_pairs():
    output = subprocess.check_output("ip link", shell=True)
    veth_list = output.decode()
    return veth_list

def port_forward(ns, device1, device2, ip1, ip2, port1, port2):
    output = subprocess.check_output("sudo sysctl -w net.ipv4_forward=1; sudo iptables -t nat -A PREROUTING -p tcp --dport "+str(port1)+" -j DNAT --to-destination "+str(ip1)+ ":"+str(port2)+"", shell=True)
    print("port forwarded")
    return output


#def tcp():
#   port = "7096"
#    ns1 = "1"
#    ns2 = "2"
#    ip = "10.1.1.1"
#    output = subprocess.check_output("ip netns exec "+str(ns1)+" nc -l "+str(ip)+" "+str(port)+" -v", shell=True)
    # open another terminal to connect second namespace to first
    # then run command to allow communication between two namespaces
    # show messages sent
    # possibly show tcpdump to grab all packets transmitted between two namespaces

# forward traffic using ports
# window to show port forwarding worked (html)

# top_5_mem()

port_forward()
#top_5_cpu()
# remove_cap()
# get_namespaces()
# get_cap()
# add_ns()
# delete_ns()
# get_procs()
# set_ips()
