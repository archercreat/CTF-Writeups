_start:
xor edx, edx
lea esi, [flag]
lea edi, [flag]
cld
_loop:
lodsb
test al, al
je _stop
mov bx, 223
mul bl
xor al, 0xA5
add dl, al
mov eax, edx
stosb
jmp _loop

_stop:
jmp _stop

flag: db 0 ; DATA EXPUNGED