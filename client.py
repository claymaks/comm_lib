import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server
msg = ""
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print("You have made initial connection...")
    while msg != "close":
        msg = input('Send message: ')
        s.sendall(msg.encode())
        if msg != "close":
            data = s.recv(1024)
            print('Received', repr(data.decode()))
