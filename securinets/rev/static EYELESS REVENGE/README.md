# static EYELESS REVENGE (11 solves)

> They can't see me Roliiiiiiing... 
>
> Authors : KERRO & Anis_Boss



This time we are given binary written in go..

main:

```c++
void __noreturn check()
{
  int v0; // eax
  int i; // [rsp+0h] [rbp-380h]
  int j; // [rsp+4h] [rbp-37Ch]
  int v3; // [rsp+8h] [rbp-378h]
  int k; // [rsp+Ch] [rbp-374h]
  int l; // [rsp+10h] [rbp-370h]
  int _check; // [rsp+14h] [rbp-36Ch]
  int m; // [rsp+18h] [rbp-368h]
  __int64 v8; // [rsp+20h] [rbp-360h]
  int rand[52]; // [rsp+30h] [rbp-350h]
  int v10[52]; // [rsp+100h] [rbp-280h]
  int v11[50]; // [rsp+1D0h] [rbp-1B0h]
  char hello[56]; // [rsp+2A0h] [rbp-E0h]
  char hello_1[56]; // [rsp+2E0h] [rbp-A0h]
  char buffer; // [rsp+320h] [rbp-60h]
  _BYTE v15[7]; // [rsp+321h] [rbp-5Fh]
  _BYTE inp[5]; // [rsp+32Bh] [rbp-55h]
  unsigned __int64 v17; // [rsp+368h] [rbp-18h]

  v17 = __readfsqword(0x28u);
  memset(v11, 0, sizeof(v11));
  v11[0] = 0xF6;
  v11[1] = 0x9B;
  v11[2] = 5;
  v11[3] = 0xFE;
  v11[4] = 0x36;
  v11[5] = 0xA3;
  v11[6] = 0x3E;
  v11[7] = 0x93;
  v11[8] = 0xC8;
  v11[9] = 0x2C;
  v11[10] = 0xB2;
  v11[11] = 0x6E;
  v11[12] = 0x33;
  v11[13] = 0x7C;
  v11[14] = 0x93;
  v11[15] = 0x2A;
  v11[16] = 0xC4;
  v11[17] = 0x6E;
  v11[18] = 0xA4;
  v11[19] = 0xF;
  v11[20] = 0x8C;
  v11[21] = 0xD8;
  v11[22] = 0x7D;
  v11[23] = 0xDF;
  v11[24] = 0xAE;
  v11[25] = 0xC6;
  v11[26] = 0x7C;
  v11[27] = 0xD7;
  v11[28] = 0xEF;
  v11[29] = 0xA5;
  v11[30] = 0x71;
  v11[31] = 0x48;
  v11[32] = 0xC8;
  v11[33] = 0x49;
  v11[34] = 0x3A;
  v11[35] = 0xB2;
  v11[36] = 0x78;
  v11[37] = 0xF5;
  v11[38] = 0xCC;
  v11[39] = 0xBE;
  v11[40] = 0x9A;
  v11[41] = 0x47;
  v11[42] = 0xD2;
  v11[43] = 0x87;
  v11[44] = 0x10;
  v11[45] = 0xFD;
  v11[46] = 0x78;
  v11[47] = 0x1D;
  *(_QWORD *)hello = '\xCE\x8B\x83\x81\x8D\x82\x8B\xB9';
  *(_QWORD *)&hello[8] = '\xBC\xBB\xAD\xAB\xBD\xCE\x81\x9A';
  *(_QWORD *)&hello[16] = '\xBA\xAD\xCE\xBD\xBA\xAB\xA0\xA7';
  *(_QWORD *)&hello[24] = '\xCF\xA8';
  *(_QWORD *)&hello[32] = '\0';
  *(_QWORD *)&hello[40] = '\0';
  *(_WORD *)&hello[48] = '\0';
  for ( i = 0; i < strlen(hello); ++i )
    hello[i] ^= 0xEEu;
  puts_0((__int64)hello);
  *(_QWORD *)hello_1 = '\xCE\x8B\x83\xCE\x8B\x98\x87\xA9';
  *(_QWORD *)&hello_1[8] = '\x9D\x9D\x8F\x9E\xCE\x8B\x86\x9A';
  *(_QWORD *)&hello_1[16] = '\xD4\x8B\x9D\x8F\x9C\x86\x9E';
  *(_QWORD *)&hello_1[24] = '\0';
  *(_QWORD *)&hello_1[32] = '\0';
  *(_QWORD *)&hello_1[40] = '\0';
  *(_WORD *)&hello_1[48] = '\0';
  for ( j = 0; j < strlen(hello_1); ++j )
    hello_1[j] ^= 0xEEu;
  puts((char)hello_1);
  fgets(&buffer, 70LL, off_6FF088);
  v3 = 0;
  while ( buffer != 's' )
    ++v3;
  v8 = 0xDEADBEEFLL * (int)sub_400488((__int64)v15, (__int64)"ecurinets{", 10LL);
  while ( v8 )
    puts((char)" SECURINETS FTW! ");
  seed(buffer);
  for ( k = 0; k <= 49; ++k )
  {
    v0 = rand();
    rand[k] = (unsigned __int8)to_char(v0);
  }
  for ( l = 0; l < strlen(inp); ++l )
    v10[l] = rand[l] ^ (char)inp[l];
  _check = 0;
  for ( m = 0; m <= 47; ++m )
    _check += v11[m] ^ v10[m];
  if ( _check )
    puts_0((__int64)"NOOOOOOO");
  else
    puts((char)"Good Job!\nsubmit with\n%s", &buffer);
  sub_4240C0(0LL);
}
```

