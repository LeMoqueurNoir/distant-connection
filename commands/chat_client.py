# coding:utf-8
import socket
import datetime as dt
import threading
import sys
from colorama import *

init()


print("\n" * 100)  # To erase any content


def get_args():
    _host, _pseudo = "", ""
    for arg in sys.argv:
        if "host=" in arg:
            _host = "".join(arg.split("=")[1:])
        elif "pseudo=" in arg:
            _pseudo = "".join(arg.split("=")[1:])
    return _host, _pseudo


host, pseudo = get_args()
print(Fore.LIGHTGREEN_EX + f"You're connected to {host}, {pseudo}\n")
port = 4287  # IP de la machine cible
print(f"Connected on {host}:{port}\n")


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


def message(string):
    global pseudo
    return f"[{dt.datetime.now().strftime('%B %d %H:%M:%S')}] {pseudo} >>> {string}"


def send_message(sk, msg):
    msg = message(msg)
    data = msg.encode("utf-8")  # Return the utf-8 encoded text to transfer using the socket protocol
    sk.sendall(data)
    print(Fore.LIGHTGREEN_EX + msg)


class ConnectionError(Exception):
    def __init__(self, message="Failed to connect to the server !"):
        self.message = message
        super().__init__(self.message)


def rcv():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,
                 10)  # For the sk socket to be reusable multiple times without waiting delay
    s.bind(("", 4287))
    while True:
        s.listen(5)
        conn, address = s.accept()
        client_thread = ClientThread(conn)
        client_thread.start()


def send():
    while True:
        input_user = input("").strip()

        try:
            sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sk.connect((host, port))
            send_message(sk=sk, msg=input_user)

        except:
            raise ConnectionError()
        finally:
            sk.close()


threading.Thread(target=rcv).start()
send()
