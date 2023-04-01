from tkinter import *
import tkinter as tk
from tkinter import ttk
from ctypes import *
import subprocess
import os
from unicodedata import name

root = Tk()
root.title("Namespace GUI: Home")

# list of all capabilities
all_caps = [{'cap': 'CAP_AUDIT_CONTROL', 'enabled': False},  {'cap': 'CAP_AUDIT_READ', 'enabled': False}, {'cap': 'CAP_AUDIT_WRITE', 'enabled': False}, 
            {'cap': 'CAP_BLOCK_SUSPEND', 'enabled': False}, {'cap': 'CAP_BPF', 'enabled': False}, {'cap': 'CAP_CHECKPOINT_RESTORE', 'enabled': False}, 
            {'cap': 'CAP_CHOWN', 'enabled': False}, {'cap': 'CAP_DAC_OVERRIDE', 'enabled': False}, {'cap': 'CAP_DAC_READ_SEARCH', 'enabled': False}, 
            {'cap': 'CAP_FOWNER', 'enabled': False}, {'cap': 'CAP_FSETID', 'enabled': False}, {'cap': 'CAP_IPC_LOCK', 'enabled': False},
            {'cap': 'CAP_IPC_OWNER', 'enabled': False}, {'cap': 'CAP_KILL', 'enabled': False}, {'cap': 'CAP_LEASE', 'enabled': False}, 
            {'cap': 'CAP_LINUX_IMMUTABLE', 'enabled': False}, {'cap': 'CAP_MAC_ADMIN', 'enabled': False}, {'cap': 'CAP_MAC_OVERRIDE', 'enabled': False}, 
            {'cap': 'CAP_MKNOD', 'enabled': False}, {'cap': 'CAP_NET_ADMIN', 'enabled': False}, {'cap': 'CAP_NET_BIND_SERVICE', 'enabled': False},
            {'cap': 'CAP_NET_BROADCAST', 'enabled': False}, {'cap': 'CAP_NET_RAW', 'enabled': False}, {'cap': 'CAP_PERFMON', 'enabled': False},
            {'cap': 'CAP_SETGID', 'enabled': False}, {'cap': 'CAP_SETFCAP', 'enabled': False}, {'cap': 'CAP_SETPCAP', 'enabled': False}, 
            {'cap': 'CAP_SETUID', 'enabled': False}, {'cap': 'CAP_SYS_ADMIN', 'enabled': False}, {'cap': 'CAP_SYS_BOOT', 'enabled': False}, 
            {'cap': 'CAP_SYS_BOOT', 'enabled': False}, {'cap': 'CAP_SYS_CHROOT', 'enabled': False}, {'cap': 'CAP_SYS_MODULE', 'enabled': False},
            {'cap': 'CAP_SYS_NICE', 'enabled': False}, {'cap': 'CAP_SYS_PACCT', 'enabled': False}, {'cap': 'CAP_SYS_PTRACE', 'enabled': False}, 
            {'cap': 'CAP_SYS_RAWIO', 'enabled': False}, {'cap':'CAP_SYS_RESOURCE', 'enabled': False}, {'cap': 'CAP_SYS_TIME', 'enabled': False},
            {'cap': 'CAP_SYS_TTY_CONFIG', 'enabled': False}, {'cap': 'CAP_SYSLOG', 'enabled': False}, {'cap': 'CAP_WAKE_ALARM', 'enabled': False}]

#namespace_heading = Label(root, text="Namespaces")
#namespace_heading.pack()

############################ INTERFACING WITH PI #################################
def get_namespaces():
    output = []
    output = subprocess.check_output("ip netns", shell=True)

    namespaces = output.decode()
    return namespaces

def get_cap(ns):
    output = []
    output = subprocess.check_output("sudo ip netns exec " + str(ns) + " capsh --print", shell=True)
    caps = output.decode()
    return caps

########################### WINDOWS #####################################
#new window to add namespace on click of add-ns button
def add_ns_window():
        add_ns_window = Toplevel(root)
        add_ns_window.title("Add New Namespace")
        Label(add_ns_window, text ="Window to add a namespace").pack()

#new window to view a namespace (on click of namespace name)
def ns_view(ns): #passing in ns name
    #TODO: make this page scrollable!!
    ns_view = Toplevel(root)
    #ns_view = tk.Canvas(root)
    ns_view.title("Namespace GUI: Namespace View")
    #scrollbar = ttk.Scrollbar(root, orient="vertical", command=ns_view.yview)

    ns_header = Label(ns_view, text=ns)
    ns_header.pack() #TODO : fix placement?? 
    #creating frames
    cap_frame = LabelFrame(ns_view, text=ns, padx=5, pady=5)
    cap_frame.grid(row = 0, column = 0, padx=10, pady=10)

    process_frame = LabelFrame(ns_view, text="Processes", padx=5, pady=5)
    process_frame.grid(row=0, column=1, padx=50, pady = 10)

    # get capabilities for this namespace with C code
    output = get_cap(ns)
    caps = output.split("\n")
    capabilities = caps[1].split('=')[1]
    cap_list = capabilities.split(',')
    print(len(cap_list))
    #TODO: enable capabilities that are returned in cap_list
    # prob need another for loop to do that???? 
    for i, cap in all_caps:
        if cap['enabled']:
            color = '0f0' # green for enabled
        else:
            color = 'f00' # red for disabled
        cap_label = Label(cap_frame, text = cap['cap'], fg = color)
        cap_label.grid(row=i, column=0, padx=5, pady=5)
        cap_en = IntVar() ## this will be used for making changes to the capabilities, enforced on "save"
        toggle = Checkbutton(cap_frame, text="enable", variable=cap_en)
        toggle.grid(row=i, column=1, padx=20, pady=5)
    # for i, cap in enumerate(cap_list):

    #     cap = Label(cap_frame, text=cap)
    #     cap.grid(row=i, column=0, padx=5, pady=5)
    #     cap_en = IntVar() #set up a list of IntVar(), corresponding with each cap
    #     #TODO: add 
    #     toggle = Checkbutton(cap_frame, text="enable", variable=cap_en) 
    #     toggle.grid(row=i, column=1, padx=20, pady= 5)

    #TODO: iterate through list of processes
    proc = Label(process_frame, text=("Processes in" + ns)) #TODO: get namespace name and insert here
    proc.grid(row=0, column=0)

##################################### FRAMES #########################################
#creating frames
namespace_frame = LabelFrame(root, text="Namespaces", padx=5, pady=5)
#namespace_frame.pack()
namespace_frame.grid(row = 0, column = 0, padx=10, pady=10)

process_frame = LabelFrame(root, text="Processes", padx=5, pady=5)
#process_frame.pack()
process_frame.grid(row=0, column=1, padx=50, pady = 10)

################################## List namespaces ##################################
# get namespaces as list from C code
namespaces = get_namespaces()
print("Got namespaces! they are : ")
ns_list = namespaces.split('\n')[:-1]

#ns_list = ['ns1', 'ns2']

for i, ns in enumerate(ns_list):
    ns_btn = Button(namespace_frame, text=ns, command=lambda ns=ns: ns_view(ns)) #TODO: clicking on button brings up NS-view.py for editing
    ns_btn.grid(row = i+1, column = 0) # TODO: row will change for each namespace, column will not. add padding around text


############################### Home 
add_ns_btn = Button(namespace_frame, text="Add Namespace", command = add_ns_window)
add_ns_btn.grid(row=0, column=1)

#TODO: List processes
# get processes as list from C code
# for proc in processes:
proc = Label(process_frame, text="process1")
proc.grid(row=0, column=0)

root.mainloop()