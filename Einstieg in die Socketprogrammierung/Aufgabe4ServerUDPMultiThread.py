import socket
import struct
import threading
import time

SUM = 1
PRODUCT = 2
MIN = 3
MAX = 4

def connectThem(number):
    My_IP = '127.0.0.1'
    My_PORT = number
    server_activity_period = 30;

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((My_IP, My_PORT))
    print('Listening on Port ', My_PORT, ' for incoming TCP connections');

    t_end = time.time() + server_activity_period  # Ende der Aktivitätsperiode

    while time.time() < t_end:
        try:
            a, adress1 = sock.recvfrom(8)
            s1 = struct.unpack("ii", a)
            OPERATOR = s1[0]
            LENGTH = s1[1]
            b, adress2 = sock.recvfrom(4 * LENGTH)
            if (adress1 != adress2):
                print("Received second package from wrong IP Address. Error.")
                break;
            s2 = struct.unpack("i" * LENGTH, b)
            res = calculate(OPERATOR, s2)
            sock.sendto(struct.pack("l", res), adress1)
        except socket.timeout:
            print('Socket timed out at', time.asctime())

    sock.close()
    if sock:
        sock.close()

def calculate(OPERATOR, b):
    def sum():
        sum = 0
        for e in b:
            sum += e
        return sum

    def product():
        product = 1
        for e in b:
            product *= e
        return product

    def minimum():
        min = b[0]
        for e in b:
            if e < min:
                min = e
        return min

    def maximum():
        max = 0
        for e in b:
            if e > max:
                max = e
        return max

    switcher = [sum, product, minimum, maximum]
    return switcher[OPERATOR - 1]()


for i in range(50000,50003):
    t1 = threading.Thread(target=connectThem, args=(i,))
    t1.start()
