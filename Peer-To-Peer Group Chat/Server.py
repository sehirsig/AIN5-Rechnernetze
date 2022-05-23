import socket
import struct
import time

NOTIFY_NEW_USER_COMMAND = 1

client_list = [] #[Spitzname, IP-Adresse, Port, Socket]

My_IP = '127.0.0.1'
My_PORT = 50000
server_activity_period = 30;

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((My_IP, My_PORT))
print('Listening on Port ', My_PORT, ' for incoming TCP connections');

t_end = time.time() + server_activity_period  # Ende der Aktivitätsperiode

sock.listen(1)
print('Listening ...')


def notify_others(new_user):
    for i in range(len(client_list) - 1):
        s = client_list[i][3]
        entry = client_list[i]
        s.send(struct.pack("i", NOTIFY_NEW_USER_COMMAND))
        s.send(entry[0].encode("utf8"))
        s.send(entry[1].encode("utf8"))
        s.send(entry[2].encode("utf8"))


while True:
    try:
        conn, addr = sock.accept()
        print('Incoming connection accepted: ', addr)
        nickname = conn.recv(1024).decode("utf8")
        print("client accepted: " + nickname)
        new_user = (nickname, addr[0], addr[1], conn)
        client_list.append(new_user)
        notify_others(new_user)
    except socket.timeout:
        print('Socket timed out listening', time.asctime())
