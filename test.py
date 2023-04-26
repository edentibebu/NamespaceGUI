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
    output = subprocess.check_output("ip netns add" + str(ns_name)+"; ip netns exec "+str(ns_name)+" bash; ip link set dev lo up", shell=True)
    add = output.decode()
    return add

def add_veth(netns, device1, device2):
    output = []
    output = subprocess.check_output("sudo ip link add " + str(device1)+" type veth peer name "+str(device1)+"; sudo ip link set "+str(device2)+" netns " + str(netns), shell=True)
    add = output.decode()
    return add

def set_one_ip(netns, device1, device2, ip):
    #output = subprocess.check_output("sudo ip netns exec "+str(netns)+" ifconfig" +str(device2)+" "+str(ip2)+" up; sudo ifconfig"+str(device1)+" " +str(ip1)+" up; ping "+str(ip2)+"; sudo ip netns exec "+str(netns)+" ping "+str(ip2)+"", shell=True)
    subprocess.check_output("sudo ip addr add "+str(ip)+" dev "+str(device1)+"; sudo ip link set "+str(device1)+" up; sudo ip netns exec "+str(netns)+" ip link set "+str(device2) +" up", shell=True)
    #ips = output.decode()
    #return ips

def set_both_ip(netns, device1, device2, ip1, ip2):
    subprocess.check_output("sudo ip addr add "+str(ip1)+" dev "+str(device1)+"; sudo ip netns exec "+str(netns)+" ip addr add "+str(ip2)+" dev "+str(device2)+"; sudo ip link set "+str(device1)+" up; sudo ip netns exec "+str(netns)+" ip link set "+str(device2)+" up", shell=True)

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
    output = subprocess.check_output("ip netns exec ns1 ss -n -a", shell=True)
    sockets = output.decode()
    print(sockets)
    return sockets

def bridge(bridge):
    output = subprocess.check_output("sudo ip link add name "+str(bridge)+" type bridge", shell=True)
    return output

def list_veth_pairs(ns):
    output = subprocess.check_output("ip netns exec " + str(ns) + "; ip link show type veth", shell=True)
    veth_list = output.decode()
    return veth_list

def port_forward(ns, device1, device2, ip1, ip2, port1, port2):
    output = subprocess.check_output("sudo sysctl -w net.ipv4_forward=1; sudo iptables -t nat -A PREROUTING -p tcp --dport "+str(port1)+" -j DNAT --to-destination "+str(ip1)+ ":"+str(port2)+"", shell=True)
    print("port forwarded")
    return output

def get_veths(ns):
    device_name_1 = subprocess.check_output("sudo ip netns exec "+str(ns)+" ip link show type veth;", shell=True)
    return device_name_1

def get_peer(ns, device):
    peer_ifindex = int(subprocess.check_output("sudo ip netns exec "+str(ns)+" ethtool -S "+str(device)+" | awk '/peer_ifindex/ {print $2}'", shell=True))
    print(peer_ifindex)
    print(type(peer_ifindex))
    device_name_2 = subprocess.check_output("ip netns exec "+str(ns)+" ip link show | grep " +str(peer_ifindex)+"", shell=True)

def create_veth_pairs3():
    subprocess.run("ip link add veth1 type veth peer name veth2", shell=True)
    #subprocess.run("ip link add veth0b type veth peer name veth1b", shell=True)

    subprocess.run("ip link set veth1 netns ns1", shell=True)
    subprocess.run("ip link set veth2  netns ns2", shell=True)

    subprocess.run("ip netns exec ns1 ip addr add 10.1.1.1/24 dev veth1", shell=True)
    subprocess.run("ip netns exec ns2 ip addr add 10.1.1.2/24 dev veth2", shell=True)

    subprocess.run("ip netns exec ns1 ip link set dev veth1 up", shell=True)
    subprocess.run("ip netns exec ns2 ip link set dev veth2 up", shell=True)
    
    
 
#command for getting list of ns within same subnet
#for ns in $(ip netns list | cut -d'(' -f1 | sed 's/\s*//g'); do sudo ip netns exec $ns ip -4 addr show | grep -q '10.1.1.' && echo $ns; done

#command for getting list of subnets within namespace
#sudo ip netns exec "+str(ns)+" ip addr show | grep 'inet ' | awk '{print $2}' | cut -d'/' -f1 | sed 's/\.[0-9]*$/\ /'


def create_veth_host_to_namespace():
    subprocess.run("ip link add veth0 type veth peer name veth1", shell=True)
    #subprocess.run("ip link add veth0b type veth peer name veth1b", shell=True)

    subprocess.run("ip link set veth1 netns myns", shell=True)

    subprocess.run("ip addr add 10.1.1.1/24 dev veth0", shell=True)
    subprocess.run("ip netns exec myns ip addr add 10.1.1.2/24 dev veth1", shell=True)

    subprocess.run("ip link set veth0 up", shell=True)
    subprocess.run("ip netns exec myns ip link set veth1 up", shell=True)

def enable_ns_to_host_ip_forwarding(port1, port2):
    subprocess.run("sysctl -w net.ipv4.ip_forward=1", shell=True)
    subprocess.check_output("iptables -t nat -A OUTPUT -p tcp --dport "+str(port1)+" -j DNAT --to-destination 127.0.0.1:"+str(port2)+"", shell=True)


def enable_ns_to_ns_ip_forwarding(device1, port1, port2, ip1, ip2):
    subprocess.run("sysctl -w net.ipv4.ip_forward=1", shell=True)
    subprocess.check_output("iptables -t nat -A PREROUTING -i "+str(device1)+" -p tcp --dport "+str(port1)+" -j DNAT --to-destination "+str(ip2)+":"+str(port2)+"", shell=True)

def enable_ns_to_ns_ip_forwarding_copy():
    subprocess.run("sysctl -w net.ipv4.ip_forward=1", shell=True)
    subprocess.check_output("iptables -t nat -A PREROUTING -i veth1 -p tcp --dport 80 -j DNAT --to-destination 10.1.1.2:8080", shell=True)


def run_python_server(ns2, port2):
    subprocess.run("ip netns exec "+str(ns2)+" python -m http.server "+str(port2)+"", shell=True)

def verify_ns_to_ns_port_forwarding(ns1, device2, port2):
    subprocess.run("ip netns exec "+str(ns1)+" lynx http://10.1.1."+str(device2)+":"+str(port2)+"", shell=True)

#get_peer()

#create_veth_pairs3()
#enable_ns_to_ns_ip_forwarding_copy()

#create_veth_pairs3()
#enable_ip_forwarding()

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

#port_forward()
#top_5_cpu()
# remove_cap()
# get_namespaces()
# get_cap()
# add_ns()
# delete_ns()
# get_procs()
# set_ips()
