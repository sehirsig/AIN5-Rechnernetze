import struct
import numpy as np

s = "dffsfhdksdppo".encode("utf8")
a = struct.pack("i"*len(s), *s)
u = bytes(struct.unpack("i"*len(s), a))
print(u.decode("utf8"))

s1 = "Hallo".encode("utf8")
s2 = "Hi".encode("utf8")
a = struct.pack("i"*(len(s1) + len(s2)), *(s1 + s2))
u = bytes(struct.unpack("i"*(len(s1) + len(s2)), a))
print(u.decode("utf8"))

ip_int_list = bytes(
    list(map(
        lambda x: np.int8(x),"78.25.63.125".split(".")
    ))
)
for i in range(len(ip_int_list)):
    print(int(ip_int_list[i]))
