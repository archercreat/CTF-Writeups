section .text
global main
extern printf
; 
; nasm -f elf32 solve.asm && gcc -m 32 solve.o -o solve && ./solve
main:
    xor     eax, eax        ; init 
    lea     ebx, [flag]
    mov     ecx, 0x3B9ACA07
loop_0:
    mov     edx, [ebx]      ; test if we at last dword
    test    edx, edx        ; if so, we exit
    je      print
    push    eax             ; save eax
    mul     ecx
    cmp     eax, [ebx]      ; check if eax * ecx == flag[i]
    je      success         ; if so we overwrite flag[i] with eax
    pop     eax
    inc     eax
    jmp     loop_0
success:
    pop     dword [ebx]     ; overwrite dword flag[i]
    lea     ebx,  [ebx + 4] ; inc ebx
    jmp     loop_0
print:
    push    flag
    push    format
    call    printf
    add     esp, 8
    ret

section .data

flag:
    dd 0xd21e24d5
    dd 0x4ce97153
    dd 0x0236ce65
    dd 0x0530a488
    dd 0x51d85473
    dd 0x74a3045e
    dd 0x57384d73
    dd 0x9e37a488
    dd 0x2ee6fb57
    dd 0xb1d96e8f
    dd 0x8aa84b8f
    dd 0x047b598f
    dd 0xc930e881
    dd 0x9d0d916c
    dd 0

format:
    db "%s\n", 0
