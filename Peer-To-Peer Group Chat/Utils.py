import numpy as np


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
