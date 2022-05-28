import socket
from threading import Thread

NOTIFY_NEW_USER_COMMAND = 1

user_list = []

Server_IP = '127.0.0.1'
Server_PORT = 50000

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

udp_sock.sendto("".encode('utf-8'),
                (Server_IP, Server_PORT))  # Dummy-Nachricht, damit dieser Socket einen Lokal-Port bekommt

sock.settimeout(100)
print('Connecting to TCP server with IP ', Server_IP, ' on Port ', Server_PORT)
sock.connect((Server_IP, Server_PORT))
print("Spitzname eingeben:")
nickname = input()


def send_initial_package():
    nickname_b = nickname.encode('utf-8')
    port_b = udp_sock.getsockname()[1].to_bytes(4, 'big')
    length_b = (len(nickname_b) + 8).to_bytes(4, 'big')  # +8 für Portnummer und Länge
    paket = length_b + nickname_b + port_b
    sock.send(paket)


send_initial_package()


def get_ip_from_bytes(ip):
    res = ""
    for i in range(3):
        res += (str(ip[i]) + ".")
    res += str(ip[3])
    return res


def routine_wait_for_new_users():
    while True:
        # command = struct.unpack("i", sock.recv(4))
        # if command == NOTIFY_NEW_USER_COMMAND:
        paket = sock.recv(1024)
        length = int.from_bytes(paket[0:4], 'big')
        nickname = paket[4:length - 8].decode("utf8")
        ip = get_ip_from_bytes(paket[length - 8: length - 4])
        port = int.from_bytes(paket[length - 4:length], 'big')
        user_list.append((nickname, ip, port))
        print("new User\n" + nickname)


Thread(target=routine_wait_for_new_users).start()
