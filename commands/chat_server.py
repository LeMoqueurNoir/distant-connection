# coding:utf-8

import socket
import threading
import subprocess
import datetime as dt
import sys

ip_adress = sys.argv[-1]
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
            print(data)
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
    print(msg)


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
