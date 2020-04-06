# Don't Break Me! (133 solves)

> I've been working on my anti-reversing lately. See if you can get this flag! Connect at `challenges.auctf.com 30005` Author: nadrojisk



We have to find the right password that after encryption == `SASRRWSXBIEBCMPX`

```c++
char* encrypt(char *s, int a2, int a3)
{
  size_t v3;
  _BYTE *v5; 
  size_t i;

  v3 = strlen(s);
  v5 = calloc(v3, 1u);
  for ( i = 0; strlen(s) > i; ++i )
  {
    if ( s[i] == 32 )
      v5[i] = s[i];
    else
      v5[i] = (a2 * (s[i] - 65) + a3) % 26 + 65;
  }
  return v5;
}
```



### Solution:

Simple bruteforce will do the trick.

```python
import sys
import string

flag = 'SASRRWSXBIEBCMPX'

charset = [ord(i) for i in string.ascii_letters + string.digits + '_']
    
def encrypt(f):
    return chr((17 * (f - 0x41) + 12) % 26 + 65)

def solve():
    out = ''
    for k in range(len(flag)):
        for i in charset:
            if encrypt(i) == flag[k]:
                print('found ', k)
                out += chr(i)
                break
    print(out)

if __name__ == "__main__":
    sys.exit(solve())

```

```bash
$ nc challenges.auctf.com 30005
54 68 65 20 6d 61 6e 20 69 6e 20 62 6c 61 63 6b 20 66 6c 65 64 20 61 63 72 6f 73 73 20 74 68 65 20 64 65 73 65 72 74 2c 20 61 6e 64 20 74 68 65 20 67 75 6e 73 6c 69 6e 67 65 72 20 66 6f 6c 6c 6f 77 65 64 2e
Input: cecffqcnbgsbyuln
auctf{static_or_dyn@mIc?_12923}
^C
```

