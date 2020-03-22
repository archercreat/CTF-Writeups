# static EYELESS (44 solves)

> Maths, Maths, Maths,.... 
>
> Authors : KERRO & Anis_Boss



The main function is a bit obfuscated:

```c++
void main(int a1, char **a2, char **a3)
{
  double __21; // xmm3_8
  __int64 v4; // kr00_8
  int i; // [rsp+10h] [rbp-230h]
  int j; // [rsp+10h] [rbp-230h]
  int check; // [rsp+14h] [rbp-22Ch]
  __int64 v8; // [rsp+20h] [rbp-220h]
  __int64 v9; // [rsp+28h] [rbp-218h]
  __int64 v10; // [rsp+28h] [rbp-218h]
  __int64 v11; // [rsp+28h] [rbp-218h]
  int xor_ar[52]; // [rsp+50h] [rbp-1F0h]
  char key[200]; // [rsp+120h] [rbp-120h]
  char s[56]; // [rsp+1F0h] [rbp-50h]
  unsigned __int64 v15; // [rsp+228h] [rbp-18h]

  memset(key, 0, sizeof(key));
  key[0]   = 0xD1;
  key[4]   = 0x1E;
  key[8]   = 0xDB;
  key[12]  = 0xFB;
  key[16]  = 0x74;
  key[20]  = 0xCB;
  key[24]  = 0x15;
  key[28]  = 0xDD;
  key[32]  = 0xFA;
  key[36]  = 0x75;
  key[40]  = 0xD9;
  key[44]  = 0x4B;
  key[48]  = 0xDA;
  key[52]  = 0xE8;
  key[56]  = 0x73;
  key[60]  = 0xD1;
  key[64]  = 0x4F;
  key[68]  = 0xCC;
  key[72]  = 0xE7;
  key[76]  = 0x36;
  key[80]  = 0xCC;
  key[84]  = 0x4E;
  key[88]  = 0xE7;
  key[92]  = 0xFC;
  key[96]  = 0x36;
  key[100] = 0xC1;
  key[104] = 0x10;
  key[108] = 0x8D;
  key[112] = 0xAF;
  key[116] = 0x7B;
  key[120] = 0xA8;
  __21 = 21();
  v9 = (((*key * (((0x1E - 1.0) * 251() + 58.0) * *&key[16] + 110) + 141.0) * __21 + 20.0) * (*&key[4] - 20)) >> (key[4] - 22);
  puts("Hello REVERSER!");
  v10 = 49406 * v9 * (ptrace(PTRACE_TRACEME, 0LL, 0LL, 0LL) + 1);
  printf("Give me the passcode:");
  v4 = v10;
  v11 = v10 / 0x100;
  v8 = v4 / 0x100;
  fgets(s, 49, stdin);
  check = 0;
  for ( i = 0; i < strlen(s); ++i )
  {
    if ( !v8 )
      v8 = v11;
    xor_ar[i] = v8 ^ s[i];
    v8 >>= 8;
  }
  for ( j = 0; j <= 29; ++j )
    check += xor_ar[j] ^ *&key[4 * j] | 1;
  if ( check == -(ptrace(PTRACE_TRACEME, 0LL, 0LL, 0LL)
                * (*&key[4]
                 + (0x123456 << (key[4] - 26) >> (key[0] + 72))
                 - (0x654321 << (key[4] - 26) >> (key[0] + 72))
                 + 3)) )
    puts("Good job!");
  else
    printf("NOOOOOOOO");
}
```



After some debugging I came up with this algorithm:

```python
key = [
    0xd1, 0x1e, 0xdb, 0xfb, 
    0x74, 0xcb, 0x15, 0xdd, 
    0xfa, 0x75, 0xd9, 0x4b, 
    0xda, 0xe8, 0x73, 0xd1, 
    0x4f, 0xcc, 0xe7, 0x36, 
    0xcc, 0x4e, 0xe7, 0xfc, 
    0x36, 0xc1, 0x10, 0x8d, 
    0xaf, 0x7b, 0xa8, 0x00]

magic = [
    0xa2, 0x7b, 0xb8, 0x8e, 
    0x06, 0xa2, 0x7b, 0xb8, 
    0x8e, 0x06, 0xa2, 0x7b, 
    0xb8, 0x8e, 0x06, 0xa2, 
    0x7b, 0xb8, 0x8e, 0x06, 
    0xa2, 0x7b, 0xb8, 0x8e, 
    0x06, 0xa2, 0x7b, 0xb8, 
    0x8e, 0x06, 0xa2, 0x7b]

flag_len = 30

def algo():
    inp = str(input())
    check = 0
    for i in range(len(inp)):
        check += (magic[i] ^ ord(inp[i]) ^ key[i]) | 1
    
    if check == 30:
        print('goodboy')
    else:
        print('no :(')
```



