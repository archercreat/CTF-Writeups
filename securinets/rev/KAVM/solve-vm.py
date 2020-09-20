import ctypes
import os
import random
import string
import struct
import sys
import time
import lief
from triton import *

# Used for nested vm
sys.setrecursionlimit(100000)

# Script options
DEBUG   = True

# The debug function
def debug(s):
    if DEBUG: print(s)

# Used for return types
SYMBOLIC = 0
CONCRETE = 1

#symbolic variables
# sym_vars = list()
sym_input = list()

# Memory mapping
BASE_PLT   = 0x10000000
BASE_STACK = 0x9fffffff

# Time of execution
startTime = None
endTime   = None

def getMemoryString(ctx, addr):
    s = str()
    index = 0

    while ctx.getConcreteMemoryValue(addr+index):
        c = chr(ctx.getConcreteMemoryValue(addr+index))
        if c not in string.printable: c = ""
        s += c
        index  += 1

    return s


def getFormatString(ctx, addr):
    return getMemoryString(ctx, addr)                                               \
           .replace("%s", "{}").replace("%d", "{:d}").replace("%#02x", "{:#02x}")   \
           .replace("%#x", "{:#x}").replace("%x", "{:x}").replace("%02X", "{:02x}") \
           .replace("%c", "{:c}").replace("%02x", "{:02x}").replace("%ld", "{:d}")  \
           .replace("%*s", "").replace("%lX", "{:x}").replace("%08x", "{:08x}")     \
           .replace("%u", "{:d}").replace("%lu", "{:d}")                            \


# Simulate the strlen() function
def strlenHandler(ctx):
    debug('[+] strlen hooked')

    # Get arguments
    str_loc = ctx.getConcreteMemoryValue(MemoryAccess(ctx.getConcreteRegisterValue(ctx.registers.esp) + 4, CPUSIZE.DWORD))
    arg1 = getMemoryString(ctx, str_loc)

    # Return value
    if ctx.isMemorySymbolized(str_loc):
        print('[+] symbolizing strlen')
        return (len(arg1), CONCRETE)
    else:
        return (len(arg1), CONCRETE)


# Simulate the printf() function
def printfHandler(ctx):
    debug('[+] printf hooked')
    str_loc = ctx.getConcreteMemoryValue(MemoryAccess(ctx.getConcreteRegisterValue(ctx.registers.esp) + 8, CPUSIZE.DWORD))
    arg1 = getMemoryString(ctx, str_loc)
    sys.stdout.write(arg1)
    return (0, CONCRETE)

def libcMainHandler(ctx):
    debug('[+] __libc_start_main hooked')

    ctx.concretizeRegister(ctx.registers.esp)
    stack_main_loc = MemoryAccess(ctx.getConcreteRegisterValue(ctx.registers.esp) + CPUSIZE.DWORD, CPUSIZE.DWORD)
    main = ctx.getConcreteMemoryValue(stack_main_loc)

    # Push the return value to jump into the main() function
    ctx.setConcreteRegisterValue(ctx.registers.esp, ctx.getConcreteRegisterValue(ctx.registers.esp)-CPUSIZE.DWORD)

    ret2main = MemoryAccess(ctx.getConcreteRegisterValue(ctx.registers.esp), CPUSIZE.DWORD)
    ctx.concretizeMemory(ret2main)
    ctx.setConcreteMemoryValue(ret2main, main)
    return (0, CONCRETE)

def scanfHandler(ctx):
    global sym_input
    debug('[+] scanf hooked')
    message = "a" * 32
    # Get buffer loc
    arg2 = ctx.getConcreteMemoryValue(MemoryAccess(ctx.getConcreteRegisterValue(ctx.registers.esp) + 8, CPUSIZE.DWORD))

    # Fill scanf buffer with dummy inputs
    ctx.setConcreteMemoryAreaValue(arg2, message.encode() + b'\x00')

    # Symbolize
    debug('[+] symbolizing scanf buffer')
    for index in range(len(message)):
        ctx.taintMemory(MemoryAccess(arg2 + index, CPUSIZE.BYTE))
        var = ctx.symbolizeMemory(MemoryAccess(arg2 + index, CPUSIZE.BYTE))
        var.setComment("input_%d" % index)
        sym_input.append(var)

    # Return value
    return (len(message), CONCRETE)

customRelocation = [
    ('__libc_start_main', libcMainHandler, BASE_PLT + 0),
    ('printf',            printfHandler,   BASE_PLT + 1),
    ('strlen',            strlenHandler,   BASE_PLT + 2),
    ('__isoc99_scanf',    scanfHandler,    BASE_PLT + 3),
]


