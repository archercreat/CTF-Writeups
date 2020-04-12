# Райтап на MSKCTF 2020

Ниже будет описано решение всех тасков из категории `RE`, которые я сделал во время mskctf 2020.


## CDKey
> Can you crack this program?
> 

Дан `cdkey.exe`, по иконке ехешника и его размеру (8 мб) можно догадаться, что это собранный с помощью `py2exe` питоновский скрипт.

Чтобы достать исходный скрипт - идем [сюда](https://github.com/countercept/python-exe-unpacker) и скачиваем репу.

Запускаем `pyinstractor.py`, он распаковывает весь архив. Среди файлов можно найти файл под названием `keycheck`. 

С помощью `uncompyle6` переводим его обратно в питоновский скрипт. (Перед этим нужно добавить `42 0d 0d 0a 00 00 00 00 00 00 00 00 00 00 00 00` в начало файла)

Получаем скрипт:

```python
import sys, functools, hashlib
ALPHABET = 'ZAC2B3EF4GH5TK67P8RS9WXY'

def strtoint(s):
    return functools.reduce(lambda x, y: x * len(ALPHABET) + y, map(ALPHABET.index, s), 0)


def check_key(key):
    parts = key.split('-')
    if len(parts) != 4:
        return False
    elif not all(len(part) == 5 for part in parts):
        return False
    elif not all(c in ALPHABET for part in parts for c in part):
        return False
    else:
        expected_checksum = int.from_bytes(hashlib.blake2b('-'.join(parts[::2]).encode()).digest(), 'big')
        expected_checksum %=  len(ALPHABET) ** len(''.join(parts[1::2]))
        checksum = strtoint(''.join(parts[1::2]))
        return expected_checksum == checksum


if __name__ == '__main__':
    print(check_key(sys.argv[1]))

```

В скрипте сначала проверяется формат ключа `XXXXX-XXXXX-XXXXX-XXXXX`, так же каждый символ должен находиться в `ALPHABET`. Потом берется хэш от `0` и `2` части и сравнивается с `1` и `3` частью переведенной в `strtoint`.


#### Решение:

Хэшируем рандомную строчку, например `XXXXX-YYYYY` (это 0 и 2 часть в ключе), получаем `27573412365809`

Теперь нужно найти такую строку, которая после `strtoint` вернет это значение.

Для этого используем z3:

```python
import sys
from z3 import *
ALPHABET = 'ZAC2B3EF4GH5TK67P8RS9WXY'


def strtoint(s):
    out = 0
    for i in s:
        pos = ALPHABET.find(i)
        out = (out * len(ALPHABET)) + pos
    return out

def main():
    s  = Solver()
    ans = 27573412365809
    out = 0
    
    for i in range(10):
        # define BitVector
        c = globals()['b%d' % i] = BitVec('b%d' % i, 128)
        # add constraints
        s.add(c >= 0, c < len(ALPHABET))
        # strtoint
        out = (out * len(ALPHABET)) + c

    s.add(out == ans)
    
    if s.check() == sat:
        model = s.model()
        out = ''
        # if model was found
        for i in range(10):
            c = globals()['b%d' % i]
            out += ALPHABET[model[c].as_long()]

    print(out)
    assert strtoint(out) == ans

if __name__ == "__main__":
    sys.exit(main())

```

Получаем `HH5W7ZC5T8`. В этом случае ключ будет - `XXXXX-HH5W7-YYYYY-ZC5T8`. Запихиваем в прогу, она делает реквест на сервак с нашим ключем и возвращает флаг.

`MSKCTF{OLDER_REAL_WORLD_CDKEY_CHECKS_ARE_ACTUALLY_LIKE_THIS}`


## MSKCTF++
> Мы разработали свой язык! Решили назвать его скромно: MSKCTF++.
> 
>В этом языке каждая команда занимает 1 символ. Есть бесконечная лента памяти, состоящая из восьмибитных ячеек. >Таким образом, каждая ячейка может хранить числа от 0 до 255 включительно. Есть пишущая головка, позволяющая >работать с ячейкой. Изначально она указывает на ячейку по адресу 0. Все ячейки изначально равны 0.
>
>Есть 8 команд:
>
>    M — сдвинуть пишущую головку вправо (прибавить к адресу 1)
>
>    S — сдвинуть пишущую головку влево, но не левее нулевой ячейки (вычесть из адреса 1)
>
>    K — прибавить к текущей ячейке 1 (при переполнении она станет равна 0)
>
>    C — вычесть из текущей ячейки 1 (при переполнении она станет равна 255)
>
>    T — напечатать значение текущей ячейки по таблице ASCII
>
>    F — прочитать символ со стандартного ввода и занести его ASCII-код в текущую ячейку
>
>    { — начать цикл
>
>    } — закончить цикл, то есть прыгнуть на начало этого цикла, если текущая ячейка не равна 0
>
>Циклы могут быть вложенными.
>
>Язык полностью реализован, интерпретатор находится в файле eval.py.
>
>Разработчик языка написал и тестовую программу для него prog.txt. Кажется, она выводит что-то интересное, но что?

Если запустить скрипт, то он очень долго будет выписывать флаг. Очевидно наша задача оптимизировать это.
По описанию можно [догадаться](https://ru.wikipedia.org/wiki/Brainfuck), что это язык брейнфак. 

Приведем его в "читабельный" вид:

```python
raw = open('prog.txt').read()

raw = raw.replace('M','>')
raw = raw.replace('S','<')
raw = raw.replace('K','+')
raw = raw.replace('C','-')
raw = raw.replace('T','.')
raw = raw.replace('F',',')
raw = raw.replace('{','[')
raw = raw.replace('}',']')

print(raw)
```

Теперь найдем онлайн интерпритатор и запустим его. Я нашел довольно быстрый, который сумел за 20-30 минут выписать 
`Welcome! Here is your flag: MSKCTF{LolKek`

Дальше я просто попробовал подставить `MSKCTF{LolKekCheburek}` и он подошел. ¯\\_(ツ)_/¯


## Simple

>У нас есть очень простая виртуальная машина с очень большими возможностями. Для этой виртуальной машины мы написали очень хорошую программу для шифрования информации, которой воспользовался очень плохой человек. Если вы поможете нам восстановить эти очень важные данные, было бы очень кстати!
> task.raw
> vm
> output.txt
> 

Как написано в таске, нужно зареверсить виртуальную машину. Так же, установив переменную окружения `DEBUG`, мы еще и получим дебаг принты.

```c++
if ( getenv("DEBUG") )
__printf_chk(1LL, "%04x - Parsing OpCode Hex:%02X\n", a1->i, (unsigned int)v4);
```

А вот как выглядит вывод:
```
0000 - Parsing OpCode Hex:30
STRING_STORE(Register 0) = 'Input one line
> '
0015 - Parsing OpCode Hex:01
STORE_INT(Reg:01) => 0042 [Hex:002a]
0019 - Parsing OpCode Hex:31
STRING_PRINT(Register 0)
[stdout] register R00 => Input one line
> 
001b - Parsing OpCode Hex:80
001c - Parsing OpCode Hex:71
POP(Register 0) => 0074
001e - Parsing OpCode Hex:41
CMP_IMMEDIATE(Register:0 vs 10 [Hex:000A])
0022 - Parsing OpCode Hex:11
JUMP_Z(Offset:69 [Hex:0045]
0025 - Parsing OpCode Hex:82
0028 - Parsing OpCode Hex:82
002b - Parsing OpCode Hex:70
PUSH(Register 1 [=002a])
002d - Parsing OpCode Hex:81
```

Можно заметить, что описание некоторых опкодов отсутствует, поэтому узнать точно что происходит невозможно.

#### Решение:

Решение довольно простое, запускаем в дебаггер (для удобства я отлаживал идой удаленно через вм).

Ставим точку остановки после `getc` и видим, что программа берет наш ввод посимвольно. 
Ставим точки остановки во все ячейки памяти, куда кладется наш введенный символ или какое-то значение, которое от него зависит.

Немного потрейсив можно заметить как каждый символ перемножается с какими-то значениями а затем выписывается хексом в stdout. 

```python
t = 0x2a
i = 0
while password[i] != 0xa:
    out = ((t * inp[i] + 0xb3) * inp[i] + 0x3039) & 0xffff
    print(hex(out))
    t = out ^ inp[i]
    i += 1
```

После чего берется следующий символ и все повторяется.

Легко можно написать брутфорс:


```python
#         M       S        K        C      T       F      {
flag = [0x32CA, 0x1D21, 0x628C, 0x7291, 0x2715, 0xB94F, 0xAB1B, 0xB43B, 0x071D, 0xA7CF, 0xB501, 0xEE1E, 0xBC8B, 0xAE1C, 0x106D, 0x7E89, 0xACCD, 0x5251, 0x6DDA, 0x1679, 0x4963, 0x01F5, 0xE1C1, 0xB6DC, 0x10B5, 0xEBF9]

z = 0x2a
out = ''
for k in range(len(x)):
    # bruteforce charset
    for i in range(32, 127):
        t = ((z * i + 0xb3) * i + 0x3039) & 0xffff
        if t == flag[k]:
            out += chr(i)
            z = t ^ i
            break
print(out)
```

`MSKCTF{very_simple_indeed}`

---


**UPDATE**: А теперь немного уличной магии. Я покажу как можно было решить это элегантно и как, в принципе, я решаю все таски с виртуальными машинами.

Для решения я использую [Triton](https://github.com/JonathanSalwan/Triton) Фреймворк, который дает возможноость символьного эмулирования программы.

Собственно, что можно сделать с помощью Тритона? Ну, для начала, давайте выпишем все инструкции, которые как-то зависят от нашего ввода или как-то с ним работают:
```asm
$ python3 solve-vm.py vm
0x135d: movzx eax, ax                               ; ax - наш введенный символ
0x1360: mov dword ptr [rbx + rdx*4 + 0x8c0], eax    ; куда-то кладется
0x41db: mov r12d, dword ptr [rbx + rdx*4 + 0x8c0]   ; оттуда достается
0x4219: mov dword ptr [rbp], r12d                   ; кладется на стэк
0x2405: mov eax, dword ptr [rbp]                    ; достается со стэка
0x2408: cmp r12d, eax                               ; сравнивается с концом строки
0x240b: jne 0x2419
0x4d11: mov eax, dword ptr [rsi]
0x144f: cdqe
0x1451: imul r13, rax
0x1455: lea rdx, [r14 + r13]
0x1459: imul rax, rdx            ; какая-то математика с нашим символом
0x1469: add r12d, eax
0x146c: movzx r12d, r12w
0x1470: mov dword ptr [rbx + rdx*4 + 0x8c0], r12d
0x2b38: mov ebp, dword ptr [rbp]
0x2b76: mov dword ptr [rbx + rdx*4 + 0x8c0], ebp
0x41db: mov r12d, dword ptr [rbx + rdx*4 + 0x8c0]
0x4219: mov dword ptr [rbp], r12d
0x41db: mov r12d, dword ptr [rbx + rdx*4 + 0x8c0]
0x4219: mov dword ptr [rbp], r12d
0x3c27: mov r12d, dword ptr [r12]
0x3c36: xor r12d, dword ptr [r13]        ; xor
0x3c3c: test r12d, r12d
0x3c3f: mov dword ptr [rbp], r12d
0x3c43: sete al
0x3c4d: mov word ptr [rbx + 0xa0], ax
0x1d05: mov r13d, dword ptr [rbx]       ; на этом моменте в r13d лежит переменная
0x1d98: mov edx, r13d                   ; которая выписывается хексом в stdout
```

Давайте теперь посмотрим на символьное представление регистра `r13d` по адресу 0x1d98:
```python
if instruction.getAddress() == 0x1d98:
    r13 = ctx.getSymbolicRegister(ctx.registers.r13)
    if r13 is not None:
        print(r13.getAst())
```

```bash
$ python3 solve-vm.py vm
((((ref_13955) << 8 | ref_13956) << 8 | ref_13957) << 8 | ref_13958)
```

Нам это ни о чем не говорит, потому что мы не знаем чему равны `ref_` переменные.
Но, благодаря символьному вычислению и смт солверу, мы можем найти чему должен равняться наш введенный символ, чтобы получилось число, например, `0x32CA` (первый хекс символ из флага).

```python
if instruction.getAddress() == 0x1d98:
    r13 = ctx.getSymbolicRegister(ctx.registers.r13)
    if r13 is not None:
        print(r13.getAst())
        pco = ctx.getPathPredicate()
        ast = ctx.getAstContext()
        mod = ctx.getModel(ast.land(
            [pco, 
            r13.getAst() == flag[0],
            ast.variable(ctx.getSymbolicVariable(0))  <= 0x7e]))
        print(mod)
```

```bash
$ python3 solve-vm.py vm
((((ref_13955) << 8 | ref_13956) << 8 | ref_13957) << 8 | ref_13958)
{0: SymVar_0:64 = 0x4D}
```
`0x4d` == `M` и это очевидно, потому что флаг начинается с `MSKCTF{`. 

Таким образом мы можем восстановить исходный флаг:
```bash
$ python3 solve-vm.py vm
{0: SymVar_0:64 = 0x4D}
{0: SymVar_0:64 = 0x53}
{0: SymVar_0:64 = 0x4B}
{0: SymVar_0:64 = 0x43}
{0: SymVar_0:64 = 0x54}
{0: SymVar_0:64 = 0x46}
{0: SymVar_0:64 = 0x7B}
{0: SymVar_0:64 = 0x76}
{0: SymVar_0:64 = 0x65}
{0: SymVar_0:64 = 0x72}
{0: SymVar_0:64 = 0x79}
{0: SymVar_0:64 = 0x5F}
{0: SymVar_0:64 = 0x73}
{0: SymVar_0:64 = 0x69}
{0: SymVar_0:64 = 0x6D}
{0: SymVar_0:64 = 0x70}
{0: SymVar_0:64 = 0x6C}
{0: SymVar_0:64 = 0x65}
{0: SymVar_0:64 = 0x5F}
{0: SymVar_0:64 = 0x69}
{0: SymVar_0:64 = 0x6E}
{0: SymVar_0:64 = 0x64}
{0: SymVar_0:64 = 0x65}
{0: SymVar_0:64 = 0x65}
{0: SymVar_0:64 = 0x64}
{0: SymVar_0:64 = 0x7D}
MSKCTF{very_simple_indeed}
executed in 30 sec
```

## Flash Reverse

>We recieved a link to a strange SWF file and got the message "You're interested in turning on the sound and watching it to the end"
>


Дан линк, который ведет на браузерное флеш приложение. С помощью браузерного дебаггера достаем ссылку откуда подгружается флеш контент и скачиваем его.

Для анализа будем использовать [ffdec](https://github.com/jindrapetrik/jpexs-decompiler).

Открываем `Container.swf` в ffdec и видим, что файл зашифрован. В `init` функции происходит расшифровка xor с 51 `BinaryData`, а потом ее загрузка.

```actionscript
private function init(e:Event = null) : void
{
 removeEventListener(Event.ADDED_TO_STAGE,this.init);
 this._loaderContext = new LoaderContext(false,ApplicationDomain.currentDomain);
 this._loaderContext.allowCodeImport = true;
 var loader:Loader = new Loader();
 this.addChild(loader);
 var someFile:ByteArray = new this._content();
 someFile.position = 0;
 var sFirstBytes:String = someFile.readUTFBytes(3);
 if(sFirstBytes != "FWS" && sFirstBytes != "CWS")
 {
    someFile.position = 0;
    this.decryptFile(someFile);
 }
 loader.loadBytes(someFile,this._loaderContext);
}

private function decryptFile(file:ByteArray) : void
{
 file.position = 0;
 var i:uint = 0;
 var nLen:uint = file.length;
 while(i < nLen)
 {
    file[i] = file[i] ^ 51;
    i++;
 }
}
```

Сохраняем зашифрованные данные на диск, расшифровываем и закидываем в ffdec

```python
raw = open('1_MainTimeline_focus_loader__content.bin','rb').read()
out = open('out.swf','wb')

for i in raw:
    out.write((i ^ 51).to_bytes(1, 'big'))
out.close()
```

В расшифрованном swf файле, в мейне можно найти интересную строчку
` private var _Ipo1W:String = "34c5f166f6abb229ee092be1e7e92ca71434bcb1a27ba0664cd2fea834d85927";`, а ниже вот такую строчку:

```actionscript
if(this._Ipo1W == SHA256.computeDigest(_foGbe))
```
где `_foGbe` наша введенная строка. 

Быстрый гугл показал, что sha256 строка - `rickroll`. Поэтому вводим ее на сайте и смотрим прикольную анимацию из звездных войн, которая выписывает флаг

`MSKCTF{hello_from_the_past}`

