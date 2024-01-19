#!/usr/bin/env python3

# 3.5m without the toobigs optimization
# 150ms with it

import sys
import math
import operator, functools


def consts(cmds):
    return tuple(int(cmds[i].split(" ")[2]) for i in [4,5,15])

def func(consts, z, w):
    a, b, c = consts

    flag = (z % 26 + b) != w
    z = int(z / a)
    if flag:
        z = z * 26 + c + w

    return z

def product(l):
    return functools.reduce(operator.mul, l)

def code(seen, k):
    digits = []
    while k in seen:
        digit, k = seen[k]
        digits.append(digit)
    return ''.join(reversed([str(d) for d in digits]))

def solve(parts, minimize):
    rng = range(9,0,-1) if minimize else range(1,10)

    cparts = [consts(x) for x in parts]
    for c in cparts:
        print(c)

    # the function divides by a, and c is always positive, so the divides by a
    # are the only way z gets smaller; we can use this fact to do pruning when
    # z is too big to be eliminated by the remaining divisions
    toobigs = (
        [product([a for a, _, _ in cparts[i:]]) for i in range(len(cparts))] + [0])

    seen = {}
    todo = [(0, 0)]
    while todo:
        idx, z = todo.pop()
        if idx < 6:
            print(len(todo), code(seen, (idx, z)), idx, z)
        if idx == len(parts) and z == 0:
            break
        if idx >= len(parts):
            continue
        for digit in rng:
            nz = func(cparts[idx], z, digit)
            # addition is to deal with truncating I guess
            if nz > toobigs[idx+1] + len(parts):
                continue
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
