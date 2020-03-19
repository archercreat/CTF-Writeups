# A Happy Family (74 solves)

> Clam became a parent and had a child. Or at least he dreamed about it. Anyway, clam wrote a program to describe his dream. In fact, he's so happy that he provided source!
>
> Find it on the shell server at `/problems/2020/a_happy_family`.
>
> The sha256 hash (no newline) of the correct input is `aa15a7b191ffa943fa602f7472ef294c6b5d138a629ac2bb75cb6ac57bfc3257`.
>
> Author: aplet123





Solution:

First, find all possible n1, n2, n3, n4 (check **find_all_possible** function)

Next, apply reverse math on them and convert back to string. 

Copy those strings that have all printable characters in them.

In the end, we have 1 in n1, n2, n3 and 4 in n4

```python
from itertools import zip_longest, product
import sys
from struct import *
import string


alphabet = "angstromctf20"
alphabet_st = "0123456789ABC"

flags = {
    'c1' : 'artomtf2srn00tgm2f',
    'c2' : 'ng0fa0mat0tmmmra0c',
    'c3' : 'ngnrmcornttnsmgcgr',
    'c4' : 'a0fn2rfa00tcgctaot'
}
 
 
def find_all_possible(inp):
    th_nums = [[alphabet_st[i] for i, y in enumerate(alphabet) if y == x] for x in inp]
    variants = [''.join(x) for x in product(*th_nums) ]
    nums = [int(x, 13) for x in variants]
    return nums

def main():
    n1 = pack('<Q', 0x315f6e7270746567).decode()
    n2 = pack('<Q', 0x6c685f3374623468).decode()
    n3 = pack('<Q', 0x74777433345f3472).decode()
    n4 = [
        pack('<Q', 0x6431637274335f44).decode(), 
        pack('<Q', 0x6431637274335f5f).decode(), 
        pack('<Q', 0x643163727433707b).decode(), 
        pack('<Q', 0x6431637274337076).decode()]

    key = [0 for i in range(32)]
    for j in range(4):
        for i in range(0, 8):
            key[i * 2] = n1[i]
            key[(i * 2) + 1] = n3[i]
            key[(i + 8) * 2] = n2[i]
            key[((i + 8) * 2) + 1] = n4[j][i]
        print(''.join(key))
        key = [0 for i in range(32)]

if __name__ == '__main__':
    sys.exit(main())
```

```bash
gre4t_p4r3nt_w1thD4_b3tt3r_ch1ld
gre4t_p4r3nt_w1th_4_b3tt3r_ch1ld		<- correct flag
gre4t_p4r3nt_w1th{4pb3tt3r_ch1ld
gre4t_p4r3nt_w1thv4pb3tt3r_ch1ld
```

