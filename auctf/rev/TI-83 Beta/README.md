# TI-83 Beta (68 solves)

> Hey I'm building a new calculator! I hid a flag inside it, think you can find it? Author: nadrojisk



We are given a windows executable.  The flag is in `SEH` exception handler that was registered in main function:

```
.text:004124D0 ; int __cdecl main_0(int argc, const char **argv, const char **envp)
.text:004124D0 _main_0         proc near               ; CODE XREF: _main↑j
.text:004124D0
.text:004124D0 var_C0          = byte ptr -0C0h
.text:004124D0 argc            = dword ptr  8
.text:004124D0 argv            = dword ptr  0Ch
.text:004124D0 envp            = dword ptr  10h
.text:004124D0
.text:004124D0                 push    ebp
.text:004124D1                 mov     ebp, esp
.text:004124D3                 sub     esp, 0C0h
.text:004124D9                 push    ebx
.text:004124DA                 push    esi
.text:004124DB                 push    edi
.text:004124DC                 lea     edi, [ebp+var_C0]
.text:004124E2                 mov     ecx, 30h
.text:004124E7                 mov     eax, 0CCCCCCCCh
.text:004124EC                 rep stosd
.text:004124EE                 push    offset sub_4111A9	; <- exception handling func
.text:004124F3                 push    large dword ptr fs:0 ; char
.text:004124FA                 mov     large fs:0, esp
.text:00412501                 push    offset aWelcomeToMyPro ; "Welcome to my program!\n"
.text:00412506                 call    print
.text:0041250B                 add     esp, 4
```



The exception handler is a bit obfuscated so IDA could not create a function from it. The flag is being create on stack one byte at the time. 

```
.text:00412560 loc_412560:                             ; CODE XREF: sub_4111A9↑j
.text:00412560                 push    ebp
.text:00412561                 mov     ebp, esp
.text:00412563                 sub     esp, 0C0h
.text:00412569                 push    ebx
.text:0041256A                 push    esi
.text:0041256B                 push    edi
.text:0041256C                 lea     edi, [ebp-0C0h]
.text:00412572                 mov     ecx, 30h ; '0'
.text:00412577                 mov     eax, 0CCCCCCCCh
.text:0041257C                 rep stosd
.text:0041257E                 xor     eax, eax
.text:00412580                 jz      short loc_412584
.text:00412580 ; ---------------------------------------------------------------------------
.text:00412582                 db 0EAh ; ê
.text:00412583                 db  58h ; X
.text:00412584 ; ---------------------------------------------------------------------------
.text:00412584
.text:00412584 loc_412584:                             ; CODE XREF: .text:00412580↑j
.text:00412584                 mov     eax, 0
.text:00412589                 sub     esp, 20h
.text:0041258C                 mov     byte ptr [esp], 61h ; 'a'
.text:00412590                 mov     byte ptr [esp+1], 75h ; 'u'
.text:00412595                 mov     byte ptr [esp+2], 63h ; 'c'
.text:0041259A                 mov     byte ptr [esp+3], 74h ; 't'
.text:0041259F                 mov     byte ptr [esp+4], 66h ; 'f'
.text:004125A4                 mov     byte ptr [esp+5], 7Bh ; '{'
.text:004125A9                 mov     byte ptr [esp+6], 6Fh ; 'o'
.text:004125AE                 xor     eax, eax
.text:004125B0                 jz      short loc_4125B4
.text:004125B0 ; ---------------------------------------------------------------------------
.text:004125B2                 db 0EAh ; ê
.text:004125B3                 db  58h ; X
.text:004125B4 ; ---------------------------------------------------------------------------
.text:004125B4
.text:004125B4 loc_4125B4:                             ; CODE XREF: .text:004125B0↑j
.text:004125B4                 mov     byte ptr [esp+7], 6Fh ; 'o'
.text:004125B9                 mov     byte ptr [esp+8], 70h ; 'p'
.text:004125BE                 mov     byte ptr [esp+9], 73h ; 's'
.text:004125C3                 mov     byte ptr [esp+0Ah], 5Fh ; '_'
.text:004125C8                 mov     byte ptr [esp+0Bh], 64h ; 'd'
.text:004125CD                 mov     byte ptr [esp+0Ch], 69h ; 'i'
.text:004125D2                 mov     byte ptr [esp+0Dh], 64h ; 'd'
.text:004125D7                 mov     byte ptr [esp+0Eh], 5Fh ; '_'
.text:004125DC                 mov     byte ptr [esp+0Fh], 69h ; 'i'
.text:004125E1                 mov     byte ptr [esp+10h], 5Fh ; '_'
.text:004125E6                 mov     byte ptr [esp+11h], 64h ; 'd'
.text:004125EB                 mov     byte ptr [esp+12h], 6Fh ; 'o'
.text:004125F0                 mov     byte ptr [esp+13h], 5Fh ; '_'
.text:004125F5                 mov     byte ptr [esp+14h], 74h ; 't'
.text:004125FA                 mov     byte ptr [esp+15h], 68h ; 'h'
.text:004125FF                 mov     byte ptr [esp+16h], 74h ; 't'
.text:00412604                 mov     byte ptr [esp+17h], 7Dh ; '}'
.text:00412609                 mov     byte ptr [esp+18h], 0Ah
.text:0041260E                 mov     byte ptr [esp+19h], 0
.text:00412613                 push    esp
.text:00412614                 call    print
```

`auctf{oops_did_i_do_tht}`