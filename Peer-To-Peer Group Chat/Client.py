import socket
import random
import time
from threading import Thread, Lock
from Utils import *

input_lock = Lock()

user_list = []

chat_list = []

Server_IP = '127.0.0.1'
Server_PORT = 50000

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# udp_sock.sendto("".encode('utf-8'),
#                (Server_IP, Server_PORT))  # Dummy-Nachricht, damit dieser Socket einen Lokal-Port bekommt

My_IP = "127.0.0.1"
My_PORT = random.randint(50001, 65000)
udp_sock.bind((My_IP, My_PORT))

sock.settimeout(10000)
print('Connecting to TCP server with IP ', Server_IP, ' on Port ', Server_PORT)
sock.connect((Server_IP, Server_PORT))

input_lock.acquire()
print("Spitzname eingeben:")
my_nickname = input()
input_lock.release()


# Paket:
# 1 Byte - Type
# msg_type = 1.to_bytes(1, 'big')
# msgtype + nickname-lenght + nickname + IPv4 + Port(4-bit uint)
#
#


def send_initial_package():
    msg_num = REGISTER_REQUEST
    msg_type_b = msg_num.to_bytes(1, 'big')
    nickname_b = my_nickname.encode('utf-8')
    nickname_length = len(nickname_b).to_bytes(1, 'big')
    ipv4, port = udp_sock.getsockname()  # .to_bytes(4, 'big')
    ipv4_b = make_bytes_from_ip_str(Server_IP)  # server ip is firtsly the same like client ip
    port_b = port.to_bytes(4, 'big')
    paket = msg_type_b + nickname_length + nickname_b + ipv4_b + port_b
    sock.send(paket)
    print("Send!")


send_initial_package()


def get_user_index(nickname):
    for i in range(len(user_list)):
        if user_list[i][0] == nickname:
            return i
    print("no such user")
    exit(1)


# UDP Call von A zu B (B wird mit TCP connect antworten)
def send_chat_request(ip, port, nickname):
    chat_IP = ip  # '127.0.0.1'
    chat_PORT = port  # 50000
    # Open a TCP Socket
    my_ip, my_port = sock.getsockname()
    new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_port = random.randint(50050, 65000)
    new_socket.bind((my_ip, my_port))
    new_socket.settimeout(10000)
    msg_num = CHAT_REQUEST
    msg_type_b = msg_num.to_bytes(1, 'big')
    my_port_b = my_port.to_bytes(4, 'big')
    paket = msg_type_b + my_port_b
    # Wait for TCP Answer
    # print('Listening on Port ', str(my_port), ' for incoming TCP connections')
    new_socket.listen(1)
    # print('Listening ...')
    # Send Request
    udp_sock.sendto(paket, (chat_IP, chat_PORT))
    # print('Waiting to accept ...')
    conn, addr = new_socket.accept()
    print(f'Incoming connection with {str(nickname)} accepted: ', addr)
    chat_list.append((nickname, conn))


def routine_receive_chat_sendrqst():
    chats = 0
    while True:
        if chats > len(chat_list):
            chats = len(chat_list)
            continue;
        if chats == len(chat_list):
            time.sleep(0.1)
            continue
        print(f"New chat with {str(chat_list[-1][0])} added!")
        Thread(target=receive_chat(chat_list[-1][0], chat_list[-1][1])).start()


def receive_chat(nickname, conn):
    while True:
        paket = conn.recv(1024)
        msg = paket.decode("utf8")
        print("New Message!")
        print(f"{str(nickname)}: {str(msg)}")


def routine_receive_chat_request():
    paket, (chat_IP, chat_UDP_PORT) = udp_sock.recvfrom(8)
    msg_type = int(paket[0])
    chat_TCP_port = int.from_bytes(paket[1:5], 'big')

    nickname = "Unknown"
    # find out the user
    for users in user_list:  # nickname, ip, port
        if users[1] == chat_IP:
            if users[2] == chat_UDP_PORT:
                nickname = users[0]
                break

    print(
        f"Received a message request from {str(nickname)} {str(chat_IP)} with TCP Port {str(chat_TCP_port)}! Type 'skiprtn' to accept/decline")
    input_lock.acquire()
    print("Incoming request from: " + str(chat_IP) + ":" + str(
        chat_TCP_port) + "\nDo you want to start the chat? (type 'y' to accept)")
    result = input()
    input_lock.release()
    if (result != "y"):
        print("Chat request refused!")
        return
    chat_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    chat_socket.settimeout(10000)
    chat_socket.connect((chat_IP, chat_TCP_port))
    print(chat_socket.getsockname())
    chat_list.append((nickname, chat_socket))
    # Thread(target=receive_chat(nickname,chat_socket)).start()


def new_user(paket, length):
    nickname = paket[2:length + 2].decode("utf8")
    ip = get_ip_from_bytes(paket[length + 2: length + 6])
    port = int.from_bytes(paket[length + 6:length + 10], 'big')
    user_list.append((nickname, ip, port))
    print("new User\n" + nickname)


def remove_user(paket, length, nickname):
    print("User exited: " + nickname)
    idx = get_user_index(nickname)
    user_list.pop(idx)


