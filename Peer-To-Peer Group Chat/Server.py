import socket
import struct
import time
from threading import Thread
from Utils import *

client_list = []  # [Spitzname, IP-Adresse, Port, Socket]

My_IP = '127.0.0.1'
My_PORT = 50000
server_activity_period = 100

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((My_IP, My_PORT))
print('Listening on Port ', My_PORT, ' for incoming TCP connections')

t_end = time.time() + server_activity_period  # Ende der Aktivitätsperiode

sock.listen(1)
print('Listening ...')


def notify_others_user_exited(nickname):
    for i in range(len(client_list)):
        conn = client_list[i][3]
        cmd_b = REMOVE_USER.to_bytes(1, 'big')
        length_b = len(nickname).to_bytes(1, 'big')
        nickname_b = nickname.encode("utf8")
        paket = cmd_b + length_b + nickname_b
        conn.send(paket)


def broadcast(conn, data):  # (nickname, ipv4, udp_port, conn)
    msg_num = BROADCAST
    msg_type_b = msg_num.to_bytes(1, 'big')
    old_msg_b = data[1:]
    nickname = ""
    for i in range(len(client_list)):
        if conn == client_list[i][3]:
            nickname = client_list[i][0]
            break
    print_broadcast_msg(nickname, data)
    nickname_length_b = len(nickname).to_bytes(1, 'big')
    nickname_b = nickname.encode("utf8")
    new_paket = msg_type_b + nickname_length_b + nickname_b + data[1:]
    for i in range(len(client_list)):
        if conn == client_list[i][3]:
            continue
        client_list[i][3].send(new_paket)


def routine_listen_to_clients(idx, conn):
    data = conn.recv(1024)
    cmd = int.from_bytes(data[0:1], 'big')
    if cmd == DEREGISTER:
        nickname = client_list[idx][0]
        print("Client exited: " + nickname)
        notify_others_user_exited(nickname)
        client_list.pop(idx)
        conn.close()
    elif cmd == BROADCAST_MSG:
        print("Received a broadcast")
        broadcast(conn, data)


def notify_others_for_new(new_user):
    # bestehende Nutzer informieren
    for users in client_list:
        cmd = ADD_USER.to_bytes(1, 'big')
        nickname = new_user[0].encode("utf8")
        nickname_length = (len(nickname)).to_bytes(1, 'big')
        ip = make_bytes_from_ip_int_array(new_user[1])
        port = new_user[2].to_bytes(4, 'big')
        conn = users[3]
        paket = cmd + nickname_length + nickname + ip + port
        conn.send(paket)


def notify_user_for_new(new_user, user_index):
    cmd = ADD_USER.to_bytes(1, 'big')
    nickname = new_user[0].encode("utf8")
    nickname_length = (len(nickname)).to_bytes(1, 'big')
    ip = make_bytes_from_ip_int_array(new_user[1])
    port = new_user[2].to_bytes(4, 'big')
    conn = client_list[user_index][3]
    paket = cmd + nickname_length + nickname + ip + port
    conn.send(paket)


def make_register_response(new_user):  # (nickname, ipv4, udp_port, conn)
    msg_num = REGISTER_RESPONSE
    msg_type_b = msg_num.to_bytes(1, 'big')
    count_clients = len(client_list)
    nickname_paket_b = bytes()
    for users in client_list:  # (nickname, ipv4, udp_port, conn)
        if users[0] == new_user[0]:
            count_clients -= 1
            continue
        len_nickname_b = len(users[0]).to_bytes(1, 'big')
        nickname_b = users[0].encode("utf8")
        ip_b = make_bytes_from_ip_int_array(users[1])
        udp_port_b = users[2].to_bytes(4, 'big')
        packing = len_nickname_b + nickname_b + ip_b + udp_port_b
        nickname_paket_b += packing

    count_clients_b = count_clients.to_bytes(4, 'big')
    paket = msg_type_b + count_clients_b + nickname_paket_b
    new_user[3].send(paket)
    print("Register Response Send")


while True:
    try:
        conn, addr = sock.accept()
        print('Incoming connection accepted: ', addr)
        data = conn.recv(1024)
        msg_type = int(data[0])
        ##TODO If Statement msg_type checken
        length = int.from_bytes(data[1:2], 'big')  # + the MSG_Type
        nickname = data[2: 2 + length].decode("utf8")
        ipv4 = struct.unpack('BBBB', data[2 + length:2 + length + 4])
        udp_port = int.from_bytes(data[2 + length + 4: 2 + length + 4 + 4], 'big')
        print("client accepted: " + nickname)
        # ipv4 = get_ip_from_bytes(data[5 + length:5 + length + 4])
        new_user = (nickname, ipv4, udp_port, conn)
        notify_others_for_new(new_user)
        client_list.append(new_user)
        Thread(target=routine_listen_to_clients,
               args=(len(client_list) - 1, conn)).start()  # listen to commands from client
        make_register_response(new_user)
    except socket.timeout:
        print('Socket timed out listening', time.asctime())
