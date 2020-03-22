# Warmup : Welcome to securinets CTF (188 solves)

> Is this enough for you? 
>
> Authors : KERRO & Anis_Boss

main:

```c++
int main(int a1, char **a2, char **a3)
{
  size_t v3;
  int v5;
  int i;

  write(1, "Welcome to SECURINETS CTF\n", 0x1AuLL);
  read(0, s, 0x31uLL);
  s[strlen(s) - 1] = 0;
  v5 = 0;
  strcpy(dest, s);
  v3 = strlen(s);
  memfrob(s, v3);
  for ( i = 0; i <= 19; ++i )
    v5 += (char)(s[i] ^ byte_201020[i]);
  if ( v5 )
    puts(":(...");
  else
    printf("Good job\nYou can submit with securinets{%s}\n", dest);
  return 0LL;
}
```

Solution:

```python
flag = [
    0x46, 0x19, 0x5e, 0x0d,
    0x59, 0x75, 0x5d, 0x1e,
    0x58, 0x47, 0x75, 0x1b,
    0x5e, 0x75, 0x5f, 0x5a,
    0x75, 0x48, 0x45, 0x53, 
    0x1e
]

out = ''
for i in flag:
    out += chr(i ^ 42)
print(out)
```

yields `l3t's_w4rm_1t_up_boy4`