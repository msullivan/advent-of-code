#!/usr/bin/env python3

import sys
import re

def extract(s):
    return [int(x) for x in re.findall(r'(-?\d+).?', s)]

def vadd(v1, v2):
    return tuple([x + y for x, y in zip(v1, v2)])

def to_std(s, v):
    s0 = s
    s1 = vadd(s0, v)
    x0, y0, _ = s0
    x1, y1, _ = s1
    m = (y1-y0)/(x1-x0)
    b = y0 - m*x0

    return m, b

def intersect(e1, e2):
    m0, b0 = e1
    m1, b1 = e2

    if m0 == m1:
        return None
    x = (b1-b0) / (m0 - m1)
    y = m0*x + b0
    return x, y


def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    data = [extract(s.rstrip('\n')) for s in file]
    data = [(tuple(x[:3]), tuple(x[3:])) for x in data]

    pmin, pmax = 7, 27
    pmin = 200000000000000
    pmax = 400000000000000

    eqns = [to_std(*x) for x in data]

    cnt = 0
    for i, ((s1, v1), eqn1) in enumerate(zip(data, eqns)):
        for j, ((s2, v2), eqn2) in enumerate(zip(data, eqns)):
            if j <= i:
                continue
            int = intersect(eqn1, eqn2)
            if not int:
                continue
            x, y = int
            if not (pmin <= x <= pmax and pmin <= y <= pmax):
                continue
            if (x >= s1[0]) != (v1[0] >= 0):
                continue
            if (x >= s2[0]) != (v2[0] >= 0):
                continue

            cnt += 1


    print(cnt)

if __name__ == '__main__':
    main(sys.argv)
