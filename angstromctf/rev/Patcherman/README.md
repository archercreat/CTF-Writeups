# Patcherman (207 solves)

> Oh no! We were gonna make this an easy  challenge where you just had to run the binary and it gave you the flag, but then clam came along under the name of "The Patcherman" and edited  the binary! I think he also touched some bytes in the header to throw  off disassemblers. 
>
> Can you still retrieve the flag?
>
> Alternatively, find it on the shell server at `/problems/2020/patcherman/`.
>
> Author: aplet123

Solution:

patching 0x601050 to 0x1337beef and patching instruction at 0x400763 to **cmp eax, 0** yields the flag:

```
Here have a flag:
actf{p4tch3rm4n_15_n0_m0r3}
```

