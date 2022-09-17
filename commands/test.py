from tkinter import ttk
import tkinter as tk
from tkinter.messagebox import showinfo
import random
import time
import threading
from tkinter import PhotoImage


# root window
root = tk.Tk()
root.geometry('300x120')
root.maxsize(width=300, height=120)
root.minsize(width=300, height=120)
root.title('Mise à jour de Windows')
photo = PhotoImage(file="../img/WindowsLogo.png")
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


def progress():
    while pb['value'] < 100:
        pb['value'] += random.randint(5, 25) / 50
        value_label['text'] = update_progress_label()
        time.sleep(random.randint(4, 18) / 50)
    else:
        showinfo(message='The progress completed!')


def stop():
    pb.stop()
    value_label['text'] = update_progress_label()


# progressbar
pb = ttk.Progressbar(
    root,
    orient='horizontal',
    mode='determinate',
    length=280
)
# place the progressbar
pb.grid(column=0, row=0, columnspan=2, padx=10, pady=20)

# label
value_label = ttk.Label(root, text=update_progress_label())
value_label.grid(column=0, row=1, columnspan=2)


stop_button = ttk.Button(
    root,
    text='Stop',
    command=stop
)
stop_button.grid(column=1, row=2, padx=10, pady=10, sticky=tk.W)

threading.Thread(target=progress).start()
root.mainloop()

