### Reverthable X-Math

![3_title](images/3_title.png)



This time we are given with LISP program and output.txt.

Lisp source:

``` lisp
(defun frobnicate(str xor offset lvl)
  (setq mead (cheekybreeky (+ xor offset)))

  (cond ((< xor (- offset 1))
        (princ (logxor (- (char-int (char str mead)) (char-int #\0)) 42))
        (princ "/")
        (if (equal lvl 3)
          (setq mead (cheekybreeky 16))
        )

        (frobnicate str xor mead (+ lvl 1))
        (frobnicate str (+ mead 1) offset (+ lvl 1))
    )
    (
      t 0
    )
  )
)

(defun cheekybreeky (num)
  (setq n 0)
  (loop
    (if (>= (* n 2) num)
       (return)
    )
    (setq n (+ 1 n))
  )

  (if (equal (* n 2) num)
    (return-from cheekybreeky n)
    (return-from cheekybreeky (- n 1))
  )
)

(defun hello()
  (setq flag "your flag is in another castle!!")
  (frobnicate flag 0 (length flag) 0.0)
)

(hello)

```

output.txt :

``` sh
47/22/9/55/-41/59/39/97/-38/-38/108/42/41/-47/-46/-38/-38/22/46/110/22/46/23/20/45/46/47/20/-45/46/103/0
```

Obviously, the output is a flag, you just need to understand the lisp code.

Solution:

​	Every element splitted by slash in output.txt xored with 42 and added with 48:

``` lisp
(princ (logxor (- (char-int (char str mead)) (char-int #\0)) 42))
```

Let's print **mead** every time the condition gets executed so we can see in which positions on which the elements should be.

``` lisp
(format t "~d " mead)
```

``` sh
Reverthable X-Math> clisp task.lsp
16 8 4 2 1 3 6 5 7 12 10 9 11 14 13 15 24 20 18 17 19 22 21 23 28 26 25 27 30 29 31
```

Algorithm:

``` python
key =
'47/22/9/55/-41/59/39/97/-38/-38/108/42/41/-47/-46/-38/-38/22/46/110/22/46/23/20/45/46/47/20/-45/46/103/0'
pos = [16, 8, 4, 2, 1, 3, 6, 5, 7, 12, 10, 9, 11, 14, 13, 15, 24, 20,
       18, 17, 19, 22, 21, 23, 28, 26, 25, 27, 30, 29, 31] 
decode = lambda y: "".join([chr((int(i) ^ 42) + 48) for i in y])

flag = [0 for i in range(len(pos) + 1)]
temp = decode(key.split('/'))
for i in range(len(pos)):
    flag[pos[i]] = temp[i]

print(''.join(str(i) for i in flag))
```

``` 
>>> 0-MAS{= l0v3 (+ 5t4llm4n 54n74)}
```

Everything is right but the first character should be 'X'
