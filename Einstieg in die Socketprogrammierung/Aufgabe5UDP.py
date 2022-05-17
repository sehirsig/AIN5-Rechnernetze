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
        dd = sock.sendto(msg.encode('utf-8'), (Server_IP, Server_PORT))
        print(str(dd))
        data, addr = sock.recvfrom(1024)
        print("-->" + "Ergebnis Socket " + str(number) + " : " + str(data) + " : " + str(addr)+ " at " + str(time.time() - start) + "\n")
    except Exception as e:
        print("-->" + str(number) + " Failed."+ " at " + str(time.time() - start) + " " + str(e) + "\n")
        #print('Socket timed out at', time.asctime())

for i in range(1,51):
    t1 = threading.Thread(target=connectThem, args=(i,))
    t1.start()
