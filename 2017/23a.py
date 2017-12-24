#!/usr/bin/env python3

import sys
from collections import defaultdict

def read(regs, s):
    return regs[s] if s.isalpha() else int(s)

def step(data, regs, ip):
    op, Rs, Rd = data[ip]
    Vs, Vd = read(regs, Rs), read(regs, Rd)

    if op == "snd":
        outq.append(Vs)
    elif op == "set":
        regs[Rs] = Vd
    elif op == "sub":
        regs[Rs] -= Vd
    elif op == "mul":
        regs[Rs] *= Vd
    elif op == "mod":
        regs[Rs] %= Vd
    elif op == "rcv":
        if not inq: return None
        regs[Rs] = inq.pop(0)
    elif op == "jnz":
        if Vs != 0:
            return ip + Vd
    return ip + 1

def main(args):
    data = [tuple(s.strip().split(" ")+['-1'])[:3] for s in sys.stdin]

    regsa, ina, ipa = defaultdict(int, {'p': 0}), [], 0
#    regsb, inb, ipb = defaultdict(int, {'p': 1}), [], 0
    snds = 0

    while True:
        if data[ipa][0] == "mul": snds+=1
        ipa = nextip = step(data, regsa, ipa)
        if ipa < 0 or ipa >= len(data): break
        print(ipa)

    print(regsa)
    print(snds)



if __name__ == '__main__':
    sys.exit(main(sys.argv))
