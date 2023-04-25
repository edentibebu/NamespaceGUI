from re import L
from tkinter import *
from tkinter import ttk
from ctypes import *
import subprocess
import os

import add_net_ns
import utils


class Home:
    def __init__(self, root):
        self.root = root
        self.frame = Frame(root)
        self.home()

    def home(self):
        # Add Namespace button
        add_ns_btn = Button(self.root, text="+", command = lambda \
            net_namespace_frame = self.root: self.open_add_ns_window(net_namespace_frame))
        add_ns_btn.grid(row=0, column=1)

        net_namespace_frame = LabelFrame(self.root, text="Network Namespaces", padx=5, pady=5)
        net_namespace_frame.grid(row = 0, column = 0, padx=10, pady=10)
        self.display_ns(net_namespace_frame)

    def display_ns(self, net_namespace_frame):
        # List namespaces 
        utils.list_namespaces(self.root, net_namespace_frame)

    
    def open_add_ns_window(self, net_namespace_frame):
        #top = Toplevel(self.root)
        add_net_ns.AddNS(self.root, net_namespace_frame)
        for widget in net_namespace_frame.winfo_children():
            widget.destroy()
#     def show_ns_view(self):
#         self.frame.destroy()  # destroy the current frame
#         page2.PageTwo(self.root)  # create the page 2 frame



# # def add_ns(ns_name):
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




    # TODO : Remove namespace button

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




# mem_procs = top_5_mem()
# cpu_procs = top_5_cpu().split('\n')

# print((cpu_procs), type(cpu_procs))
# cpu_header_list = cpu_procs[0].split(' ')

# for i, proc in enumerate(cpu_procs):
#     #print(proc)
#     proc_label = Label(process_cpu_frame, text=proc)
#     proc_label.grid(row=i, column=0)

#proc = Label(process_frame, text="process1")
#proc.grid(row=0, column=0)