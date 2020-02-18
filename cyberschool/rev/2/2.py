flag = [248, 224, 150, 126, 44, 172, 101, 55, 191, 35, 55, 174, 12, 112, 124, 86, 222, 66, 160, 122, 2, 196, 40, 209, 229, 249, 93, 55, 141, 95, 74, 183, 253, 0]
dl = 0
out = ''
for i in range(len(flag) - 1):
    for j in range(32, 127):
        temp = (j * 223) & 0xff
        temp ^= 0xa5
        if (dl + temp) & 0xff == flag[i]:
            out += chr(j)
            dl += temp
            dl &= 0xff
            break

print(out)