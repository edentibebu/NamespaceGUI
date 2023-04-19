from re import L
from tkinter import *
import tkinter as tk
from tkinter import ttk
from ctypes import *
import subprocess
import os
from unicodedata import name

root = Tk()
root.title("Namespace GUI: Home")
checkuid = subprocess.check_output("id -u", shell=True).decode()


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
            {'cap': 'CAP_SYS_CHROOT', 'enabled': False}, {'cap': 'CAP_SYS_MODULE', 'enabled': False}, {'cap': 'CAP_SYS_NICE', 'enabled': False}, 
            {'cap': 'CAP_SYS_PACCT', 'enabled': False}, {'cap': 'CAP_SYS_PTRACE', 'enabled': False}, {'cap': 'CAP_SYS_RAWIO', 'enabled': False},
            {'cap':'CAP_SYS_RESOURCE', 'enabled': False}, {'cap': 'CAP_SYS_TIME', 'enabled': False}, {'cap': 'CAP_SYS_TTY_CONFIG', 'enabled': False}, 
            {'cap': 'CAP_SYSLOG', 'enabled': False}, {'cap': 'CAP_WAKE_ALARM', 'enabled': False}]
#namespace_heading = Label(root, text="Namespaces")
#namespace_heading.pack()

############################ INTERFACING WITH PI #################################
def get_net_namespaces():
    output = []
    if(checkuid[0] == '0'):
        output = subprocess.check_output("sudo ip netns", shell=True)
    else:
        output = subprocess.check_output('ip netns', shell=True)

    net_namespaces = output.decode()
    return net_namespaces

def get_user_namespaces():
    output = []
    if (checkuid[0] == "0"):
        output = subprocess.check_output("sudo lsns -l -n --type user", shell=True)
    else:
        output = subprocess.check_output("lsns -l -n --type user", shell=True)

    user_namespaces = output.decode()
    #print ("userns output type: ", type(user_namespaces))
    return user_namespaces

def get_mount_namespaces():
    output = []
    if (checkuid[0] == "0"):
        output = subprocess.check_output("sudo lsns --type mnt", shell=True)
    else:
        output = subprocess.check_output("lsns --type mnt", shell=True)

    mount_namespaces = output.decode()
    return mount_namespaces

def get_proc_namespaces():
    output = []
    if (checkuid[0] == "0"):
        output = subprocess.check_output("sudo lsns --type pid", shell=True)
    else:
        output = subprocess.check_output("lsns --type pid", shell=True)

    proc_namespaces = output.decode()
    return proc_namespaces
    
def get_uts_namespaces():
    output = []
    if (checkuid[0] == "0"):
        output = subprocess.check_output("sudo lsns --type uts", shell=True)
    else:
        output = subprocess.check_output("lsns --type uts", shell=True)

    uts_namespaces = output.decode()
    return uts_namespaces

def get_ipc_namespaces():
    output = []
    if (checkuid[0] == "0"):
        output = subprocess.check_output("sudo lsns --type ipc", shell=True)
    else:
        output = subprocess.check_output("lsns --type ipc", shell=True)

    ipc_namespaces = output.decode()
    return ipc_namespaces

def top_5_cpu():
    output = subprocess.check_output("ps -eo pid,ppid,%cpu,%mem,cmd --sort=-%cpu | head -n 6", shell=True)
    cpu = output.decode()
    return cpu

def top_5_mem():
    output = subprocess.check_output("ps -eo pid,ppid,%cpu,%mem --sort=-%mem | head -n 6", shell=True)
    mem = output.decode()
    return mem

def get_cap(ns):
    output = []
    output = subprocess.check_output("sudo ip netns exec " + str(ns) + " capsh --print", shell=True)
    caps = output.decode()
    return caps

def get_procs(ns):
    output = subprocess.check_output("ps u $(ip netns pids " + str(ns) + ")", shell=True)
    procs = output.decode('utf-8').split('\n')
    return procs

def add_ns(ns_name):
    subprocess.check_output("ip netns add " + str(ns_name), shell=True)

def add_veth(netns, device1, device2):
    ouput = []
    device1 = "veth0"
    device2 = "veth1"
    subprocess.check_output("sudo ip link add " +str(device1) +" type veth peer name " +str(device2)+"; sudo ip link set " +str(device2)+" netns "+str(netns), shell=True)

def set_ips(netns, device1, device2, ip1, ip2):
    subprocess.check_output("sudo ip netns exec "+str(netns)+" ifconfig " +str(device2)+" "+str(ip2)+" up; sudo ifconfig "+str(device1)+" " +str(ip1)+" up; ping "+str(ip2)+"; sudo ip netns exec "+str(netns)+" ping "+str(ip2), shell=True)
    # ips = output.decode()
    # return ips
########################### WINDOWS #####################################
# alert window, can be used for various errors
def show_alert(message):
    alert_window = Toplevel()
    alert_window.title("Alert")
    alert_label = Label(alert_window, text=message)
    alert_label.pack(padx=20, pady=20)
    ok_button = Button(alert_window, text="OK", command=alert_window.destroy)
    ok_button.pack(pady=10)

