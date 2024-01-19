#!/usr/bin/env python3

"""
00:20 < sully> this could be a Z3 day.
00:29 < sully> "A sword day, a red day."
"""

# I can't remember if this ever worked in 2021. I think maybe not, and
# I used the "honest" versions? When I was playing around with it in
# 2024 it run for 90 minutes without finishing, and then I tried using
# BitVec instead and it became fast.

import sys
import z3


NB = 32
def bv(n):
    return z3.BitVecVal(n, NB)


def eval(cmds, regs, inp):
    def r2(x):
        if x.isalpha():
            return regs[x]
        else:
            return bv(int(x))

    for cmd in cmds:
        x, *rest = cmd.split(" ")
        if x == 'inp':
            regs[rest[0]] = inp
            continue
        a, b = rest

        if x == 'add':
            regs[a] = regs[a] + r2(b)
        elif x == 'mul':
            regs[a] = regs[a] * r2(b)
        elif x == 'div':
            regs[a] = regs[a] / r2(b)
        elif x == 'mod':
            regs[a] = regs[a] % r2(b)
        elif x == 'eql':
            regs[a] = z3.If(regs[a] == r2(b), bv(1), bv(0))


def solve(cmds, func):
    parts = []
    cur = []
    for cmd in cmds:
        if cur and cmd.startswith('inp'):
            parts.append(cur)
            cur = []
        cur.append(cmd)
    parts.append(cur)

    digits = []
    regs = {k: bv(0) for k in 'wxyz'}
    opt = z3.Optimize()
    for i, part in enumerate(parts):
        digit = z3.BitVec(f'd{i}', NB)
        digits.append(digit)
        opt.add(1 <= digit)
        opt.add(digit <= 9)
        eval(part, regs, digit)

    print(regs['z'])
    opt.add(0 == regs['z'])
    for digit in digits:
        func(opt, digit)

    opt.check()

    model = opt.model()
    print(model)

    s = ""
    for d in digits:
        s += str(model[d].as_long())

    return(s)


def main(args):
    cmds = [s.strip() for s in open(args[1])]
    part1 = solve(cmds, lambda opt, d: opt.maximize(d))
    part2 = solve(cmds, lambda opt, d: opt.minimize(d))

    print(part1)
    print(part2)

if __name__ == '__main__':
    main(sys.argv)
