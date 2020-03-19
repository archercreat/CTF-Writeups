# Just Rust (41 solves)

> Clam really enjoys writing in C, but he realizes that he'll have to learn another language eventually. After all, he's grown pretty rusty after only programming in C for a year. So, he decided to write a program to create some ASCII art from user input. He also provided a sample output!
>
> Author: aplet123

*output.txt*:

```
What do you want to encode?
[REDACTED]
CCHJEHMK
CFKJCEOL
FOJLMOJJ
BDN@H@BA
ODMJHFCJ
MOOKMOOO
OOAOFOGI
@@@@@@@@
```

The binary is written in rust but has very simple encoding algorithm.

Our job is to find initial input.

The encoding algorithm:

```python
def algo(inp):
    out = [0x40 for i in range(72)]

    for i in range(len(inp)):
        t = i
        x = i >> 3
        for j in range(8):
            out[8 * j + (t & 7)] |= ((1 << (j & 7)) & inp[i]) >> (j & 7) << (x & 7)
            t += 1
    print(''.join(map(chr, out)))
```

Solution:

```python
from z3 import *
import sys

def find_all_possible(s):
    while s.check() == sat:
        model = s.model()
        block = []
        out = ''
        for i in range(32):
            c = globals()['b%i' % i]
            out += chr(model[c].as_long())
            block.append(c != model[c])
        s.add(Or(block))
        print(out)

def main():
    s = Solver()
    out = [0x40 for i in range(72)]
    for i in range(32):
        globals()['b%d' % i] = BitVec('b%d' % i, 8)
        t = i
        x = i >> 3
        for j in range(8):
            out[8 * j + (t & 7)] |= ((1 << (j & 7)) & globals()['b%d' % i]) >> (j & 7) << (x & 7)
            t += 1

    s.add(globals()['b0'] == ord('a'))
    s.add(globals()['b1'] == ord('c'))
    s.add(globals()['b2'] == ord('t'))
    s.add(globals()['b3'] == ord('f'))
    s.add(globals()['b4'] == ord('{'))

    for i in range(64):
        s.add(out[i] == ord(flag[i]))

    find_all_possible(s)


if __name__ == "__main__":
    sys.exit(main())
```

yields the flag

```bash
actf{b1gg3r_4nd_b4dd3r_l4ngu4g3}
```

