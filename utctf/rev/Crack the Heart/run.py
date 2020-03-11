## $ python3 run.py crackme2
## [+] Loading 0x400000 - 0x4000e8
## [+] Loading 0x401000 - 0x401013
## [+] Loading 0x402000 - 0x4149ad
## [+] Starting emulation.
## [+] ptrace hooked
## [+] Write hooked
## Why should I go out with you?
## [+] Read hooked
## [+] asking for 83 bytes
## [+] Write hooked
## uWu very cool!
## [+] exit hooked
## utflag{what_1f....i_mapp3d_mY_m3m0ry_n3xt_to_y0urs....ahahaha, jkjk....unless ;)?}

import string
import struct
import sys
import lief

from triton    import *

DEBUG = True

# Memory mapping
BASE_STACK = 0x9fffffff

def debug(s):
    if DEBUG: print(s)


def WriteHandler(ctx):
    debug('[+] Write hooked')

    # Get arguments
    buf  = ctx.getConcreteRegisterValue(ctx.registers.rsi)
    size = ctx.getConcreteRegisterValue(ctx.registers.rdx)

    s = str()
    for index in range(size):
        c = chr(ctx.getConcreteMemoryValue(buf+index))
        if c not in string.printable: c = ""
        s += c
    
    sys.stdout.write(s)
    return size


def ReadHandler(ctx):
    debug('[+] Read hooked')

    buf  = ctx.getConcreteRegisterValue(ctx.registers.rsi)
    size = ctx.getConcreteRegisterValue(ctx.registers.rdx)

    debug(f'[+] asking for {size} bytes')

    # fill dummy input
    inp = "a" * (size - 1) + '\x00'
    ctx.setConcreteMemoryAreaValue(buf, inp.encode())   

    # symbolize size bytes
    for i in range(size):
        # ctx.taintMemory(MemoryAccess(buf + i, CPUSIZE.BYTE))
        var = ctx.symbolizeMemory(MemoryAccess(buf + i, CPUSIZE.BYTE))
    return size

def ptraceHandler(ctx):
    debug('[+] ptrace hooked')
    return 0

def exitHandler(ctx):
    debug('[+] exit hooked')
    
    ast = ctx.getAstContext()
    pco = ctx.getPathPredicate()
    # Ask for a new model which set all symbolic variables to ascii printable characters
    mod = ctx.getModel(ast.land(
            [pco] +
            [ast.variable(ctx.getSymbolicVariable(x))  <= 0x7e for x in range(0, 33)]
          ))

    flag = str()
    for k, v in sorted(mod.items()):
        flag += chr(v.getValue())
    print(flag)
    sys.exit(0)

custom_relocs = [
    (0x40218B, ReadHandler),
    (0x402166, WriteHandler),
    (0x4021EA, ptraceHandler),
    (0x4021C4, exitHandler)
]

def hookingHandler(ctx):
    pc = ctx.getConcreteRegisterValue(ctx.registers.rip)

    for rel in custom_relocs:
        if rel[0] == pc:
            ret_val = rel[1](ctx)
            if ret_val is not None:
                ctx.concretizeRegister(ctx.registers.rax)
                ctx.setConcreteRegisterValue(ctx.registers.rax, ret_val)


# Emulate the binary.
def emulate(ctx, pc):
    count = 0
    while pc:
        opcodes = ctx.getConcreteMemoryAreaValue(pc, 16)

        instruction = Instruction()
        instruction.setOpcode(opcodes)
        instruction.setAddress(pc)

        count += 1

        if ctx.processing(instruction) == False:
            debug('[-] Instruction not supported: %s' %(str(instruction)))
            break

        if instruction.getType() == OPCODE.X86.HLT:
            break
        
        # check condition
        # sub, al, bl
        if instruction.getAddress() == 0x40213B:
            zf  = ctx.getSymbolicRegister(ctx.registers.zf).getAst()
            pco = ctx.getPathPredicate()
            ast = ctx.getAstContext()
            # find model that fits the equation
            mod = ctx.getModel(ast.land([pco, zf == 1]))
            # set every variable to its desired value
            for k, v in list(mod.items()):
                ctx.setConcreteVariableValue(ctx.getSymbolicVariable(k), v.getValue())

        hookingHandler(ctx)
        
        pc = ctx.getConcreteRegisterValue(ctx.registers.rip)

    debug('[+] Instruction executed: %d' %(count)) 
    return

def run(ctx, binary):
    # Concretize previous context
    ctx.concretizeAllMemory()
    ctx.concretizeAllRegister()

    # Define a fake stack
    ctx.setConcreteRegisterValue(ctx.registers.rbp, BASE_STACK)
    ctx.setConcreteRegisterValue(ctx.registers.rsp, BASE_STACK)

    # Let's emulate the binary from the entry point
    debug('[+] Starting emulation.')
    emulate(ctx, binary.entrypoint)
    debug('[+] Emulation done.')
    return

def loadBinary(ctx, binary):
    # Map the binary into the memory
    phdrs = binary.segments
    for phdr in phdrs:
        size   = phdr.physical_size
        vaddr  = phdr.virtual_address
        debug('[+] Loading 0x%06x - 0x%06x' %(vaddr, vaddr+size))
        ctx.setConcreteMemoryAreaValue(vaddr, phdr.content)
    return


def main():
    if len(sys.argv) != 2:
        print('[-] Usage: python3 run.py <filename>')
        sys.exit(-1)

    ctx = TritonContext()
    ctx.setArchitecture(ARCH.X86_64)

    ctx.setMode(MODE.ALIGNED_MEMORY, True)
    ctx.setMode(MODE.ONLY_ON_SYMBOLIZED, True)

    ctx.setAstRepresentationMode(AST_REPRESENTATION.PYTHON)

    binary = lief.parse(sys.argv[1])
    loadBinary(ctx, binary)

    run(ctx, binary)
    return 0

if __name__ == "__main__":
    sys.exit(main())