#new window to add namespace on click of add-ns button
def add_net_ns(ns_name, device1, device2, ip1, ip2):
    ns_name = ns_name.get()
    device1 = device1.get()
    device2 = device2.get()
    ip1 = ip1.get()
    ip2 = ip2.get()
    if ns_name:
        add_ns(ns_name)
        print("adding: " , ns_name)
    else:
        show_alert("you must specify the namespace name in order to add a network namespace.")
    if device1 and device2:
        print("adding Veth pairs")
        add_veth(ns_name, device1, device2)
    if device1 and device2 and ip1 and ip2:
        set_ips(ns_name, device1, device2, ip1, ip2)

def add_net_ns_window():
    add_net_ns_window = Toplevel(root)
    add_net_ns_window.title("Add New Network Namespace")
    if(checkuid[0] == "0"):
        Label(add_net_ns_window, text ="Name:").grid(row=0, column=0)
        ns_name = Entry(add_net_ns_window)
        ns_name.grid(row=0, column=1)

        #TODO: add functionality to make placeholder text grey that goes away after clicking in cell
        
        Label(add_net_ns_window, text ="VEth Pairs:").grid(row=2, column=0)
        Label(add_net_ns_window, text ="Device 1:").grid(row=1, column=1)
        Label(add_net_ns_window, text ="Device 1:").grid(row=1, column=2)
        device1 = Entry(add_net_ns_window)
        device1.grid(row=2, column=1)
        device2 = Entry(add_net_ns_window)
        device2.grid(row=2, column=2)

        Label(add_net_ns_window, text ="IP Addresses:").grid(row=4, column=0)
        Label(add_net_ns_window, text ="Address 1:").grid(row=3, column=1)
        Label(add_net_ns_window, text ="Address 2:").grid(row=3, column=2)

        ip1 = Entry(add_net_ns_window)
        ip1.grid(row=4, column=1)
        ip2 = Entry(add_net_ns_window)
        ip2.grid(row=4, column=2)

        #ns_name_text = ns_name.get()
        #print(ns_name_text)
        add_ns_btn = Button(add_net_ns_window, text='Submit', command = lambda: add_net_ns(ns_name, device1, device2, ip1, ip2))
        add_ns_btn.grid(row=5, column=4)
        
    else:
        Label(add_net_ns_window, text = "Sorry, you cannot access this window because you do not have root privileges").pack()

def add_user_ns_window():
        add_user_ns_window = Toplevel(root)
        checkuid = subprocess.check_output("id -u", shell=True).decode()
        add_user_ns_window.title("Add New User Namespace")
        if(checkuid[0] == "0"):
            Label(add_user_ns_window, text ="Window to add a namespace").pack()
        else:
            Label(add_user_ns_window, text = "Sorry, you cannot access this window because you do not have root privileges").pack()

def add_mount_ns_window():
        add_mount_ns_window = Toplevel(root)
        add_mount_ns_window.title("Add New Mount Namespace")
        if(checkuid[0] == "0"):
            Label(add_mount_ns_window, text ="Window to add a namespace").pack()
        else:
            Label(add_mount_ns_window, text = "Sorry, you cannot access this window because you do not have root privileges").pack()

def add_proc_ns_window():
        add_proc_ns_window = Toplevel(root)
        checkuid = subprocess.check_output("id -u", shell=True).decode()
        add_proc_ns_window.title("Add New Network Namespace")
        if(checkuid[0] == "0"):
            Label(add_proc_ns_window, text ="Window to add a namespace").pack()
        else:
            Label(add_proc_ns_window, text = "Sorry, you cannot access this window because you do not have root privileges").pack()

def add_uts_ns_window():
        add_uts_ns_window = Toplevel(root)
        checkuid = subprocess.check_output("id -u", shell=True).decode()
        add_uts_ns_window.title("Add New Network Namespace")
        if(checkuid[0] == "0"):
            Label(add_uts_ns_window, text ="Window to add a namespace").pack()
        else:
            Label(add_uts_ns_window, text = "Sorry, you cannot access this window because you do not have root privileges").pack()

def add_ipc_ns_window():
        add_ipc_ns_window = Toplevel(root)
        checkuid = subprocess.check_output("id -u", shell=True).decode()
        add_ipc_ns_window.title("Add New Network Namespace")
        if(checkuid[0] == "0"):
            Label(add_ipc_ns_window, text ="Window to add a namespace").pack()
        else:
            Label(add_ipc_ns_window, text = "Sorry, you cannot access this window because you do not have root privileges").pack()


