import numpy as np

EXIT_COMMAND = 1
NOTIFY_REGISTERED_USER_COMMAND = 2
NOTIFY_UNREGISTERED_USER_COMMAND = 3
BROADCAST_COMMAND = 4
REGISTER_RESPONSE_COMMAND = 5


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


def print_broadcast_msg(data):
    len_nickname = int.from_bytes(data[4:8], 'big')
    start_nickname = 8
    end_nickname = start_nickname + len_nickname
    nickname = data[start_nickname: end_nickname].decode("utf8")
    start_msg = end_nickname + 4
    len_msg = int.from_bytes(data[end_nickname: start_msg], 'big')
    end_msg = start_msg + len_msg
    msg = data[start_msg: end_msg].decode("utf8")
    print("broadcast_msg from: " + nickname + ":\n" + msg)
