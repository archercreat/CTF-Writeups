# Chestburster (23 solves)

> I'm out of descriptions. This guys got layers!
>
>  Connect with `nc challenges.auctf.com 30006` Author: nadrojisk



The challenge consist of 2 parts. In first, we have to find right password, and in second we have to intercept flag transmission.



### Part 1:

```c++
int  main()
{
  FILE *v3;
  FILE *v4;
  int result;
  char v6;
  char v7;
  char Buffer;

  v3 = _acrt_iob_func(1u);
  setvbuf(v3, 0, 4, 0);
  printf("Welcome to The Vault!\n\n\tThis challenge is simple answer the questions right and you get the flag!\n", v7);
  printf("Be warned however, what you seek may not be here ... \n", v6);
  if ( check() )
  {
    printf("\tNice job!\n", Buffer);
    v4 = fopen("flag.txt", "r");
    if ( !v4 )
    {
      printf("Too bad you can only run this exploit on the server...\n", Buffer);
      exit(0);
    }
    fgets(&Buffer, 512, v4);
    printf("%s", (char)&Buffer);
    result = 0;
  }
  else
  {
    printf("\tThat is not correct\n", Buffer);
    result = 0;
  }
  return result;
}
```

The check function is pretty big... After it read our input it makes some encoding and compares it to `welcome_to_the_jungle!`

```c++
return strcmp(encoded_input, "welcome_to_the_jungle!");
```

So, we can observe what our input is being encoded into. 

I ran the binary with input  = `0123456789abcdefghijkl` and got `5b06c17dl28ekj39fihg4a`

So it looks that the algorithm just swaps the letters.

So, lets reverse that:

```python
import sys

def main():
    inp = '0123456789abcdefghijkl'
    out = '5b06c17dl28ekj39fihg4a'
    flag= 'welcome_to_the_jungle!'
    flag_flag = [0 for i in range(22)]
    for i, v in enumerate(inp):
        pos = out.find(v)
        flag_flag[i] = flag[pos]
    print(''.join(flag_flag))    

if __name__ == "__main__":
    sys.exit(main())
```

We get `lmo_ewce_j!eo_tulgneht`

Lets check it:

```bash
$ nc challenges.auctf.com 30006
Welcome to The Vault!

        This challenge is simple answer the questions right and you get the flag!
Be warned however, what you seek may not be here ...
        You know the drill, give me some input and I'll tell you if it's right

        lmo_ewce_j!eo_tulgneht
        Nice job!
Sorry Mario your flag isn't here... but you can have this! challenges.auctf.com:30009
^C
```

Instead of flag we get the link to an empty website..



### Part 2:

The executable file itself weights 6 mb. It\`s not normal. If we open it in hex editor and search for `This program` we find another executable appended to the end of the first one.

The second executable is written in `GO` and its very huge.

If we run it, it asks us for `URL:PORT` and if we give `challenges.auctf.com:30009` to it it prints

```
>chestburster.exe challenges.auctf.com:30009
Establishing Connection ...

Message from server: Ahh. I see you've found me... here comes the flag :)
Message from server:
```

So, it looks like it prints only part of the message.

We can use wireshark to intercept transmission and get full message.

```
>chestburster.exe challenges.auctf.com:30009
Establishing Connection ...

Message from server: Ahh. I see you've found me... here comes the flag :)
Message from server: auctf{r3s0urc3_h4cK1Ng_1S_n3at0_1021}
```

