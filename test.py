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

def add_ns():
    output = []
    NS = "added"
    output = subprocess.check_output("ip netns add added", shell=True)
    add = output.decode()
    return add

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

def top_5_cpu():
    output = subprocess.check_output("ps -eo pid,ppid,%cpu,%mem,cmd --sort=-%cpu | head -n 6", shell=True)
    cpu = output.decode()
    print(cpu)
    return cpu

def top_5_mem():
    output = subprocess.check_output("ps -eo pid,ppid,%cpu,%mem --sort=-%mem | head -n 6", shell=True)
    mem = output.decode()
    print(mem)
    return mem

# top_5_mem()


# top_5_cpu()
# remove_cap()
# get_namespaces()
# get_cap()
# add_ns()
# delete_ns()
get_procs()
