flag = list(map(lambda x: int(x, 16), '''94 78  DE C2 D0 FC AE 32 6B B3 3E 1E D0 5B 3B C6 F6 26  06 8A 3C 42 F4 07 11 76 56 E1 11 F1 50 B5 13 E4  96 C6 74 F8 D8 08 41 9F DF 35 00'''.split()))

_1 = lambda j: ((j * 0x6d) & 0xff) ^ 0xef
_2 = lambda j: ((j ^ 0xff) * 0x6b) & 0xff

dl = 0
out = ''
for i in range(len(flag) - 1):
    for j in range(32, 127):
        if j & 0b1:
            t = (_2(j) + dl) & 0xff
        else:
            t = (_1(j) + dl) & 0xff
        if t == flag[i]:
            out += chr(j)
            dl  = t
            break
print(out)