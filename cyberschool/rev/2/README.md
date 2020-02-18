## Второе задание

Нам удалось восстановить байты, которые хранились по метке `flag` после завершения программы: 248, 224, 150, 126, 44, 172, 101, 55, 191, 35, 55, 174, 12, 112, 124, 86,  222, 66, 160, 122, 2, 196, 40, 209, 229, 249, 93, 55, 141, 95, 74, 183,  253, 0

Код программы:

```asm
_start:
xor edx, edx
lea esi, [flag]
lea edi, [flag]
cld
_loop:
lodsb
test al, al
je _stop
mov bx, 223
mul bl
xor al, 0xA5
add dl, al
mov eax, edx
stosb
jmp _loop

_stop:
jmp _stop

flag: db 0 ; DATA EXPUNGED
```



Переведем код в питон:

```python
dl = 0
for i in range(len(flag)):
    if flag[i] == 0:
        break
    dl += (flag[i] * 223) & 0xff ^ 0xa5
    flag[i] = dl
```

То есть flag[i]  содержит сумму предыдущих операций с dl

### Решение:

```python
flag = [248, 224, 150, 126, 44, 172, 101, 55, 191, 35, 55, 174, 12, 112, 124, 86, 222, 66, 160, 122, 2, 196, 40, 209, 229, 249, 93, 55, 141, 95, 74, 183, 253, 0]
dl = 0
out = ''
for i in range(len(flag) - 1):
    for j in range(32, 127):		# brute force every printable char
        temp = (j * 223) & 0xff
        temp ^= 0xa5
        if (dl + temp) & 0xff == flag[i]:
            out += chr(j)
            dl += temp
            dl &= 0xff
            break

print(out)
```



