# Cracker Barrel (315 solves)

> I found a USB drive under the checkers  board at cracker barrel. My friends told me not to plug it in but surely nothing bad is on it? I found this file, but I can't seem to unlock it's secrets. Can you help me out? Also.. once you think you've got it I think you should try to connect to `challenges.auctf.com` at port `30000` not sure what that means, but it written on the flash drive.. Author: nadrojisk





## Solution:

There 3 checks that we should pass in order to get the flag:

#### check 1:

```c++
strcmp(input, "starwars")
```

#### check 2:

```c++
bool check2(char* input)
{
  int i;
  int len;
  char *v4;
  len = strlen(input);
  v4 = (char *)malloc_0(8LL * (len + 1));
  for ( i = 0; i < len; ++i )
    v4[i] = flag1[len - 1 - i];
  return strcmp(v4, input) == 0;
}
```

input should be `'si siht egassem terces'[::-1] ='secret message this is'`

#### check 3:

```c++
int check3(char *a1)
{
  __int64 v1;
  unsigned __int64 v2;
  unsigned __int64 v3; 
  __int64 result; 
  int i; 
  int v6; 
  int j;
  int *v8; 
  int v9[10];

  v7[0] = 'z';
  v7[1] = '!';
  v7[2] = '!';
  v7[3] = 'b';
  v7[4] = '6';
  v7[5] = '~';
  v7[6] = 'w';
  v7[7] = 'n';
  v7[8] = '&';
  v7[9] = '`';
  v1 = strlen_0(a1);
  v6 = (int *)malloc_0(4 * v1);
  for ( i = 0; i < (unsigned __int64)strlen_0(a1); ++i )
    v6[i] = (a1[i] + 2) ^ 0x14;
  v4 = 0;
  for ( j = 0; j < (unsigned __int64)strlen_0(a1); ++j )
  {
    if ( v6[j] != v7[j] )
      v4 = 1;
  }
  return v4 == 0;
}
```

We do everything in reverse and get the last flag:

```python
f = ['z', '!', '!', 'b', '6', '~', 'w', 'n', '&', '`']
out = ''
for i in f:
    out += chr((ord(i) ^ 0x14) - 2)
print(out)
```

`l33t hax0r`

after that we get the flag:

```bash
Give me a key!
starwars
You have passed the first test! Now I need another key!
secret message this is
Nice work! You've passes the second test, we aren't done yet!
l33t hax0r
Congrats you finished! Here is your flag!
auctf{w3lc0m3_to_R3_1021}
```

