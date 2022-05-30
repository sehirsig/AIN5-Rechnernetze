import socket
import random
from threading import Thread, Lock
from Utils import *

input_lock = Lock()

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

input_lock.acquire()
nickname = input()
input_lock.release()

# Paket:
# 1 Byte - Type
# msg_type = 1.to_bytes(1, 'big')
# msgtype + nickname-lenght + nickname + IPv4 + Port(4-bit uint)
#
#
msg_num = 1
msg_type = msg_num.to_bytes(1, 'big')
print(msg_type)


def send_initial_package():
    msg_num = 1
    msg_type_b = msg_num.to_bytes(1, 'big')
    nickname_b = nickname.encode('utf-8')
    nickname_length = len(nickname_b).to_bytes(4, 'big')
    ipv4, port = udp_sock.getsockname()  # .to_bytes(4, 'big')
    ipv4_b = make_bytes_from_ip_str(Server_IP)  # server ip is firtsly the same like client ip
    port_b = port.to_bytes(4, 'big')
    paket = msg_type_b + nickname_length + nickname_b + ipv4_b + port_b
    sock.send(paket)
    print("bytes: " + str(paket))
    print("Send!")


send_initial_package()


def get_user_index(nickname):
    for i in range(len(user_list)):
        if user_list[i][0] == nickname:
            return i
    print("no such user")
    exit(1)


# UDP Call von A zu B (B wird mit TCP connect antworten)
def send_chat_request(ip, port):
    chat_IP = ip  # '127.0.0.1'
    chat_PORT = port  # 50000
    # Open a TCP Socket
    my_ip, my_port = sock.getsockname()
    new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_port = my_port + random.randint(1, 999)
    new_socket.bind((my_ip, my_port))
    msg_num = 5
    msg_type_b = msg_num.to_bytes(1, 'big')
    my_port_b = my_port.to_bytes(4, 'big')
    paket = msg_type_b + my_port_b
    # Send Request
    udp_sock.sendto(paket, (chat_IP, chat_PORT))
    # Wait for TCP Answer
    print('Listening on Port ', str(my_port), ' for incoming TCP connections')
    sock.listen(1)
    print('Listening ...')


def receive_chat_request():
    paket, (chat_IP, chat_UDP_PORT) = udp_sock.recv(4)
    msg_type = int(paket[0])
    chat_TCP_port = int.from_bytes(paket[1:5], 'big')
    chat_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    chat_socket.settimeout(100)
    chat_socket.connect((chat_IP, chat_TCP_port))


def new_user(paket, length):
    nickname = paket[8:length - 8].decode("utf8")
    ip = get_ip_from_bytes(paket[length - 8: length - 4])
    port = int.from_bytes(paket[length - 4:length], 'big')
    user_list.append((nickname, ip, port))
    print("new User\n" + nickname)


def remove_user(paket, length):
    nickname = paket[8:length].decode("utf8")
    print("User exited: " + nickname)
    idx = get_user_index(nickname)
    user_list.pop(idx)


def receive_broad_cast(data):
    print_broadcast_msg(data)


def print_register_response(paket):
    len_nickname = int.from_bytes(paket[4:8], 'big')
    start_nickname = 8
    end_nickname = start_nickname + len_nickname
    nickname = paket[start_nickname: end_nickname].decode("utf8")
    ip = get_ip_from_bytes(paket[end_nickname: end_nickname + 4])
    udp_port = int.from_bytes(paket[end_nickname + 4 : end_nickname + 8], 'big')
    print("register-response:\nnickname: " + nickname + "; ip: " + ip + "; udp_port: " + str(udp_port))


def routine_wait_for_new_users():
    while True:
        paket = sock.recv(1024)
        cmd = int.from_bytes(paket[0:4], 'big')
        if cmd == NOTIFY_REGISTERED_USER_COMMAND:
            length = int.from_bytes(paket[4:8], 'big')
            new_user(paket, length)
        elif cmd == NOTIFY_UNREGISTERED_USER_COMMAND:
            length = int.from_bytes(paket[4:8], 'big')
            remove_user(paket, length)
        elif cmd == BROADCAST_COMMAND:
            receive_broad_cast(paket)
        elif cmd == REGISTER_RESPONSE_COMMAND:
            print_register_response(paket)


def send_broad_cast(msg):
    cmd_b = BROADCAST_COMMAND.to_bytes(4, 'big')
    len_nickname_b = len(nickname).to_bytes(4, 'big')
    nickname_b = nickname.encode("utf8")
    len_msg_b = len(msg).to_bytes(4, 'big')
    msg_b = msg.encode("utf8")
    paket = cmd_b + len_nickname_b + nickname_b + len_msg_b + msg_b
    sock.send(paket)


def routine_user_input():
    while True:
        input_lock.acquire()
        s = input()
        input_lock.release()
        if s == "exit":
            paket = EXIT_COMMAND.to_bytes(4, 'big')
            sock.send(paket)
            sock.close()
            exit(0)
        elif s == "broadcast":
            input_lock.acquire()
            msg = input()
            input_lock.release()
            send_broad_cast(msg)


Thread(target=routine_wait_for_new_users).start()
Thread(target=routine_user_input).start()
