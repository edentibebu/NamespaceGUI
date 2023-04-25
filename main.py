from tkinter import *
import home, utils
import os,time
import subprocess
import threading

def inotify():
    inotify_process = subprocess.Popen(["sudo", "./inotify_gui", "/var/run/netns", "output.txt"])
    filename = 'output.txt'
    last_modified = os.path.getmtime(filename)
    while(True):
        current_modified = os.path.getmtime(filename)
        if last_modified != current_modified:
            with open(filename, 'r') as file:
                lines = file.readlines()
                if lines:
                    last_line = lines[-1]
                    print(last_line)
                last_modified = current_modified
            time.sleep(0.1)

root = Tk()
root.title("Namespace GUI: Home")
home.Home(root)

thread = threading.Thread(target=inotify)
thread.start()
root.mainloop()