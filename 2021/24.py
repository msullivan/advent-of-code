#!/usr/bin/env python3

"""
00:20 < sully> this could be a Z3 day.
00:29 < sully> "A sword day, a red day."
"""

import sys
import z3


def test(x, b):
    return isinstance(x, int) and x == b

def eval(cmds, regs, inp):
    def r2(x):
        if x.isalpha():
            return regs[x]
        else:
            return int(x)

    for cmd in cmds:
        x, *rest = cmd.split(" ")
        if x == 'inp':
            regs[rest[0]] = inp
            continue
        a, b = rest

        if x == 'add':
            if not test(r2(b), 0):
                regs[a] = regs[a] + r2(b)
        elif x == 'mul':
            if test(r2(b), 0):
                regs[a] = 0
            else:
                if not test(r2(b), 1):
                    regs[a] = regs[a] * r2(b)
        elif x == 'div':
            if not test(r2(b), 1):
                regs[a] = regs[a] / r2(b)
        elif x == 'mod':
            regs[a] = regs[a] % r2(b)
        elif x == 'eql':
            regs[a] = z3.If(regs[a] == r2(b), 1, 0)


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
    regs = {k: 0 for k in 'wxyz'}
    opt = z3.Optimize()
    for i, part in enumerate(parts):
        digit = z3.Int(f'd{i}')
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
