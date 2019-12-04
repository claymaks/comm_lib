# -*- coding: utf-8 -*-
import socket
HOST = '127.0.0.1'  # IP Address of computer running computer.py
PORT = 65433        # The port used by the server
msg = ""
try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print("You have made initial connection...")
        try:
            while True:
                button = input("//: ")
                s.sendall(button.encode())
                try:
                    s.settimeout(.1)
                    data = s.recv(1024)
                    print('Received', repr(data.decode()))
                except socket.timeout:
                    pass
                
        except KeyboardInterrupt:
            pass
except ConnectionRefusedError as e:
    print(e)
