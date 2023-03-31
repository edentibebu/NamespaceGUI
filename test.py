from ctypes import *
import subprocess
import os


cwd = os.getcwd()
rel_path = os.path.join(cwd, "list.so")
so_file = rel_path
my_functions = CDLL(so_file) 

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
    output = subprocess.check_output("ip netns exec"+ NS +"capsh --print", shell=True)
    caps = output.decode()
    print(caps)
    return caps

get_cap()






#get_namespaces()