#new window to view a namespace (on click of namespace name)
def net_ns_view(ns): #passing in ns name
    #TODO: make this page scrollable!!
    ns_view = Toplevel(root)
    #ns_view = tk.Canvas(root)
    ns_view.title("Namespace GUI: Namespace View")
    #scrollbar = ttk.Scrollbar(root, orient="vertical", command=ns_view.yview)
    checkuid = subprocess.check_output("id -u", shell = True).decode()

    if(checkuid[0] != "0"):
        Label(ns_view, text = "Sorry, you cannot access this window because you do not have root privileges").pack()
        return

    net_ns_header = Label(ns_view, text=ns)
    #ns_header.pack() #TODO : fix placement?? 
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
    cap_list = [cap.upper() for cap in cap_list]

    cap_en  = IntVar()
    for i, cap in enumerate(all_caps):
        if(cap['cap'] in cap_list):
            cap['enabled'] = True
        if cap['enabled']:
            color = '#0f0' # green for enabled
        else:
            color = '#f00' # red for disabled
        cap_label = Label(cap_frame, text = cap['cap'], fg = color)
        cap_label.grid(row=i, column=0, padx=5, pady=5)
        cap_en.set(int(cap['enabled'])) ## this will be used for making changes to the capabilities, enforced on "save"
        toggle = Checkbutton(cap_frame, text="enable", variable=cap_en)
        toggle.grid(row=i, column=1, padx=20, pady=5)

    #TODO: iterate through list of processes
    procs = get_procs(ns)

    header = procs[0].split(' ')
    body = procs[1:]
    for i, line in enumerate(body):
        line = line.split(' ')
        row = []
        for element in line:
            element = element.strip()
            if element:
                row.append(element)
        if(row):
            body[i] = row    
    columns = []
    for col in header:
        col = col.strip()
        if(col):
            columns.append(col)

    
    proc_table = ttk.Treeview(process_frame, columns = columns)
    for col in columns: 
        proc_table.heading(col, text=col)


    ### PROC TABLE ###
    # populate the table: #TODO: values are not lined up with the correct columns
    for i, line in enumerate(body):
        # print(line, type(line))
        proc_table.insert(parent='', index='end', iid = i, text='', values = line)
    proc_table.grid(row = 0, column = 1)
    # procs[0] is header for table
    for i, proc in enumerate(procs):
        proc_label = Label(process_frame, text=(proc)) #TODO: get namespace name and insert here
        #proc_label.grid(row=i, column=0)

    # TODO : Remove namespace button

    


##################################### FRAMES #########################################
#creating frames
net_namespace_frame = LabelFrame(root, text="Network Namespaces", padx=5, pady=5)
net_namespace_frame.grid(row = 0, column = 0, padx=10, pady=10)

user_namespace_frame = LabelFrame(root, text="User Namespaces", padx=5, pady=5)
user_namespace_frame.grid(row = 0, column = 1, padx=10, pady=10)

mount_namespace_frame = LabelFrame(root, text="Mount Namespaces", padx=5, pady=5)
mount_namespace_frame.grid(row = 0, column = 2, padx=10, pady=10)

proc_namespace_frame = LabelFrame(root, text="Process Namespaces", padx=5, pady=5)
proc_namespace_frame.grid(row = 1, column = 0, padx=10, pady=10)

uts_namespace_frame = LabelFrame(root, text="UTS Namespaces", padx=5, pady=5)
uts_namespace_frame.grid(row = 1, column = 1, padx=10, pady=10)

ipc_namespace_frame = LabelFrame(root, text="Process Namespaces", padx=5, pady=5)
ipc_namespace_frame.grid(row = 1, column = 2, padx=10, pady=10)

process_cpu_frame = LabelFrame(root, text="Top CPU Processes", padx=5, pady=5)
process_cpu_frame.grid(row=2, column=0, padx=50, pady = 10)

process_mem_frame = LabelFrame(root, text="Top Memory Processes")
process_mem_frame.grid(row=2, column=0, padx=50, pady=10)

################################## List namespaces ##################################
# get namespaces as list from C code
net_ns = get_net_namespaces()
net_ns_list = net_ns.split('\n')[:-1]

user_ns = get_user_namespaces()
#print(user_ns)

#print(get_user_namespaces())

#ns_list = ['ns1', 'ns2']

for i, ns in enumerate(net_ns_list):
    ns_btn = Button(net_namespace_frame, text=ns, command=lambda ns=ns: net_ns_view(ns)) #TODO: clicking on button brings up NS-view.py for editing
    ns_btn.grid(row = i+1, column = 0) # TODO: row will change for each namespace, column will not. add padding around text

############################### Home #######################

add_ns_btn = Button(net_namespace_frame, text="+", command = add_net_ns_window)
add_ns_btn.grid(row=0, column=1)

#TODO: List processes

mem_procs = top_5_mem()
cpu_procs = top_5_cpu().split('\n')

# print((cpu_procs), type(cpu_procs))
cpu_header_list = cpu_procs[0].split(' ')

# for i, proc in enumerate(cpu_procs):
#     #print(proc)
#     proc_label = Label(process_cpu_frame, text=proc)
#     proc_label.grid(row=i, column=0)

#proc = Label(process_frame, text="process1")
#proc.grid(row=0, column=0)

root.mainloop()
