
raw = open('Re4.bin', 'rb').read()
import binascii
from unicorn import *
from unicorn.x86_const import *

def hook_code(uc, address, size, user_data):
    if address == 0x01AA:
        print('end of decoding stage')
        shellcode = uc.mem_read(2, 0x63) # shellcode
        open('shellcode', 'wb').write(shellcode)
    
    if address == 0xf:
        eax = uc.reg_read(UC_X86_REG_EAX)
        print(hex(eax))
    
    if address == 0x27:
        uc.emu_stop()


uc = Uc(UC_ARCH_X86, UC_MODE_32)

base = 0
uc.mem_map(base, 0x1000)
uc.mem_write(base, raw)
uc.hook_add(UC_HOOK_CODE, hook_code)

try:
    uc.emu_start(base, base + len(raw))
except UcError as e:
    print(e)
    print(f'adr = {hex(uc.reg_read(UC_X86_REG_EIP))}')