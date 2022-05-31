import numpy as np

#1. Register-Request (MsgType, Nickname-Length, Nickname, IPv4, Port)
#2. Register-Response (MsgType, Anzahl-User, {Nickname-Length, Nickname, IPv4, Port})
#3. Add-User (MsgType, Nickname-Length, Nickname, IPv4, Port)
#4. Chat-Request  (MsgType, tcp-port)
#5. Broadcast-MSG (send to server) (MsgType, Message-Length, Message)
#6. Broadcast (from server) (MsgType, Nickname-Length, Nickname, Message-Length, Message)
#7. DeRegister (MsgType ?)
#8. Remove-User (MsgType, Nickname-Length, Nickname)

EXIT_COMMAND = 0
REGISTER_REQUEST = 1
REGISTER_RESPONSE = 2
ADD_USER = 3
CHAT_REQUEST = 4
BROADCAST_MSG = 5
BROADCAST = 6
DEREGISTER = 7
REMOVE_USER = 8


def make_bytes_from_ip_int_array(l):
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


def make_bytes_from_ip_str(ip_str):
    l = list(map(lambda x: int(x), ip_str.split(".")))
    return make_bytes_from_ip_int_array(l)


def get_ip_from_bytes(ip):
    res = ""
    for i in range(3):
        res += (str(ip[i]) + ".")
    res += str(ip[3])
    return res


def print_broadcast_msg(nickname, data):
    len_msg = int.from_bytes(data[1: 2], 'big')
    end_msg = 2 + len_msg
    msg = data[2: end_msg].decode("utf8")
    print("broadcast_msg from >" + nickname + "<: " + msg)
