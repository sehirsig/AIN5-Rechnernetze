import socket
import struct
import time

SUM = 1
PRODUCT = 2
MIN = 3
MAX = 4

My_IP = '127.0.0.1'
My_PORT = 50000
server_activity_period = 30;

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((My_IP, My_PORT))
print('Listening on Port ', My_PORT, ' for incoming TCP connections');

t_end = time.time() + server_activity_period  # Ende der Aktivitätsperiode


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


while time.time() < t_end:
    try:
        a, adress = sock.recvfrom(8)
        s1 = struct.unpack("ii", a)
        OPERATOR = s1[0]
        LENGTH = s1[1]
        b, adress = sock.recvfrom(4 * LENGTH)
        s2 = struct.unpack("i" * LENGTH, b)
        res = calculate(OPERATOR, s2)
        sock.sendto(struct.pack("l", res), adress)
    except socket.timeout:
        print('Socket timed out at', time.asctime())

sock.close()
if sock:
    sock.close()
