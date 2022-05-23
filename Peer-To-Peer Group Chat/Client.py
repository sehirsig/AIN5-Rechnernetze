import socket
import struct
import time

NOTIFY_NEW_USER_COMMAND = 1

user_list = []

Server_IP = '127.0.0.1'
Server_PORT = 50000

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(10)
print('Connecting to TCP server with IP ', Server_IP, ' on Port ', Server_PORT)
sock.connect((Server_IP, Server_PORT))
print("Spitzname eingeben:")
nickname = input()
sock.send(nickname.encode('utf-8'))

while True:
    command = struct.unpack("i", sock.recv(4))
    if command == NOTIFY_NEW_USER_COMMAND:
        nickname = sock.recv(1024).decode("utf8")
        ip = sock.recv(1024).decode("utf8")
        port = sock.recv(1024).decode("utf8")
        user_list.append((nickname, ip, port))
        print("new User: " + nickname + "; ip: ;" + ip + "port: " + port)
