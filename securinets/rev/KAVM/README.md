# KAVM (12 solves)

>I think "K" stands for KERRO and "A" for Anis_Boss and you know the rest... :D 
>
>Authors : KERRO & Anis_Boss



We are given 32bit binary, the binary is packed with virtual machine. 

The dispatch function is simple. We fetch byte from bytecode and process it.

```c++
int main()
{
  int opcode;

  while ( next )
  {
    ++count;
    opcode = fetch_opcode();
    vm(opcode);
  }
  return 0;
}
```

I wont list vm code here, it is pretty simple.

Solution:

Place hardware breakpoints on access on our entered flag. Notice, that it is being xored with index of array.

The algo looks like this:

```python
def algo():
    out = ''
    inp = str(input())
    for i in range(len(inp)):
        out += chr(ord(inp[i]) ^ (flag_len - i))
    print(out)
```

After that it is being compared with hardcoded buffer.

full script:

```python
import sys
from binascii import unhexlify as ux

flag_len = 0x20
# hardcoded flag
flag = ux('53 7A 7D 68 6E 72 74 7C  6C 64 6D 63 79 4C 62 63 20 7B 3D 6E 78 3A 3A 67  57 75 36 66 6F 36 23 7C'.replace(' ', ''))

def main():
    out = ''
    for i in range(len(flag)):
        out += chr(flag[i] ^ (flag_len - i))
    print(out)

if __name__ == "__main__":
    sys.exit(main())
```

yields the flag:

`securinets{vm_pr0t3ct10n_r0ck5!}`