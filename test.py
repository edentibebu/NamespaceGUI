from ctypes import *
import os

cwd = os.getcwd()
rel_path = os.path.join(cwd, "list.so")
so_file = rel_path
my_functions = CDLL(so_file) 

def get_namespaces():
    namespaces = my_functions.list()
    return namespaces