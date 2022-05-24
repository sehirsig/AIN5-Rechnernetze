import struct

s = "dffsfhdksdppo".encode("utf8")
a = struct.pack("i"*len(s), *s)
u = bytes(struct.unpack("i"*len(s), a))
print(u.decode("utf8"))