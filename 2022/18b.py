#!/usr/bin/env python3

import sys
import re

def extract(s):
    return [int(x) for x in re.findall(r'(-?\d+).?', s)]

def vadd(v1, v2):
    return tuple(x + y for x, y in zip(v1, v2))

def mag(v):
    return abs(v[0]) + abs(v[1]) + abs(v[2])

VDIRS3 = (0, -1, 0), (1, 0, 0), (0, 1, 0), (-1, 0, 0), (0, 0, 1), (0, 0, -1)

def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    data = [tuple(extract(s.rstrip('\n'))) for s in file]
    pts = set(data)

    # Part 1
    total = 0
    for pt in pts:
        for d in VDIRS3:
            if vadd(pt, d) not in pts:
                total += 1
    print(total)

    # Part 2

    # Find all of the squares reachable from "outside".
    # This is unsound, since I just eyeballed the input, saw it looked like
    # everything was greater than 0, and figured we were good.

    wl = [(0,0,0)]
    avail = set()
    while wl:
        x = wl.pop()
        avail.add(x)
        for d in VDIRS3:
            nb = vadd(x, d)
            if nb not in pts and mag(nb) < 50 and nb not in avail:
                wl.append(nb)

    total = 0
    for pt in pts:
        for d in VDIRS3:
            if vadd(pt, d) in avail:
                total += 1

    print(total)

if __name__ == '__main__':
    main(sys.argv)
