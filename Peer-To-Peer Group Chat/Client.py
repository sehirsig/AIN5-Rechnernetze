import socket
from threading import Thread, Lock

NOTIFY_NEW_USER_COMMAND = 1
EXIT_COMMAND = 2

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

#Paket:
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
    ipv4, port = udp_sock.getsockname()#.to_bytes(4, 'big')
    ipv4_b = socket.inet_aton(ipv4)
    port_b = port.to_bytes(4, 'big')
    paket = msg_type_b + nickname_length + nickname_b + ipv4_b + port_b
    sock.send(paket)
    print("bytes: " + str(paket))
    print("Send!")


send_initial_package()


def get_ip_from_bytes(ip):
    res = ""
    for i in range(3):
        res += (str(ip[i]) + ".")
    res += str(ip[3])
    return res


#UDP Call von A zu B (B wird mit TCP connect antworten)
def send_chat_request(ip, port):
    chat_IP = ip #'127.0.0.1'
    chat_PORT = port #50000
    #Open a TCP Socket
    my_ip, my_port = sock.getsockname()
    new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    new_socket.bind((my_ip, my_port))
    msg_num = 5
    msg_type_b = msg_num.to_bytes(1, 'big')
    my_port_b = my_port.to_bytes(4, 'big')
    paket = msg_type_b + my_port_b
    #Send Request
    udp_sock.sendto(paket, (chat_IP, chat_PORT))
    #Wait for TCP Answer
    print('Listening on Port ', My_PORT, ' for incoming TCP connections')
    sock.listen(1)
    print('Listening ...')


def receive_chat_request():
    paket, (chat_UDP_PORT, chat_IP) = udp_sock.recv(4)
    msg_type = int(paket[0])
    chat_TCP_port = int.from_bytes(paket[1:5], 'big')
    chat_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    chat_socket.settimeout(100)
    chat_socket.connect((chat_IP, chat_TCP_port))


def routine_wait_for_new_users():
    while True:
        # command = struct.unpack("i", sock.recv(4))
        # if command == NOTIFY_NEW_USER_COMMAND:
        paket = sock.recv(1024)
        length = int.from_bytes(paket[1:5], 'big') + 1
        nickname = paket[5:length - 8].decode("utf8")
        ip = get_ip_from_bytes(paket[length - 8: length - 4])
        port = int.from_bytes(paket[length - 4:length], 'big')
        user_list.append((nickname, ip, port))
        print("new User\n" + nickname)


def routine_user_input():
    while True:
        input_lock.acquire()
        s = input()
        input_lock.release()
        if s == "exit":
            paket = EXIT_COMMAND.to_bytes(4, 'big')
            sock.send(paket)
            sock.close()


Thread(target=routine_wait_for_new_users).start()
Thread(target=routine_user_input).start()
