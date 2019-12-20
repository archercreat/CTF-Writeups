from __future__ import print_function   # PEP 3105
import re
import binascii
import struct
import idaapi
import idc
import yara

rules = """
rule nanomite
{

    strings:
        $s1 = {EC ??}

    condition:
        any of them
}
"""



# max bits > 0 == width of the value in bits (e.g., int_16 -> 16)

# Rotate left: 0b1001 --> 0b0011
rol = lambda val, r_bits, max_bits: \
    (val << r_bits%max_bits) & (2**max_bits-1) | \
    ((val & (2**max_bits-1)) >> (max_bits-(r_bits%max_bits)))

# Rotate right: 0b1001 --> 0b1100
ror = lambda val, r_bits, max_bits: \
    ((val & (2**max_bits-1)) >> r_bits%max_bits) | \
    (val << (max_bits-(r_bits%max_bits)) & (2**max_bits-1))

max_bits = 32  # For fun, try 2, 17 or other arbitrary (positive!) values


fnc_start = 0x698   # get_seed
fnc_end = 0x8f2     # get_seed
#fnc_start = 0x8F2  # main algo
#fnc_end = 0x12B9   # main algo

def encode(val):
    val = binascii.hexlify(val)
    val = long(binascii.hexlify(struct.pack('<Q', long(val, 16))), 16)
    return ~ror(0xCAFEDEADBEEFCAFE ^ val, 3, 32) & 0xffffffff

start = 0x401000
end = 0x40c000

def patch(dest, seq):
    for i, c in enumerate(seq):
        idc.PatchByte(dest+i, ord(c))

def nanomite(number):
    number = struct.unpack("B", number)[0]
    if number == 7:         # ok
        return (0x73, 10)
    elif number == 11:      # ok
        return (0x7d, 10)
    elif number == 13:      # ok
        return (0x7f, 10)
    elif number == 12:      # ok
        return (0x7c, 10)
    elif number == 14:      # ok
        return (0x7e, 10)
    elif number == 9:       # ok
        return (0x77, 10)
    elif number == 10:      # ok
        return (0x76, 10)
    elif number == 8:       # ok
        return (0x72, 10)
    elif number == 3:       # ok
        return (0x79, 10)
    elif number == 5:       # ok
        return (0x75, 10)
    elif number == 6:       # ok
        return (0x74, 10)
    elif number == 1:       # ok
        return (0x71, 10)
    elif number == 0:       # ok < no conditional
        return (0x90, 0x90)
    elif number == 4:       # ok
        return (0x78, 10)
    elif number == 2:       # ok
        return (0x70, 10)
    else:
        return (0x00, 0x00)


align = lambda size, alignment: ((size // alignment) + 1) * alignment

if __name__ == "__main__":
    start = idc.get_segm_by_sel(0)
    end = idc.get_segm_end(start)
    data = idaapi.get_many_bytes(start  + fnc_start, fnc_end - fnc_start + 2)
    matches = yara.compile(source=rules).match(data=data)
    count = 0
    match = list()
    for hit in matches:
        if hit.rule == 'nanomite':
            match = hit.strings
    for hit in match:
        (offset, name, pattern) = hit
        number = data[offset + 1]
        encoded = data[offset + 2:offset + 2 + 8]
        jmp_addr = encode(encoded)
        jmp_addr_off = (jmp_addr - (start + fnc_start +  offset + 2) & 0xffffffff) & 0xffffffff
        ins, jmp_off = nanomite(number)
        if ins == 0x00 or jmp_addr < 0x401000 or jmp_addr > 0x40c000:
            continue
        else:
            print(hex(start + fnc_start + offset), hex(struct.unpack("B", number)[0]))
        if ins == 0x90:
            conditional = "\x90\x90"
        else:
            conditional = struct.pack("B", ins) + struct.pack("B", jmp_off - 2)
            constant = "\xE9" + struct.pack("<I", jmp_addr_off - 5)
        #conditional = "\x90\x90"

        patch(start + fnc_start + offset, conditional)
        patch(start + fnc_start + offset + 2, constant)
