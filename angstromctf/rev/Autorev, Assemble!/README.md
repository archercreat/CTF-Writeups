# Autorev, Assemble! (225 solves)

>Clam was trying to make a neural network to automatically do reverse engineering for him, but he made a typo and the neural net ended up making a reverse engineering challenge instead of solving one! Can you get the flag?
>
>Find it on the shell server at /problems/2020/autorev_assemble/ or over tcp at nc shell.actf.co 20203.
>
>Author: aplet123



The main function looks obfuscated...

```c++
int __cdecl main(int argc, const char **argv, const char **envp)
{
  puts("PROBLEM CREATION MODE: ON");
  puts("VISUAL BASIC GUI: ON");
  puts("HACKERMAN: ON");
  puts("HOTEL: TRIVAGO");
  puts("INPUT: ?");
  fgets(z, 256, stdin);
  if ( f992(z)
    && f268(z)
    && f723(z)
    && f611(z)
    && f985(z)
    && f45(z)
    && f189(z)
 ...
 ... // bunch of calls...
 ...
	&& f915(z) )
  {
    puts("CHALLENGE: SOLVED");
  }
  else
  {
    puts("YOUR SKILL: INSUFFICIENT");
  }
  return 0;
}
```



Solution:

We use angr to automatically solve challenge for us :)

```python
import angr
import claripy
import sys


def main():
    proj = angr.Project('autorev_assemble')

    state = proj.factory.entry_state()

    simgr = proj.factory.simgr(state)

    simgr.explore(
        find=0x408953,
        avoid=0x408961
    )

    print(simgr)

    if simgr.found:
        f = simgr.found[-1]
        print(f.posix.dumps(0))

if __name__ == "__main__":
    sys.exit(main())
```

```bash
$ python3 solve.py
b'Blockchain big data solutions now with added machine learning. Enjoy! I sincerely hope you actf{wr0t3_4_pr0gr4m_t0_h3lp_y0u_w1th_th1s_df93171eb49e21a3a436e186bc68a5b2d8ed} instead of doing it by hand.'
```

