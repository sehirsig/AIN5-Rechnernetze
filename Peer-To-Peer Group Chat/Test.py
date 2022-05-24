import struct

s = "dffsfhdksdppo".encode("utf8")
a = struct.pack("i"*len(s), *s)
u = bytes(struct.unpack("i"*len(s), a))
print(u.decode("utf8"))

s1 = "Hallo".encode("utf8")
s2 = "Hi".encode("utf8")
a = struct.pack("i"*(len(s1) + len(s2)), *(s1 + s2))
u = bytes(struct.unpack("i"*(len(s1) + len(s2)), a))
print(u.decode("utf8"))