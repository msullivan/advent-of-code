#!/usr/bin/env python3

# just because I like feeling bad

import sys
import re
from z3 import Int, If, Optimize

def extract(s):
    return [int(x) for x in re.findall(r'(-?\d+).?', s)]

def vsub(v1, v2):
    return (v1[0]-v2[0], v1[1]-v2[1])

def mag(v):
    return abs(v[0]) + abs(v[1])

def z3_abs(x):
    return If(x >= 0,x,-x)

def z3_dist(x, y):
    return z3_abs(x[0] - y[0]) + z3_abs(x[1] - y[1])

def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    data = [extract(s) for s in file]

    spots = []
    for line in data:
        a, b, c, d = line
        p1, p2 = (a, b), (c, d)
        sz = mag(vsub(p2, p1))
        spots.append((p1, p2, sz))

    M = 4000000

    x = Int('x')
    y = Int('y')
    orig = (x, y)
    opt = Optimize() # ??
    opt.add(x >= 0)
    opt.add(x <= M)
    opt.add(y >= 0)
    opt.add(y <= M)

    for pos, _, sz in spots:
        opt.add(z3_dist(orig, pos) > sz)
    print("let's go")
    opt.check()
    model = opt.model()
    pos = (model[x].as_long(), model[y].as_long())
    print(pos)
    print(pos[0] * M + pos[1])


if __name__ == '__main__':
    main(sys.argv)
