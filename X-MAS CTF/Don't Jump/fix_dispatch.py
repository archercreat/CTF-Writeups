import re
import idaapi
import idc
import yara

rules = """
rule jumps
{
    strings:
        $s1 = {E9 00 00 00 00}

    condition:
        any of them
}
"""

align = lambda size, alignment: ((size // alignment) + 1) * alignment

def patch(dest, seq):
    for i, c in enumerate(seq):
        idc.PatchByte(dest+i, ord(c))


def patch_inderect_jumps():
    print "patching  jumps.."
    count = 0
    match = list()
    for hit in matches:
        if hit.rule == 'jumps':
            match = hit.strings
    for hit in match:
        (offset, name, pattern) = hit
        print offset, name, pattern
        pattern_size = len(pattern)
        patch(start + offset, "\x90"*5)
        print(hex(start + offset))
        count += 1
    print "patched %d jumps!" % count

if __name__ == "__main__":
    start = idc.get_segm_by_sel(10)
    print hex(start)
    end = idc.get_segm_end(start)
    print hex(end)
    data = idaapi.get_many_bytes(start, end - start)
    matches = yara.compile(source=rules).match(data=data)
    #path_jumps_with_constant_condition()
    patch_inderect_jumps()
