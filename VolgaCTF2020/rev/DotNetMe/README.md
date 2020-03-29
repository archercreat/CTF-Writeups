# DotNetMe (34 solves)

> Don't get confused when solving it!

The binary is packed with confuser v 1.3. 

Solution:

Open in dnspy, place bp on first dll call, trace password checking routine.
First it checks `length == 29`

Then it checks if `len(key.split('-')[i]) == 4`

So the flag format should be `YYYY-YYYY-YYYY-YYYY-YYYY-YYYY`

After that it performs xor checksum of all characters in the string and compares the value with 41.

Then it gets encoded flag, creates new string with out input and encoded flag and checks xor checksum with 74.

The hard part was to get hardcoded flag, since the binary is packed, dnspy could not show local variables so we basically debugged blindly. 

The way I solved it is by dumping the whole process onto the disk and running `strings -n29 proc.dmp`

After we get the encoded flag we can write a keygen:

```python

from z3 import *
import string
key = '3cD1Z84acsdf1caEBbfgMeAF0bObA'
alp = string.ascii_lowercase + string.ascii_uppercase + string.digits
flag_len = 29


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
    k = 0
    for i in range(flag_len):
        globals()['b%d' % i] = BitVec('b%d' % i, 32)
        c = globals()['b%d' % i]
        
        if (i + 1) % 5 == 0:
            s.add(c == ord('-'))
        else:
            s.add(Or([c == ord(i) for i in alp]))
        k ^= c

    s.add(k == 41)
    k = 0
    for i in range(flag_len):
        c = globals()['b%d' % i]
        n = c * ord('*')
        v = ((n >> 6) + (n >> 5) & 127) ^ (n + ord(key[i]) & 127) ^ ord(key[flag_len - i - 1])
        k ^= v

    s.add(k == 74)
    find_all_posible_solutions(s)    



    
if __name__ == "__main__":
    sys.exit(main())

```



 ```
$ python3 go.py
vsxs-wvmX-7qD3-66qn-UNro-IXur
nQ8N-BAbl-hcHR-KncK-YfBB-I5OP
nq8N-BAbl-HcHR-KncK-YfBB-I5OP
T3q8-Ordh-OATM-CqqK-MXX9-g0tS
T3Y8-Ordh-OATM-CqqK-MXp9-g0tS
T3Y8-Ordh-OATM-CqqK-MX09-gptS
T3Y8-Ordh-OATM-Cqqk-MX09-gPtS
ABbL-LEkI-pFLG-8lcD-aJ6Z-NBNI
 ```

