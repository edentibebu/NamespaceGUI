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
    output = subprocess.check_output("sudo setcap -r testing", shell=True)
    remove = output.decode()
    return remove

def get_procs():
    output = subprocess.check_output("ps u $(ip netns pids testing)", shell=True)
    procs = output.decode()
    return procs

# remove_cap()
# get_namespaces()
# get_cap()
# add_ns()
# delete_ns()
# get_procs()
