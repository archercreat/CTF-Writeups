# Revving up (798 solves)

> Clam wrote a program for his school's cybersecurity club's first rev lecture! 
>
> Can you get it to give you the flag? 
>
> You can find it at `/problems/2020/revving_up` on the shell server, which you can access via the "shell" link at the top of the site.
>
> Author: aplet123

```c++
int __cdecl main(int argc, const char argv, const char envp)
{
  int result;  eax
  char v4;  [rsp+18h] [rbp-98h]
  char s;  [rsp+20h] [rbp-90h]
  unsigned __int64 v6;  [rsp+A8h] [rbp-8h]

  v6 = __readfsqword(0x28u);
  puts("Congratulations on running the binary!");
  puts("Now there are a few more things to tend to.");
  puts("Please type give flag (without the quotes).");
  fgets(&s, 128, stdin);
  v4 = strchr(&s, 10);
  if ( v4 )
    v4 = 0;
  if ( !strcmp(&s, "give flag") )
  {
    puts("Good job!");
    if ( argc  1 )
    {
      if ( !strcmp(argv[1], "banana") )
      {
        puts("ell I think it's about time you got the flag!");
        print_flag();
        result = 0;
      }
      else
      {
        printf("You provided %s, not banana. Please try again\n", argv[1]);
        result = 1;
      }
    }
    else
    {
      puts("Now run the program with a command line argument of banana and you'll be done!");
      result = 1;
    }
  }
  else
  {
    printf("You entered %s, not give flag. Please try again\n", &s);
    result = 1;
  }
  return result;
}
```



Solution:

calling binary with "banana" and telling it "give flag" yields flag

```
actf{g3tting_4_h4ng_0f_l1nux_4nd_b4sh}
```

