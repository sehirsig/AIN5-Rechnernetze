import socket
import threading
import time


def connectThem(number):
    My_IP = "127.0.0.1"
    My_PORT = number
    server_activity_period=30 # Zeit, wie lange der Server aktiv sein soll

    sock = socket.socket(socket.AF_INET,
                     socket.SOCK_DGRAM) 
    sock.bind((My_IP, My_PORT))

    sock.settimeout(10)
    t_end=time.time()+server_activity_period # Ende der Aktivitätsperiode

    while time.time()<t_end:
        try:
            data, addr = sock.recvfrom(1024)
            print('received message: '+data.decode('utf-8')+' from ', addr)
            sock.sendto(data[::-1],addr)
        except socket.timeout:
            print('Socket timed out at',time.asctime())

    sock.close()

for i in range(50000,50003):
    t1 = threading.Thread(target=connectThem, args=(i,))
    t1.start()