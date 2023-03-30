from ctypes import *
so_file = "home/pi/list.so"
my_functions = CDLL(so_file) 

my_functions.list()
