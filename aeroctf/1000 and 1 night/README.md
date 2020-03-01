# 1000 and 1 night

### Description:

```
I wrote all this manually in 1000 and 1 night.

It seems that the solution will take the same amount of time.

After connecting to the server, it will ask you for a token for a binary.

You need to enter the correct tokens for the requested files and you will receive a flag.

nc tasks.aeroctf.com 44324
```

We are given with 1001 binaries that ask for a token. Every binary has the same layout, the only difference is in constants in **check** function.

```c
int  main(int argc, const char **argv, const char **envp)
{
  int result; 
  _BYTE *buf; 

  setup(argc, argv, envp);
  printf("[?] Enter valid token: ");
  buf = malloc(0x40uLL);
  buf[(int)read(0, buf, 0x40uLL) - 1] = 0;
  if ( strlen(buf) == 32 )
  {
    if ( check(buf) )
      puts("[+] This is a valid token!");
    else
      puts("[-] Incorrect!");
    result = 0;
  }
  else
  {
    puts("[-] Incorrect!");
    result = 0x539;
  }
  return result;
}
```

```c
bool check(char *a1)
{
  __int64 s2; 
  __int64 v3; 
  __int64 v4; 
  __int64 v5; 
  int i; 

  s2 = 0x2673231825237276LL;
  v3 = 0x2373262077182774LL;
  v4 = 0x2025271873772577LL;
  v5 = 0x2375232776217420LL;
  for ( i = 0; i <= 31; ++i )
    a1[i] = ((a1[i] + 7) ^ 0x17) - 8;
  return memcmp(a1, &s2, 0x20uLL) == 0;
}
```



### Solution:

We use angr to automatically solve crackmes and save output to file. After 30~ mins we use pwntools to submit token to server.

```python
import angr
import claripy
import os
import sys
import binascii
from tqdm import tqdm
import logging

log_things = ["angr", "pyvex", "claripy", "cle"]
for log in log_things:
    logger = logging.getLogger(log)
    logger.disabled = True
    logger.propagate = False
    
files_path = os.path.join(os.getcwd(), 'files')

check_func = 0x4012a4
key_loc = 0x600000

def main(filename, f):
    key = claripy.BVS('key', 8*32)
    proj = angr.Project(os.path.join(files_path, filename))
    state = proj.factory.blank_state(addr=0x401219) # addr of check function
	
    # key is only in printable char range
    for c in key.chop(8):
        state.add_constraints(c >= 32)
        state.add_constraints(c <= 127)

    state.memory.store(key_loc, key)
    state.regs.rdi = key_loc
    state.regs.rax = key_loc
    simgr = proj.factory.simgr(state)
    simgr.explore(
        find=0x401230, # goodboy
        avoid=0x401222 # badboy
    )
    print(simgr)
    if simgr.found:
        out = simgr.found[-1].solver.eval(key, cast_to=bytes)
        print(out)
        f.write(f'{filename}\t{out.decode("utf-8")}\n')
    else:
        print(f'no token found for {filename}')
        f.write(f'{filename}\tNOTHING')

if __name__ == "__main__":
    with open('out.txt', 'w') as f:
        for file in tqdm(os.listdir(files_path)):
            main(file, f)

```

```python
from pwn import *
import sys
import re

def main(target):
    answers = open('out.txt').readlines()
    while True:  
        raw = r.recv()
        print(raw)
        binary_name = re.findall('<(.*)>', raw.decode())[0]
        for i in answers:
            if binary_name in i:
                r.sendline(i.split('\t')[-1].replace('\n',''))
                break

if __name__ == "__main__":
    r = remote('tasks.aeroctf.com', 44324)
    sys.exit(main(r))
```

Output from server:

```sh
b'Enter valid token to binary with name <704afe073992cbe4813cae2f7715336f>\nToken: '
b'Enter valid token to binary with name <fccb60fb512d13df5083790d64c4d5dd>\nToken: '
b'Enter valid token to binary with name <303ed4c69846ab36c2904d3ba8573050>\nToken: '
b'Enter valid token to binary with name <9f61408e3afb633e50cdf1b20de6f466>\nToken: '
b'Enter valid token to binary with name <fe7ee8fc1959cc7214fa21c4840dff0a>\nToken: '
b'Enter valid token to binary with name <46922a0880a8f11f8f69cbb52b1396be>\nToken: '
b'Enter valid token to binary with name <210f760a89db30aa72ca258a3483cc7f>\nToken: '
b'Enter valid token to binary with name <92cc227532d17e56e07902b254dfad10>\nToken: '
b'Enter valid token to binary with name <6855456e2fe46a9d49d3d3af4f57443d>\nToken: '
b'Enter valid token to binary with name <8c235f89a8143a28a1d6067e959dd858>\nToken: '
b'Flag: Aero{0f9e7ddd2be70f58b86f8f6589e17f182fc21c71437c2d9923fefa7ae281712b}\n'
```

