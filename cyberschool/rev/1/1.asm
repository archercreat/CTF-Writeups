global main
extern printf

main:
mov dword [flag + 6], 1870225259
mov eax, 3738091242
ror eax, 1
mov dword [flag + 10], eax
mov eax, 2342557323
xor eax, 0xFFFFFFFF
bswap eax
mov dword [flag + 14], eax
push flag
call printf
add esp, 4
jmp _stop

_stop:
jmp _stop

section .data

flag:
db "CSMSU{"
resb 12
db '}'
db '\0'
