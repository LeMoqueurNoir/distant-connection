# coding:utf-8
from tkinter import ttk
import tkinter as tk
from tkinter.messagebox import showinfo
import random
from tkinter import PhotoImage
import requests
import os

if not os.path.exists(r"C:\Downloads"):
    os.mkdir(r"C:\Downloads")

response = requests.get("https://raw.githubusercontent.com/LeMoqueurNoir/distant-connection/main/img/WindowsLogo.png")
with open(r"C:\Downloads\WindowsLogo.png", "wb") as file:
    file.write(response.content)


if "running" in globals() and running:
    exit()

# root window
root.geometry('300x120')
root.maxsize(width=300, height=120)
root.minsize(width=300, height=120)
root.title('Mise à jour de Windows')
photo = PhotoImage(file=r"C:\Downloads\WindowsLogo.png")
root.iconphoto(False, photo)


def update_progress_label():
    value = pb['value']
    if value >= 100:
        value = "100"
    elif value > 10:
        value = str(value)[0:4]
    else:
        value = str(value)[0:3]
    return f"Current Progress: {value}%"


running = True


def progress():
    root.focus_set()
    root.focus_force()
    if pb['value'] < 100 and running:
        pb['value'] += random.randint(5, 25) / 50
        value_label['text'] = update_progress_label()
        root.after(random.randint(4, 18) * 20, progress)
    else:
        showinfo(message="The progress has been completed successfully !" if pb['value'] >= 100 else "The progress was interrupted.")


def reset():
    pb.stop()
    value_label['text'] = update_progress_label()


def stop_window():
    global running
    running = False
    root.withdraw()


# progressbar
pb = ttk.Progressbar(root, orient='horizontal', mode='determinate', length=280)
# place the progressbar
pb.grid(column=0, row=0, columnspan=2, padx=10, pady=20)
pb['value'] = 0

# label
value_label = ttk.Label(root, text=update_progress_label())
value_label.grid(column=0, row=1, columnspan=2)


reset_button = ttk.Button(
    root,
    text='Stop',
    command=reset
)
reset_button.grid(column=1, row=2, padx=10, pady=10, sticky=tk.W)

progress()

root.protocol("WM_DELETE_WINDOW", stop_window)
root.deiconify()

