import socket
import struct
import time
import numpy as np

NOTIFY_NEW_USER_COMMAND = 1

client_list = []  # [Spitzname, IP-Adresse, Port, Socket]

My_IP = '127.0.0.1'
My_PORT = 50000
server_activity_period = 30;

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((My_IP, My_PORT))
print('Listening on Port ', My_PORT, ' for incoming TCP connections');

t_end = time.time() + server_activity_period  # Ende der Aktivitätsperiode

sock.listen(1)
print('Listening ...')


def make_bytes_from_ip(ip_str):
    l = list(map(lambda x: int(x), ip_str.split(".")))

    def check():
        if len(l) != 4:
            return False
        for e in l:
            if e < 0 | e > 255:
                return False
        return True

    if not check():
        print("ip adress uncorrect")
        exit(1)
    return bytes(
        list(map(
            lambda x: np.int8(x), l
        ))
    )


def notify_others(new_user):
    for i in range(len(client_list) - 1):
        msg = new_user[0].encode("utf8")
        ip = new_user[1]
        port = new_user[2].to_bytes(4, 'big')
        paket_length = (len(msg) + 12).to_bytes(4, 'big') # zusätzlich Länge von IP, Port und Paketlänge selbst
        paket = paket_length + msg + ip + port
        s = struct.pack("i" * len(paket), *paket)


while True:
    try:
        conn, addr = sock.accept()
        print('Incoming connection accepted: ', addr)
        nickname = conn.recv(1024).decode("utf8")
        print("client accepted: " + nickname)
        ip = make_bytes_from_ip(addr[0])
        port = addr[1]
        new_user = (nickname, ip, port, conn)
        client_list.append(new_user)
        notify_others(new_user)
    except socket.timeout:
        print('Socket timed out listening', time.asctime())
