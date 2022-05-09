import socket
import struct
import time

Server_IP = '127.0.0.1'
Server_PORT = 50000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(10)

try:
    print("Operator angeben: 1 - 4 (Summe, Produkt, Minimum, Maximum)")
    op = int(input())
    l = input().split(" ")
    l = list(map(int, l))
    s1 = struct.pack("ii", op, len(l))
    sock.sendto(s1, (Server_IP, Server_PORT))
    s2 = struct.pack("i"*len(l), *l)
    sock.sendto(s2, (Server_IP, Server_PORT))
    res = struct.unpack("l", sock.recv(8))
    print("Ergebnis: " + str(res[0]))
except socket.timeout:
    print('Socket timed out at',time.asctime())
sock.close()