First, program checks if our input starts with **securinets{**, after that it sends 's' to srand as a seed

After that if checks:

**input[i] ^ key[i] ^ rand_seq[i] == 0**

Solution:

```python

import sys
from z3 import *

key = [
    0xf6, 0x9b, 0x05, 0xfe,
    0x36, 0xa3, 0x3e, 0x93,
    0xc8, 0x2c, 0xb2, 0x6e,
    0x33, 0x7c, 0x93, 0x2a,
    0xc4, 0x6e, 0xa4, 0x0f,
    0x8c, 0xd8, 0x7d, 0xdf,
    0xae, 0xc6, 0x7c, 0xd7,
    0xef, 0xa5, 0x71, 0x48,
    0xc8, 0x49, 0x3a, 0xb2,
    0x78, 0xf5, 0xcc, 0xbe,
    0x9a, 0x47, 0xd2, 0x87,
    0x10, 0xfd, 0x78, 0xd1
]

# random seq given 's' as a seed
seq = [
    0x9f, 0xc4, 0x77, 0xcd, 
    0x02, 0xcf, 0x52, 0xea, 
    0x97, 0x4e, 0x81, 0x02, 
    0x02, 0x4f, 0xe5, 0x19, 
    0x9b, 0x5f, 0xca, 0x50,
    0xf9, 0xaa, 0x22, 0xb9, 
    0xdb, 0xb2, 0x09, 0xa5, 
    0xdc, 0xfa, 0x03, 0x7b, 
    0xbe, 0x7a, 0x48, 0xc1, 
    0x49, 0x9b, 0xab, 0xe1, 
    0xe9, 0x2c, 0xe3, 0xeb, 
    0x7c, 0xc8, 0x05, 0x17,
    0x27, 0xcf]

flag_len = 48

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
    check = 0
    for i in range(flag_len):
        globals()['b%d' % i] = BitVec('b%d' % i, 8)

    for i in range(flag_len):
        s.add(globals()['b%d' % i] ^ seq[i] ^ key[i] == 0)

    find_all_posible_solutions(s)
   

if __name__ == "__main__":
    sys.exit(main())

```

gives the flag `i_r34lly_b3l13v3_1n_ur_futur3_r3v3rs1ng_sk1ll5}`

