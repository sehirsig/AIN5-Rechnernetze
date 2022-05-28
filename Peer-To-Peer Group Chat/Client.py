import socket

NOTIFY_NEW_USER_COMMAND = 1

user_list = []

Server_IP = '127.0.0.1'
Server_PORT = 50000

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.settimeout(100)
print('Connecting to TCP server with IP ', Server_IP, ' on Port ', Server_PORT)
sock.connect((Server_IP, Server_PORT))
print("Spitzname eingeben:")
nickname = input()
sock.send(nickname.encode('utf-8'))


def get_ip_from_bytes(ip):
    res = ""
    for i in range(3):
        res += (str(ip[i]) + ".")
    res += str(ip[3])
    return res

while True:
    #command = struct.unpack("i", sock.recv(4))
    #if command == NOTIFY_NEW_USER_COMMAND:
    paket = sock.recv(1024)
    length = int.from_bytes(paket[0:4], 'big')
    nickname = paket[4:length - 8].decode("utf8")
    ip = get_ip_from_bytes(paket[length - 8: length - 4])
    port = int.from_bytes(paket[length - 4:length], 'big')
    user_list.append((nickname, ip, port))
    print("new User\n" + nickname)
