# coding:utf-8
import socket
import datetime as dt
import threading
import sys

pseudo = sys.argv[0]
host, port = sys.argv[1], 4287  # IP de la machine cible


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


def message(string):
    global pseudo
    return f"[{dt.datetime.now().strftime('%B %d %H:%M:%S')}] {pseudo} >>> {string}"


def send_message(sk, msg):
    msg = message(msg)
    data = msg.encode("utf-8")  # Return the utf-8 encoded text to transfer using the socket protocol
    sk.sendall(data)
    print(msg)


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


threading.Thread(target=send).start()
threading.Thread(target=rcv).start()
