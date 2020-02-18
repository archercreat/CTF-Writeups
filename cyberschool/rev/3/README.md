## Третье задание

Нам удалось получить дамп оперативной памяти по адресу 0. Известно, что там была какая-то программа.

P.S.: `objdump -D -b binary -m i386 -M intel re3.bin`

Дан `Re3.bin` файл, из описания понятно, что это код программы. Откроем в Иде и посмотрим

```asm
seg000:00000000 sub_0           proc near
seg000:00000000                 xor     edx, edx
seg000:00000002                 lea     esi, flag
seg000:00000008                 lea     edi, flag
seg000:0000000E                 cld
seg000:0000000F loc_F:                                  ; CODE XREF: sub_0+32↓j
seg000:0000000F                 lodsb
seg000:00000010                 test    al, al
seg000:00000012                 jz      short loc_34
seg000:00000014                 bt      ax, 0
seg000:00000019                 jb      short loc_25
seg000:0000001B                 mov     bx, 6Dh ; 'm'
seg000:0000001F                 mul     bl
seg000:00000021                 xor     al, 0EFh
seg000:00000023                 jmp     short loc_2D
seg000:00000025 loc_25:                                 ; CODE XREF: sub_0+19↑j
seg000:00000025                 mov     bx, 6Bh ; 'k'
seg000:00000029                 xor     al, 0FFh
seg000:0000002B                 mul     bl
seg000:0000002D                 add     dl, al
seg000:0000002F                 mov     eax, edx
seg000:00000031                 stosb
seg000:00000032                 jmp     short loc_F
seg000:00000034                 jmp     short loc_34
seg000:00000034 sub_0           endp

seg000:00000036 flag            db  94h                 ; DATA XREF: sub_0+2↑o
seg000:00000036                                         ; sub_0+8↑o
seg000:00000037                 db 78h
seg000:00000038                 db 0DEh
seg000:00000039                 db 0C2h, 0D0h, 0FCh
seg000:0000003C                 dd 0B36B32AEh, 5BD01E3Eh, 26F6C63Bh, 423C8A06h, 761107F4h
seg000:0000003C                 dd 0F111E156h, 0E413B550h, 0F874C696h, 9F4108D8h
seg000:00000060                 db 0DFh
seg000:00000061                 db  35h ; 5
seg000:00000062                 db    0
seg000:00000062 seg000          ends
```

Поскольку алгоритм снова очень простой, переведем его в питон:

```python
_1 = lambda j: ((j * 0x6d) & 0xff) ^ 0xef
_2 = lambda j: ((j ^ 0xff) * 0x6b) & 0xff
dl = 0

for i in range(len(flag)):
    if i & 0b1:
        dl = (_2(flag[i]) + dl) & 0xff
    else:
        dl = (_1(flag[i]) + dl) & 0xff
    flag[i] = dl
```

### Решение

```python
flag = list(map(lambda x: int(x, 16), '''94 78 DE C2 D0 FC AE 32 6B B3 3E 1E D0 5B 3B C6 F6 26  06 8A 3C 42 F4 07 11 76 56 E1 11 F1 50 B5 13 E4 96 C6 74 F8 D8 08 41 9F DF 35 00'''.split()))

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
```