Now we use z3 to find the flag:

```python
from z3 import *
import sys

key = [
    0xd1, 0x1e, 0xdb, 0xfb, 
    0x74, 0xcb, 0x15, 0xdd, 
    0xfa, 0x75, 0xd9, 0x4b, 
    0xda, 0xe8, 0x73, 0xd1, 
    0x4f, 0xcc, 0xe7, 0x36, 
    0xcc, 0x4e, 0xe7, 0xfc, 
    0x36, 0xc1, 0x10, 0x8d, 
    0xaf, 0x7b, 0xa8, 0x00]


magic = [
    0xa2, 0x7b, 0xb8, 0x8e, 
    0x06, 0xa2, 0x7b, 0xb8, 
    0x8e, 0x06, 0xa2, 0x7b, 
    0xb8, 0x8e, 0x06, 0xa2, 
    0x7b, 0xb8, 0x8e, 0x06, 
    0xa2, 0x7b, 0xb8, 0x8e, 
    0x06, 0xa2, 0x7b, 0xb8, 
    0x8e, 0x06, 0xa2, 0x7b]

flag_len = 30

def main():
    s = Solver()
    check = 0
    for i in range(flag_len):
        globals()['b%d' % i] = BitVec('b%d' % i, 32)
        s.add(globals()['b%d' % i] > 32, globals()['b%d' % i] < 127)

    for i in range(flag_len):
        c = magic[i] ^ globals()['b%d' % i]
        check +=  (c ^ key[i]) | 1

    s.add(globals()['b0'] == ord('s'))
    s.add(globals()['b1'] == ord('e'))
    s.add(globals()['b2'] == ord('c'))
    s.add(globals()['b3'] == ord('u'))
    s.add(globals()['b4'] == ord('r'))
    s.add(globals()['b5'] == ord('i'))
    s.add(globals()['b6'] == ord('n'))
    s.add(globals()['b7'] == ord('e'))
    s.add(globals()['b8'] == ord('t'))
    s.add(globals()['b9'] == ord('s'))
    s.add(globals()['b10'] == ord('{'))
    s.add(globals()['b29'] == ord('}'))

    s.add(check == 30)

    find_all_posible_solutions(s)
    
    

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

if __name__ == "__main__":
    sys.exit(main())
```

The script yields bunch of flags...

```
securinets{0cftr4uh0o4_r1bk4!}
securinets{0bftr4ui1n4^r0bk4!}
securinets{0bfur4uh0o4_s1ck4!}
securinets{0cfur5ui0n4_s0bj4!}
securinets{0cftr4uh0n4^r1ck4!}
securinets{0bftr4ui1o4_r0ck4!}
securinets{0cfur5uh1n4_s1cj4!}
securinets{0cfur4ui0o4^s0ck4!}
securinets{0bftr4uh1o4^r1bj4!}
securinets{0cftr4ui1n4_r0bj4!}
securinets{0bfur4uh0o4^s1cj4!}
```

So, we should add more constraints...

```python
s.add(globals()['b11'] == ord('0'))
s.add(globals()['b12'] == ord('b'))
s.add(globals()['b13'] == ord('f'))
s.add(globals()['b14'] == ord('u'))
s.add(globals()['b15'] == ord('s'))

s.add(globals()['b14'] == ord('u'))
s.add(globals()['b22'] == ord('_'))
s.add(globals()['b23'] == ord('r'))
s.add(globals()['b24'] == ord('0'))
s.add(globals()['b25'] == ord('c'))
s.add(globals()['b26'] == ord('k'))
s.add(globals()['b27'] == ord('5'))
s.add(globals()['b28'] == ord('!'))
s.add(globals()['b29'] == ord('}'))
```

After that we still get tons of results but I somehow found that the flag is `securinets{0bfus4ti0n5_r0ck5!}`

¯\\_(ツ)_/¯