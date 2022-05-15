import socket
import struct
import time
import threading



def connectThem(number):
    start = time.time();
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)
    # print('TCP Client created')
    Server_IP = '141.37.168.26'
    Server_PORT = number
    print(Server_PORT)
    #print('Connecting to TCP server with IP ', Server_IP, ' on Port ', Server_PORT)
    try:
        msg = "Hello"
        sock.sendto(msg.encode('utf-8'), (Server_IP, Server_PORT))
        data, addr = sock.recvfrom(1024)
        print("-->" + "Ergebnis Socket " + number + " : " + str(data) + " : " + str(addr)+ " at " + str(time.time() - start))
    except:
        print("-->" + str(number) + " Failed."+ " at " + str(time.time() - start))
        #print('Socket timed out at', time.asctime())

for i in range(1,51):
    t1 = threading.Thread(target=connectThem, args=(i,))
    t1.start()
