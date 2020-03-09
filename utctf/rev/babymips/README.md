# babymips (122 solves)	

Description:

> what's the flag? 
>
> by Dan



Looking at the main function we can see the binary asks for flag, then calls check function.

```c++
undefined4 main(void)

{
  basic_ostream *this;
  basic_string<char,std--char_traits<char>,std--allocator<char>> abStack152 [24];
  basic_string<char,std--char_traits<char>,std--allocator<char>> input [24];
  undefined encoded_flag [84];
  int iStack20;
  
  iStack20 = __stack_chk_guard;
  basic_string();
  this = operator<<<std--char_traits<char>>((basic_ostream *)&cout,"enter the flag");
  operator<<((basic_ostream<char,std--char_traits<char>> *)this,endl<char,std--char_traits<char>>);
  operator>><char,std--char_traits<char>,std--allocator<char>>
            ((basic_istream *)&cin,(basic_string *)abStack152);
  memcpy(encoded_flag,&UNK_004015f4,0x54);
  basic_string((basic_string *)input);
  check_flag(encoded_flag,input);
  ~basic_string(input);
  ~basic_string(abStack152);
  return 0;
}
```

The **check_function** takes 2 arguments. First one being actual encoded flag, the second being our input string.

```c++
void check_flag(int encoded_flag,
               basic_string<char,std--char_traits<char>,std--allocator<char>> *input)

{
  int iVar1;
  basic_ostream *this;
  uint uVar2;
  char *c;
  uint i;
  
  iVar1 = size();
  if (iVar1 == 0x4e) {
    i = 0;
    while (uVar2 = size(), i < uVar2) {
      c = (char *)operator[](input,i);
      if (((int)*c ^ i + 0x17) != (int)*(char *)(encoded_flag + i)) {
        this = operator<<<std--char_traits<char>>((basic_ostream *)&cout,"incorrect");
        operator<<((basic_ostream<char,std--char_traits<char>> *)this,
                   endl<char,std--char_traits<char>>);
        return;
      }
      i = i + 1;
    }
    this = operator<<<std--char_traits<char>>((basic_ostream *)&cout,"correct!");
    operator<<((basic_ostream<char,std--char_traits<char>> *)this,endl<char,std--char_traits<char>>)
    ;
  }
  else {
    this = operator<<<std--char_traits<char>>((basic_ostream *)&cout,"incorrect");
    operator<<((basic_ostream<char,std--char_traits<char>> *)this,endl<char,std--char_traits<char>>)
    ;
  }
  return;
}
```



The algorithm is straightforward. We take one byte from out input, xor it with **i** and add 0x17

Solution:

```python
import binascii
from z3 import *
flag = '62 6C 7F 76 7A 7B 66 73 76 50 52 7D 40 54 55 79 40 49 47 4D 74 19 7B 6A 42 0A 4F 52 7D 69 4F 53 0C 64 10 0F  1E 4A 67 03 7C 67 02 6A 31 67 61 37 7A 62 2C 2C 0F 6E 17 00 16 0F 16 0A 6D 62 73 25 39 76 2E 1C 63 78 2B 74 32 16 20 22 44 19'.replace(' ','')
flag = binascii.unhexlify(flag)



def encode(inp, i):
    return (inp ^ i + 0x17) & 0xff

def find_all_posible_solutions(s):
    while s.check() == sat:
        model = s.model()
        block = []
        out = ''
        for i in range(flag_len):
            c = globals()['b%i' % i]
            out += chr(model[c].as_long())
            block.append(c != model[c])
        s.add(Or(block))
        print(out) 
      
def main():
    s = Solver()
    flag_len = len(flag)
    for i in range(flag_len):
        globals()['b%d' % i] = BitVec('b%d' % i, 8)
        s.add(globals()['b%d' % i] >= 32)
        s.add(globals()['b%d' % i] <= 126)
        s.add(encode(globals()['b%d' % i], i) == flag[i])
       
    find_all_posible_solutions(s)
   
if __name__ == "__main__":
    main()
```

The script yields one solution:

```
utflag{mips_cpp_gang_5VDm:~`N]ze;\)5%vZ=C'C(r#$q=*efD"ZNY_GX>6&sn.wF8$v*mvA@'}
```

