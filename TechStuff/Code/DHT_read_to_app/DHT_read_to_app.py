import serial  # type: ignore
import tkinter as tk
import time
import ttkbootstrap as ttk # type: ignore
from ttkbootstrap.constants import * # type: ignore

ser = serial.Serial("COM3", 9600)
time.sleep(2)

root = ttk.Window(themename="cyborg")
root.title("DHT11 Monitor")
root.geometry("400x300")

temp_label = ttk.Label(root, text="Initializing sensor...", font=("Segoe UI", 20))
humid_label = ttk.Label(root, text="", font=("Segoe UI", 20))
tstatus_label = ttk.Label(root, text="", font=("Segoe UI",20),bootstyle="warning")
hstatus_label = ttk.Label(root, text="", font=("Segoe UI",20),bootstyle="warning")

temp_label.pack(pady=10)
humid_label.pack(pady=10)
tstatus_label.pack(pady=10)
hstatus_label.pack(pady=10)


def update():

    # Parsing input

    if ser.in_waiting:
        data = ser.readline().decode().strip()
        try:
            temp, humid = data.split(",")
            t = float(temp)
            h = float(humid)
            temp_label.config(text=f"Temperature: {temp} °C") 
            humid_label.config(text=f"Humidity: {humid} %") 
            print(f"Raw data: {data}")
        except:
            pass

    # Temperature Status

    if t < 10:
        tstatus_label.config(text="Cold!", bootstyle="primary")
    elif 10 <= t <= 20:
        tstatus_label.config(text="Cool", bootstyle="success")
    elif 20 <= t <= 30:
        tstatus_label.config(text="Warm", bootstyle="warning")
    else:
        tstatus_label.config(text="Hot!", bootstyle="danger")

    # Humidity Status

    if 0 <= h <= 15:
        hstatus_label.config(text="Dry!", bootstyle="danger")
    elif 15 < h < 50:
        hstatus_label.config(text="Mild", bootstyle="success")
    else:
        hstatus_label.config(text="Humid!", bootstyle="primary")
    
    root.after(1000, update)


root.after(2000, update)
root.mainloop()
