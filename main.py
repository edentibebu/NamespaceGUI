from tkinter import *
import home, utils
import os,time
import subprocess
import threading
    
stop_flag = threading.Event()    
print("before root")
root = Tk()
root.title("Namespace GUI: Home")
home.Home(root)

if not os.path.isfile('gui_log.txt'):
    with open('gui_log.txt', "w") as file:
       file.write("")

def inotify():
    inotify_process = subprocess.Popen(["sudo", "./inotify_gui", "/var/run/netns", "output.txt"])
    filename = 'output.txt'
    gui_log = 'gui_log.txt'
    time.sleep(2)
    last_modified = os.path.getmtime(filename)
    while not stop_flag.is_set():
        current_modified = os.path.getmtime(filename)
        if last_modified != current_modified:
            with open(filename, 'r') as f:
                lines = f.readlines()
                if lines:
                    last_line = lines[-1]
                    with open(gui_log, 'r') as g:
                        gui_lines = g.readlines()
                        if gui_lines:
                            if last_line != gui_lines[-1]:
                                print("command line changes!!!")
                                utils.show_alert(last_line)
                                home.Home(root).display_ns_cmd   
                                last_modified = current_modified
            time.sleep(0.1)
    

# print("starting thread")
thread = threading.Thread(target=inotify)
thread.start()

def on_closing():  
    stop_flag.set()
    thread.join()
    root.destroy()

# print("main loop")
root.protocol("WM_DELETE_WINDOW",on_closing)
root.mainloop()

