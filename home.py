from re import L
from tkinter import *
from tkinter import ttk
from ctypes import *
import subprocess
import os

import add_net_ns
import utils

root = Tk()
root.title("Namespace GUI: Home")


#namespace_heading = Label(root, text="Namespaces")
#namespace_heading.pack()

############################ INTERFACING WITH PI #################################

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

# def add_ns(ns_name):
#     command_str = "ip netns add " + str(ns_name)
#     result = subprocess.run(command_str, text = True, stderr=subprocess.PIPE, shell=True)
#     if result.returncode != 0:
#         show_alert(result.stderr)
# def add_veth(netns, device1, device2):
#     command_str = "sudo ip link add " +str(device1) +" type veth peer name " +str(device2)+"; sudo ip link set " +str(device2)+" netns "+str(netns)
#     result = subprocess.run((command_str), text=True, stderr=subprocess.PIPE, shell=True)
#     if result.returncode != 0:
#         show_alert(result.stderr)
# def set_ips(netns, device1, device2, ip1, ip2):
#     subprocess.check_output("sudo ip netns exec "+str(netns)+" ifconfig " +str(device2)+" "+str(ip2)+" up; sudo ifconfig "+str(device1)+" " +str(ip1)+" up; ping "+str(ip2)+"; sudo ip netns exec "+str(netns)+" ping "+str(ip2), shell=True)
    # ips = output.decode()
    # return ips
########################### WINDOWS #####################################

def add_net_ns_window(net_namespace_frame):
    add_net_ns_window = Toplevel(root)
    add_net_ns_window.title("Add New Network Namespace")
    if(utils.checkuid[0] == "0"):
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

        add_ns_btn = Button(add_net_ns_window, text='Submit', command = lambda: add_net_ns.add(net_namespace_frame, ns_name, device1, device2, ip1, ip2))
        add_ns_btn.grid(row=5, column=4)
        
    else:
        Label(add_net_ns_window, text = "Sorry, you cannot access this window because you do not have root privileges").pack()

def net_ns_view(ns): #passing in ns name
    #TODO: make this page scrollable!!
    ns_view = Toplevel(root)
    #ns_view = tk.Canvas(root)
    ns_view.title("Namespace GUI: Namespace View")
    #scrollbar = ttk.Scrollbar(root, orient="vertical", command=ns_view.yview)

    if(utils.checkuid[0] != "0"):
        Label(ns_view, text = "Sorry, you cannot access this window because you do not have root privileges").pack()
        return

    net_ns_header = Label(ns_view, text=ns)
    #ns_header.pack() #TODO : fix placement?? 


    #TODO: iterate through list of processes
    # procs = get_procs(ns)

    # header = procs[0].split(' ')
    # body = procs[1:]
    # for i, line in enumerate(body):
    #     line = line.split(' ')
    #     row = []
    #     for element in line:
    #         element = element.strip()
    #         if element:
    #             row.append(element)
    #     if(row):
    #         body[i] = row    
    # columns = []
    # for col in header:
    #     col = col.strip()
    #     if(col):
    #         columns.append(col)

    
    # proc_table = ttk.Treeview(process_frame, columns = columns)
    # for col in columns: 
    #     proc_table.heading(col, text=col)


    # ### PROC TABLE ###
    # # populate the table: #TODO: values are not lined up with the correct columns
    # for i, line in enumerate(body):
    #     # print(line, type(line))
    #     proc_table.insert(parent='', index='end', iid = i, text='', values = line)
    # proc_table.grid(row = 0, column = 1)
    # # procs[0] is header for table
    # for i, proc in enumerate(procs):
    #     proc_label = Label(process_frame, text=(proc)) #TODO: get namespace name and insert here
    #     #proc_label.grid(row=i, column=0)

    # TODO : Remove namespace button

##################################### FRAME #########################################
#creating frames
net_namespace_frame = Frame(root, text="Network Namespaces", padx=5, pady=5)
net_namespace_frame.grid(row = 0, column = 0, padx=10, pady=10)

################################## List namespaces ##################################
utils.list_namespaces(net_namespace_frame)

############################### Home #######################

add_ns_btn = Button(net_namespace_frame, text="+", command = lambda net_namespace_frame = net_namespace_frame: add_net_ns_window(net_namespace_frame))
add_ns_btn.grid(row=0, column=1)

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