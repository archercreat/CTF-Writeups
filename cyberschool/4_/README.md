### 4 таск

сказано, что на флаг два раза сделали rot с неизвестным сдвигом по ascii символам.

Решение:

Пишем брутфорс rot от 0 до 255 два раза и если получаются символы в интервале от 32 до 127 (те, которые можно вывести на экран), сохраняем в файл.

```python
flag = 'fhkhshold<LFLNtfZbgX/+]]Z^*,,.111[\^2Z_Z[ZZ-*^[/))v'


def encrypt(text,s):
    result = ""
    # transverse the plain text
    for i in range(len(text)):
        char = text[i]
        result += chr((ord(char) + s) & 0xff)
    return result

f = open('out.txt', 'w')

for i in range(255):
    for j in range(255):
        b = False
        t = encrypt(flag, j)
        t = encrypt(t, i)
        for x in t:
            if ord(x) < 32 or ord(x) > 127:
                b = True
        if b:
            continue
        f.write(t + '\n')

f.close()

```

После чего находим часто повторяющуюся строку 

**morozovskCSMSU{main_62ddae1335888bce9afabaa41eb600}**