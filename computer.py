import socket

#HOST = '192.168.1.20'  # Standard loopback interface address (localhost)
HOST = '127.0.0.1'  #IP Address of computer running this script
PORT = 65433        # Port to listen on (non-privileged ports are > 1023)
data = ""

x = 0
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            x += 1
            if not data:
                break
            msg = "Recieved " + data.decode('utf-8')
            print(msg)
            conn.sendall(("Acknowledged " + data.decode('utf-8')).encode())

print(x)