def receive_broad_cast(data):
    msg_type = int(data[0])
    nick_len = int.from_bytes(data[1: 2], 'big')
    nickname = data[2:2 + nick_len].decode("utf8")
    len_msg = int.from_bytes(data[2 + nick_len: 3 + nick_len], 'big')
    msg = data[3 + nick_len: 3 + nick_len + len_msg].decode("utf8")
    print("broadcast_msg from >" + nickname + "<: " + msg)


def print_register_response(paket):
    current_limit = 5
    len_user_array = int.from_bytes(paket[1:current_limit], 'big')
    print("Received Register Response")
    for user_id in range(len_user_array):
        current_limit += 1
        nickname_length = int.from_bytes(paket[current_limit - 1:current_limit], 'big')
        nickname = paket[current_limit: current_limit + nickname_length].decode("utf8")
        current_limit = current_limit + nickname_length
        ip = get_ip_from_bytes(paket[current_limit: current_limit + 4])
        udp_port = int.from_bytes(paket[current_limit + 4: current_limit + 8], 'big')
        current_limit = current_limit + 8
        user_list.append((nickname, ip, udp_port))
        print("register-response:\nnickname: " + nickname + "; ip: " + ip + "; udp_port: " + str(udp_port))


def routine_listen_to_server():
    while True:
        paket = sock.recv(1024)
        cmd = int.from_bytes(paket[0:1], 'big')
        if cmd == ADD_USER:
            length = int.from_bytes(paket[1:2], 'big')
            new_user(paket, length)
        elif cmd == REMOVE_USER:
            length = int.from_bytes(paket[1:2], 'big')
            nickname = paket[2: 2 + length].decode("utf8")

            for chats in range(len(chat_list)):
                if chat_list[chats][0] == nickname:
                    chat_list.pop(chats)

            if nickname == my_nickname:

                sock.close()
                import os
                os._exit(0)

            remove_user(paket, length, nickname)
        elif cmd == BROADCAST:
            receive_broad_cast(paket)
        elif cmd == REGISTER_RESPONSE:
            print_register_response(paket)


def send_broad_cast(msg):
    cmd_b = BROADCAST_MSG.to_bytes(1, 'big')
    len_msg_b = len(msg).to_bytes(1, 'big')
    msg_b = msg.encode("utf8")
    paket = cmd_b + len_msg_b + msg_b
    sock.send(paket)


def send_message(chat_user):
    input_lock.acquire()
    print("Write your message:")
    MESSAGE = input()
    input_lock.release()
    # MESSAGE_length_b = len(MESSAGE).to_bytes(1, 'big')
    MESSAGE_b = MESSAGE.encode('utf-8')
    # paket = MESSAGE_length_b + MESSAGE_b
    paket = MESSAGE_b
    chat_user[1].send(paket)
    print(f"Message '{str(MESSAGE)}' send to {str(chat_user[0])}!")


# skiprtn to let routine sleep for 2 seconds!
def routine_user_input():
    while True:
        input_lock.acquire()
        print("Routine: (exit/broadcast/rqstchat/showlist/skiprtn/chatlist/sendmsg/help)")
        s = input()
        input_lock.release()
        if s == "exit":
            paket = DEREGISTER.to_bytes(1, 'big')
            sock.send(paket)
        elif s == "broadcast":
            input_lock.acquire()
            print("Type a message to broadcast:")
            msg = input()
            input_lock.release()
            send_broad_cast(msg)
        elif s == "showlist":
            counter = 0
            for users in user_list:
                print(str(counter) + " : " + str(users))
                counter += 1
        elif s == "rqstchat":
            input_lock.acquire()
            print("Type a usernum to request a chat to:")
            receiver = int(input())
            input_lock.release()
            if (receiver >= len(user_list) or receiver < 0):
                print(f"User {str(receiver)} does not exist!")
                continue
            receiver_ip = user_list[receiver][1]  # (nickname, ip, port)
            receiver_udp_port = user_list[receiver][2]
            print(f"Sending chat request to {str(user_list[receiver][0])}")
            send_chat_request(receiver_ip, receiver_udp_port, str(user_list[receiver][0]))
            print("FINISHED DEBUG DEBUG FINISHED")
        elif s == "skiprtn":
            time.sleep(2)
        elif s == "chatlist":
            counter = 0
            for users in chat_list:
                print(str(counter) + " : " + str(users))
                counter += 1
        elif s == "sendmsg":
            input_lock.acquire()
            print("Enter a usernum from chatlist")
            chatnum = int(input())
            input_lock.release()
            send_message(chat_list[chatnum])
        elif s == "help":
            print("""
            Commands:
            exit - Exit the Server
            broadcast - Send a message to everyone
            rqstchat - request a chat from someone in the showlist
            showlist - all users on the server
            skiprtn - skip the routine input
            chatlist - list with all your chats
            sendmsg - send a message to someone from your chatlist
            """)


Thread(target=routine_listen_to_server).start()
Thread(target=routine_user_input).start()
Thread(target=routine_receive_chat_request).start()
Thread(target=routine_receive_chat_sendrqst).start()
