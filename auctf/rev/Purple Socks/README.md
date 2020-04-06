# Purple Socks (54 solves)

> We found this file hidden in a comic book store. Do you think you can reverse engineer it? We think it's been encrypted but we aren't sure. Author: nadrojisk



We are given an encrypted file. Assuming it is a reverse challenge, it is probably an encrypted executable.

First few bytes:

```
31 0B 02 08 4F 4F 4F 00 00 00 00 00 00 00 00 00 4D 00 4D 00 4F 00 00 00 3E 5F 00 00 7A 00 00 00 62 73 00 00 00 00 00 00 7A 00 6E 00 45 00 66 00
```

```python
>>> elf = '\x7fELF'
>>> bin = '\x31\x0b\x02\x08'

>>> for i in range(len(elf)):
...   print(chr(ord(elf[i]) ^ ord(bin[i])))
...
N
N
N
N
>>>
```

It looks like non zero values are xored with letter `N`. Now we can decrypt it.

```python
f = open('out', 'wb')

with open('purple_socks', 'rb') as f:
    raw = f.read()
    
for i in range(len(raw)):
    if raw[i] != 0:
        f.write(raw[i] ^ ord('N'))
    else:
        f.write(chr(raw[i]))
f.close()
```

main:

```c++
int main(int argc, const char **argv, const char **envp)
{
  char v4[8192];
  char dest[8192];
  int *v6;

  v6 = &argc;
  lp_input = (const char *)&input;
  setvbuf(stdout, 0, 2, 0);
  puts("Please Login: ");
  printf("username: ");
  fgets((char *)lp_input, 0x2000, stdin);
  remove_newline((char *)lp_input);
  strcpy(dest, lp_input);
  strcpy(v4, lp_input);
  printf("password: ");
  fgets((char *)lp_input, 0x2000, stdin);
  remove_newline((char *)lp_input);
  sprintf(dest, "%s:%s", dest, lp_input);
  if ( !strcmp(dest, creds) )
  {
    printf("Welcome %s\n\n", v4);
    commandline();
  }
  puts("Error: Incorrect login credentials");
  return 0;
}
```

Looks like some kind of service.

The creds are `bucky:longing, rusted, seventeen, daybreak, furnace, nine, benign, homecoming, one, freight car`

Lets log in and check whats up:

```bash
$ nc challenges.auctf.com 30049
Please Login:
username: bucky
password: longing, rusted, seventeen, daybreak, furnace, nine, benign, homecoming, one, freight car
Welcome bucky

> [? for menu]: ls
ls
call: ls
enc
entry.sh
flag.txt
> [? for menu]: read flag.txt
This file is password protected ...
You will have to enter the password to gain access
```

So, in order to get the read the flag we need the password.

Lets find check password function:

```c++
int encrypt()
{
  size_t input_len;
  size_t v1;
  size_t v2;
  char input[8192];
  int v5; 
  _DWORD *out; 
  unsigned int j; 
  int v8; 
  int i; 

  puts("This file is password protected ... \nYou will have to enter the password to gain access");
  printf("Password: ");
  fgets(input, 0x2000, stdin);
  input_len = strlen(input);
  out = malloc(4 * input_len);
  for ( i = 0; ; ++i )
  {
    v1 = strlen(input);
    if ( v1 <= i )
      break;
    v5 = i % 5;
    out[i] = input[i] ^ seed[i % 5];
    seed[v5] = out[i];
  }
  v8 = 0;
  for ( j = 0; ; ++j )
  {
    v2 = strlen(input);
    if ( v2 <= j )
      break;
    if ( secret[j] != out[j] )
      v8 = 1;
  }
  return v8;
}
```



### Solution:

```python
secret = [
    0x0e, 0x05, 0x06, 0x1a, 
    0x39, 0x7d, 0x60, 0x75, 
    0x7b, 0x54, 0x18, 0x6a]

seed   = [0x61, 0x75, 0x63, 0x74, 0x66]


def solve():
    state = 'auctf'
    seed2 = [0 for i in range(5)]
    out = ''
    for i in range(len(secret)):        
        for j in range(32, 127):
            c = seed[i % len(seed)] 
            if j ^ c == secret[i]:
                out += chr(j)
                seed[i % len(seed)] = j ^ c
                break
    print(out)

if __name__ == "__main__":
    solve()
```

gives `open_sesame`:

```bash
Password: open_sesame
auctf{encrypti0n_1s_gr8t_12921}
> [? for menu]:
```

