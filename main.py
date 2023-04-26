from tkinter import *
import home, utils
import os,time
import subprocess
import threading

def inotify():
    inotify_process = subprocess.Popen(["sudo", "./inotify_gui", "/var/run/netns", "output.txt"])
    filename = 'output.txt'
    gui_log = 'gui_log.txt'
    time.sleep(2)
    last_modified = os.path.getmtime(filename)
    while(True):
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
                last_modified = current_modified
            time.sleep(0.1)
print("before root")
root = Tk()
root.title("Namespace GUI: Home")
print("launching home")
home.Home(root)

print("starting thread")
thread = threading.Thread(target=inotify)
thread.start()
print("main loop")
root.mainloop()