def hookingHandler(ctx):
    # global sym_vars
    pc = ctx.getConcreteRegisterValue(ctx.registers.eip)

    for rel in customRelocation:
        if rel[2] == pc:
            # Emulate the routine and the return value
            ret_value, ret_type = rel[1](ctx)
            if ret_value is not None:             
                ret_value &= 0xffffffff
                ctx.concretizeRegister(ctx.registers.eax)
                ctx.setConcreteRegisterValue(ctx.registers.eax, ret_value)
                
                if ret_type == SYMBOLIC:
                    var = ctx.symbolizeRegister(ctx.registers.eax)
                    # var.setComment("strlen")
                    # sym_vars.append(var)

            # Get the return address
            ret_addr = ctx.getConcreteMemoryValue(MemoryAccess(ctx.getConcreteRegisterValue(ctx.registers.esp), CPUSIZE.DWORD))

            # Hijack EIP to skip the call
            ctx.concretizeRegister(ctx.registers.eip)
            ctx.setConcreteRegisterValue(ctx.registers.eip, ret_addr)

            # Restore ESP (simulate the ret)
            ctx.concretizeRegister(ctx.registers.esp)
            ctx.setConcreteRegisterValue(ctx.registers.esp, ctx.getConcreteRegisterValue(ctx.registers.esp)+CPUSIZE.DWORD)
    return


def getNewInputs(ctx):
    inputs = list()
    ast = ctx.getAstContext()
    pco = ctx.getPathConstraints()
    # start with any input 
    previousConstraints = ast.equal(ast.bvtrue(), ast.bvtrue())

    # Go through the path constraints
    for pc in pco:
        # If there is a condition
        if pc.isMultipleBranches():
            # Get all branches
            branches = pc.getBranchConstraints()

            for branch in branches:
                # Get constraints of the branch which has been not taken
                if not branch['isTaken']:
                    # Ask for model
                    models = ctx.getModel(ast.land(
                        [previousConstraints] +
                        [branch['constraint']] + 
                        [ast.variable(i) > 32 for i in sym_input] +
                        [ast.variable(i) < 127 for i in sym_input]))
                    seed = dict()

                    for k, v in sorted(models.items()):
                        # Get symbolic variable assigned to model
                        symVar = ctx.getSymbolicVariable(k)
                        # Save new input
                        seed.update({symVar: v.getValue()})
                    if seed:
                        inputs.append(seed)
        # Update the previous constraints with true branch to keep a good path
        previousConstraints = ast.land([previousConstraints, pc.getTakenPredicate()])
    return inputs

# Emulate the binary.
def emulate(ctx, pc):
    count = 0
    while pc:
        # Fetch opcodes
        opcodes = ctx.getConcreteMemoryAreaValue(pc, 16)
        # Create the Triton instruction
        instruction = Instruction()
        instruction.setOpcode(opcodes)
        instruction.setAddress(pc)

        # Process
        if ctx.processing(instruction) == False:
            debug('[-] Instruction not supported: %s' %(str(instruction)))
            break
        count += 1

        if instruction.isSymbolized():
            print(instruction)

        hookingHandler(ctx)

        pc = ctx.getConcreteRegisterValue(ctx.registers.eip)


    debug('[+] Instruction executed: %d' %(count))
    
    debug('[+] Getting new input..')

    for input in getNewInputs(ctx):
        out = ''
        for k, v in input.items():
            out += chr(v)
        print(out)
    return


def loadBinary(ctx, binary):
    phdrs = binary.segments
    for phdr in phdrs:
        size   = phdr.physical_size
        vaddr  = phdr.virtual_address
        debug('[+] Loading 0x%08x - 0x%08x' %(vaddr, vaddr+size))
        ctx.setConcreteMemoryAreaValue(vaddr, phdr.content)
    return


def makeRelocation(ctx, binary):
    try:
        for rel in binary.pltgot_relocations:
            symbolName = rel.symbol.name
            symbolRelo = rel.address
            for crel in customRelocation:
                if symbolName == crel[0]:
                    debug('[+] Hooking %s' %(symbolName))
                    ctx.setConcreteMemoryValue(MemoryAccess(symbolRelo, CPUSIZE.DWORD), crel[2])
    except:
        pass
    try:
        for rel in binary.dynamic_relocations:
            symbolName = rel.symbol.name
            symbolRelo = rel.address
            for crel in customRelocation:
                if symbolName == crel[0]:
                    debug('[+] Hooking %s' %(symbolName))
                    ctx.setConcreteMemoryValue(MemoryAccess(symbolRelo, CPUSIZE.DWORD), crel[2])
    except:
        pass
    return


def run(ctx, binary):
    # Concretize previous context
    ctx.concretizeAllMemory()
    ctx.concretizeAllRegister()

    # Define a fake stack
    ctx.setConcreteRegisterValue(ctx.registers.ebp, BASE_STACK)
    ctx.setConcreteRegisterValue(ctx.registers.esp, BASE_STACK)

    # Let's emulate the binary from the entry point
    debug('[+] Starting emulation.')
    emulate(ctx, binary.entrypoint)
    debug('[+] Emulation done.')
    return

def main():
    ctx = TritonContext()
    ctx.setArchitecture(ARCH.X86)

    ctx.setMode(MODE.ALIGNED_MEMORY, True)
    ctx.setMode(MODE.ONLY_ON_SYMBOLIZED, True)

    ctx.setAstRepresentationMode(AST_REPRESENTATION.PYTHON)

    if len(sys.argv) != 2:
        debug('[-] Syntax: %s <target vm>' %(sys.argv[0]))
        return -1

    binary = lief.parse(sys.argv[1])
    loadBinary(ctx, binary)
    makeRelocation(ctx, binary)

    run(ctx, binary)
    return 0


if __name__ == '__main__':
    startTime = time.clock()
    retValue  = main()
    endTime   = time.clock()
    sys.exit(retValue)
