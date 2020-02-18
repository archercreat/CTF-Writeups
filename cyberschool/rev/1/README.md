## Первое задание

### Что собирает программа

``` asm
_start:
mov dword ptr [flag + 6], 1870225259
mov eax, 3738091242
ror eax, 1
mov dword ptr [flag + 10], eax
mov eax, 2342557323
xor eax, 0xFFFFFFFF
bswap eax
mov dword ptr [flag + 14], eax
jmp _stop

_stop:
jmp _stop

flag:
db "CSMSU{"
resb 12
db '}'
```



resb резервирует 12 байт (3 двойных слова), после строчки **CSMSU{**

Из кода видно, что первое двойное слово (4 байта) заполняется **1870225259**

Второе двойное слово заполняется **3738091242 >> 1**

Третье двойное слово заполняется **bswap32(2342557323 ^ 0xffffffff)**

### Решение

```python
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
out += p32(1870225259) # first dword


out += p32(ror(3738091242, 1, 32)) # second dword
out += p32(swap32((2342557323 ^ 0xffffffff)))	# third dword

print(out)
```

