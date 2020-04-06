# Sora (226 solves)

> This obnoxious kid with spiky hair keeps telling me his key can open all doors. Can you generate a key to open this program before he does? Connect to `challenges.auctf.com 30004` Author: nadrojisk



check function:

```c++
__int64  check(char *input)
{
  int i;

  for ( i = 0; i < strlen(secret); ++i )
  {
    if ( (8 * input[i] + 19) % 61 + 65 != secret[i] )
      return 0;
  }
  return 1;
}
```



### Solution:

I wrote keygen for this challenge:

```python
from z3 import *
import sys

secret = 'aQLpavpKQcCVpfcg'
flag_len = len(secret)

def find_all_posible_solutions(s):
    while s.check() == sat:
        model = s.model()
        block = []
        out = ''
        for i in range(flag_len):
            c = globals()['b%i' % i]
            out += chr(model[c].as_long())
            block.append(c != model[c])
        s.add(Or(block))
        print(out) 

def main():
    s = Solver()

    for i in range(flag_len):
        c = globals()['b%d' % i] = BitVec('b%d' % i, 32)
        s.add(c > 32, c < 127)
        s.add((8 * c + 19) % 61 + 65 == ord(secret[i]) )

    find_all_posible_solutions(s)



if __name__ == "__main__":
    sys.exit(main())
```

Submitting any of them will give the flag:

```bash
$ nc challenges.auctf.com 30004
Give me a key!
try_7o"%rea."0(G
auctf{that_w@s_2_ezy_29302}
```

