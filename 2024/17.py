#!/usr/bin/env python3

import sys
import re

def extract(s):
    return [int(x) for x in re.findall(r'(-?\d+).?', s)]


def run(program, regs, a=None):
    regs = list(regs)
    if a is not None:
        regs[0] = a

    def combo(op):
        if op <= 3:
            return op
        else:
            return regs[op - 4]
    M = 7

    out = []
    ip = 0
    while ip < len(program):
        op = program[ip]
        val = program[ip+1]
        if op == 0:
            regs[0] = regs[0] >> combo(val)
        elif op == 1:
            regs[1] ^= val
        elif op == 2:
            regs[1] = combo(val) & 7
        elif op == 3:
            if regs[0] != 0:
                ip = val
                continue
        elif op == 4:
            regs[1] ^= regs[2]
        elif op == 5:
            out.append(combo(val) & M)
        elif op == 6:
            regs[1] = regs[0] >> combo(val)
        elif op == 7:
            regs[2] = regs[0] >> combo(val)
        ip += 2

    return out


def encode(num, i, program):
    """
    Original version was based onbased on the program:

    B = A & 7
    B = B ^ 1
    C = A >> B
    B = B ^ C
    B = B ^ 4
    A = A >> 3
    OUT(B & 7)
    jnz A 0
    """

    if i < 0:
        return num

    val = program[i]
    # print(i, val, num)
    for ib in range(8):
        nnum = (num << 3) | ib
        # I should have reused run to do this in the first place
        # instead of coding it myself and screwing it up repeatedly.
        # But still, **39 so.

        out = run(program[:-2], [nnum, 0, 0])[0]

        # Original solution did:
        # b = ib ^ 1
        # c = nnum >> b
        # b ^= c
        # b ^= 4
        # out = b & 7

        if out == val:
            ok = encode(nnum, i-1, program)
            if ok is not None:
                return ok

    return None



def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    data = [s.rstrip('\n') for s in file]

    regs = [extract(l)[0] for l in data[:3]]
    program = extract(data[-1])

    print(','.join(str(x) for x in run(program, regs)))

    val = encode(0, len(program)-1, program)
    assert run(program, regs, val) == program
    print(val)


if __name__ == '__main__':
    main(sys.argv)
