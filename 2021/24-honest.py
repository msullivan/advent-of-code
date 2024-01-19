#!/usr/bin/env python3

# This is very slow, though with the as_df suggested z threshold it is
# fine? Is that legit??
# 18m without, 27s with it

import sys
import math


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
            regs[a] = regs[a] + r2(b)
        elif x == 'mul':
            regs[a] = regs[a] * r2(b)
        elif x == 'div':
            regs[a] = int(regs[a] / r2(b))
        elif x == 'mod':
            regs[a] = regs[a] % r2(b)
        elif x == 'eql':
            regs[a] = int(regs[a] == r2(b))

def run(cmds, z, inp):
    regs = {k: 0 for k in 'wxyz'}
    regs['z'] = z
    eval(cmds, regs, inp)
    return regs['z']

def code(seen, k):
    digits = []
    while k in seen:
        digit, k = seen[k]
        digits.append(digit)
    return ''.join(reversed([str(d) for d in digits]))

def solve(parts, minimize):
    rng = range(9,0,-1) if minimize else range(1,10)

    seen = {}
    todo = [(0, 0)]
    while todo:
        idx, z = todo.pop()
        if idx < 6:
            print(len(todo), code(seen, (idx, z)), idx, z)
        if idx == len(parts) and z == 0:
            print("GOT IT")
            break
        if idx >= len(parts):
            continue
        for digit in rng:
            nz = run(parts[idx], z, digit)
            # XXX: as_df suggested this;; this is probably not quite sound
            # if nz > 26**5:
            #     continue
            k = (idx+1, nz)
            if k not in seen:
                seen[k] = (digit, (idx, z))
                todo.append(k)
    else:
        print("WRONG")

    return code(seen, (idx, z))

def main(args):
    cmds = [s.strip() for s in open(args[1])]

    parts = []
    cur = []
    for cmd in cmds:
        if cur and cmd.startswith('inp'):
            parts.append(cur)
            cur = []
        cur.append(cmd)
    parts.append(cur)

    part1 = solve(parts, minimize=False)
    part2 = solve(parts, minimize=True)

    print(part1)
    print(part2)

if __name__ == '__main__':
    main(sys.argv)
