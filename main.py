from tkinter import *
import home, utils
import os,time
import subprocess
import threading
    
stop_flag = threading.Event()    
print("before root")
root = Tk()
root.title("Namespace GUI: Home")
print("launching home")
home.Home(root)

def inotify():
    inotify_process = subprocess.Popen(["sudo", "./inotify_gui", "/var/run/netns", "output.txt"])
    filename = 'output.txt'
    gui_log = 'gui_log.txt'
    time.sleep(2)
    last_modified = os.path.getmtime(filename)
    last_modified_gui = os.path.getmtime(gui_log)
    while not stop_flag.is_set():
        current_modified = os.path.getmtime(filename)
        current_modified_gui = os.path.getmtime(gui_log)
        if (last_modified != current_modified) and (last_modified_gui != current_modified_gui):
            with open(filename, 'r') as f:
                with open(gui_log, 'r') as g:
                    lines = f.readlines()
                    if lines:
                        last_line = lines[-1]
                        gui_lines = g.readlines()
                        if gui_lines:
                            if last_line != gui_lines[-1]:
                                print("command line changes!!!")
                                utils.show_alert(last_line)
                                for widget in root.winfo_children():
                                    if not isinstance(widget,Toplevel):       
                                        widget.destroy()
                                home.Home(root).display_ns
                            #  utils.update_ns(homelink, homepage)
                                last_modified = current_modified
                                last_modified_gui = current_modified_gui
                        else:
                            print(gui_lines[-1], last_line)
                            print("command line changes!!!")
                            utils.show_alert(last_line)
                            for widget in root.winfo_children():
                                if not isinstance(widget,Toplevel):
                                    widget.destroy()
                            home.Home(root).display_ns
                        #  utils.update_ns(homelink, homepage)
                            last_modified = current_modified
                            last_modified_gui = current_modified_gui
        elif(last_modified != current_modified):
            with open(filename, 'r') as f:
                lines = f.readlines()
                if lines:
                    last_line = lines[-1]
                    print("command line changes!!!")
                    utils.show_alert(last_line)
                    for widget in root.winfo_children():
                        if not isinstance(widget,Toplevel):
                            widget.destroy()
                    home.Home(root).display_ns
                    #  utils.update_ns(homelink, homepage)
                    last_modified = current_modified
        time.sleep(1)

    

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
