import binascii
import struct

# Rotate right: 0b1001 --> 0b1100
ror = lambda val, r_bits, max_bits: \
    ((val & (2**max_bits-1)) >> r_bits%max_bits) | \
    (val << (max_bits-(r_bits%max_bits)) & (2**max_bits-1))

def swap32(i):
    return struct.unpack("<I", struct.pack(">I", i))[0]

p32 = lambda x: struct.pack('<I', x)

out = b''
out += p32(1870225259)


out += p32(ror(3738091242, 1, 32))
out += p32(swap32((2342557323 ^ 0xffffffff)))

print(out)