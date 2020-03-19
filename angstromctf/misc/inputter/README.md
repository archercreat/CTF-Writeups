# Inputter (320 solves)

> Clam **really** likes challenging himself. When he learned about all these weird unprintable ASCII characters he just HAD to put it in a challenge. 
>
> Can you satisfy his knack for strange and hard-to-input characters? Source.
>
> Find it on the shell server at `/problems/2020/inputter/`.
>
> Author: aplet123



```c++
#define _GNU_SOURCE

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <unistd.h>

#define FLAGSIZE 128

void print_flag() {
    gid_t gid = getegid();
    setresgid(gid, gid, gid);
    FILE *file = fopen("flag.txt", "r");
    char flag[FLAGSIZE];
    if (file == NULL) {
        printf("Cannot read flag file.\n");
        exit(1);
    }
    fgets(flag, FLAGSIZE, file);
    printf("%s", flag);
}

int main(int argc, char* argv[]) {
    setvbuf(stdout, NULL, _IONBF, 0);
    if (argc != 2) {
        puts("Your argument count isn't right.");
        return 1;
    }
    if (strcmp(argv[1], " \n'\"\x07")) {
        puts("Your argument isn't right.");
        return 1;
    }
    char buf[128];
    fgets(buf, 128, stdin);
    if (strcmp(buf, "\x00\x01\x02\x03\n")) {
        puts("Your input isn't right.");
        return 1;
    }
    puts("You seem to know what you're doing.");
    print_flag();
}
```

Solution:

```bash
 export EGG=`python -c 'print "\x20\x0a\x27\x22\x07"'`
 python -c "print '\x00\x01\x02\x03\n'" | ./inputter "$EGG"
 
 You seem to know what you're doing.
 actf{impr4ctic4l_pr0blems_c4ll_f0r_impr4ctic4l_s0lutions}
```

