import socket
import struct
import time
import threading



def connectThem(number):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)
    # print('TCP Client created')
    Server_IP = '141.37.168.26'
    Server_PORT = i
    #print('Connecting to TCP server with IP ', Server_IP, ' on Port ', Server_PORT)
    try:
        sock.connect((Server_IP, Server_PORT))
        msg = "Hello"
        sock.send(msg)
        answer = sock.recv(1024)
        print("Ergebnis Socket " + i + ": " + str(answer))
    except socket.timeout:
        pass
        #print('Socket timed out at', time.asctime())
    sock.close()

for i in range(1,51):
    t1 = threading.Thread(target=connectThem, args=(i,))
    t1.start()
