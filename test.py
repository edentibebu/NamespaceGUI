from ctypes import *
so_file = "/list.so"
my_functions = CDLL(so_file) 

my_functions.list()