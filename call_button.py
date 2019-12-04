# -*- coding: utf-8 -*-
import socket
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

channel = 13
GPIO.setup(channel, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

HOST = '127.0.0.1'  # IP Address of computer running computer.py
PORT = 65433        # The port used by the server
msg = ""
x = 0
try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print("You have made initial connection...")
        try:
            while True:
                if GPIO.input(channel) == GPIO.HIGH:
                    s.sendall("Pushed".encode())
                    x += 1
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
print(x)
