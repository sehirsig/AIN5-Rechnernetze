import socket
import struct
import time

Server_IP = '127.0.0.1'
Server_PORT = 50000

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(10)
print('Connecting to TCP server with IP ', Server_IP, ' on Port ', Server_PORT)
sock.connect((Server_IP, Server_PORT))

try:
    print("Operator angeben: 1 - 4 (Summe, Produkt, Minimum, Maximum):")
    op = int(input())
    print("Zahlen angeben, mit Leerzeichen getrennt:")
    l = input().split(" ")
    l = list(map(int, l))
    s1 = struct.pack("ii", op, len(l))
    sock.send(s1)
    s2 = struct.pack("i"*len(l), *l)
    sock.send(s2)
    res = struct.unpack("l", sock.recv(8))
    print("Ergebnis: " + str(res[0]))
except socket.timeout:
    print('Socket timed out at',time.asctime())
sock.close()
