import subprocess
from tkinter import *
import tkinter as tk
from tkinter import ttk

checkuid = subprocess.check_output("id -u", shell=True).decode()

def show_alert(message):
    alert_window = Toplevel()
    alert_window.title("Alert")
    alert_label = Label(alert_window, text=message)
    alert_label.pack(padx=20, pady=20)
    ok_button = Button(alert_window, text="OK", command=alert_window.destroy)
    ok_button.pack(pady=10)