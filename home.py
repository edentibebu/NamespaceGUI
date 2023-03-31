from tkinter import *
from ctypes import *
import subprocess
import os
from unicodedata import name

root = Tk()
root.title("Namespace GUI: Home")

#namespace_heading = Label(root, text="Namespaces")
#namespace_heading.pack()

def get_namespaces():
    output = []
    output = subprocess.check_output("ip netns", shell=True)

    namespaces = output.decode()
    return namespaces

#new window to add namespace on add-ns button
def add_ns_window():
        add_ns_window = Toplevel(root)
        add_ns_window.title("Add New Namespace")
        Label(add_ns_window, text ="Window to add a namespace").pack()

#new window to view a namespace (on click of namespace name)
def ns_view(): #TODO: pass in namespace name
    ns_view = Toplevel(root)
    ns_view.title("Namespace GUI: Namespace View")
    ns_header = Label(ns_view, text="Namespace Name") #TODO: pass in namespace name somehow and print it here

    #creating frames
    cap_frame = LabelFrame(ns_view, text="Namespaces", padx=5, pady=5)
    #namespace_frame.pack()
    cap_frame.grid(row = 0, column = 0, padx=10, pady=10)

    process_frame = LabelFrame(ns_view, text="Processes", padx=5, pady=5)
    process_frame.grid(row=0, column=1, padx=50, pady = 10)

    # TODO: get capabilities for this namespace with C code
    cap = Label(cap_frame, text="capability 1")
    cap.grid(row=0, column=0, padx=5, pady=5)
    cap_en = IntVar() #set up a list of IntVar(), corresponding with each cap
    toggle = Checkbutton(cap_frame, text="enable", variable=cap_en) 
    toggle.grid(row=0, column=1, padx=20, pady= 5)

    #TODO: iterate through list of processes
    proc = Label(process_frame, text="Processes in [Namespace Name]" ) #TODO: get namespace name and insert here
    proc.grid(row=0, column=0)


#creating frames
namespace_frame = LabelFrame(root, text="Namespaces", padx=5, pady=5)
#namespace_frame.pack()
namespace_frame.grid(row = 0, column = 0, padx=10, pady=10)

process_frame = LabelFrame(root, text="Processes", padx=5, pady=5)
#process_frame.pack()
process_frame.grid(row=0, column=1, padx=50, pady = 10)

#TODO: List namespaces
# get namespaces as list from C code
namespaces = get_namespaces()
print("Got namespaces! they are : ")
ns_list = namespaces.split('\n')

#ns_list = ['ns1', 'ns2']

for i, ns in enumerate(ns_list):
    ns_btn = Button(namespace_frame, text=ns) #TODO: clicking on button brings up NS-view.py for editing
    print(type(ns))
    ns_btn.grid(row = i+1, column = 0) # TODO: row will change for each namespace, column will not. add padding around text
# 
add_ns_btn = Button(namespace_frame, text="Add Namespace", command = add_ns_window)
add_ns_btn.grid(row=0, column=1)

#TODO: List processes
# get processes as list from C code
# for proc in processes:
proc = Label(process_frame, text="process1")
proc.grid(row=0, column=0)

root.mainloop()