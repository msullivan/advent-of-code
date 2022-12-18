#!/usr/bin/env python3

import sys
import re

def extract(s):
    return [int(x) for x in re.findall(r'(-?\d+).?', s)]

def vadd(v1, v2):
    return tuple(x + y for x, y in zip(v1, v2))

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
    # Find a bounding box for all the points
    coords = list(zip(*pts))
    pmin = tuple(min(c)-1 for c in coords)
    pmax = tuple(max(c)+1 for c in coords)
    print(pmin, pmax)

    # Find all of the squares that are "outside".
    # My original solution that finished #16th did an unsound version of this,
    # based on eyeballing the input: I always started at (0, 0, 0) and bounded
    # it at points with magnitude 50.
    wl = [(pmin)]
    outside = set()
    while wl:
        x = wl.pop()
        outside.add(x)
        for d in VDIRS3:
            nb = vadd(x, d)
            if nb not in pts and nb not in outside and all(
                pmin[i] <= nb[i] <= pmax[i] for i in (0, 1, 2)
            ):
                wl.append(nb)

    total = 0
    for pt in pts:
        for d in VDIRS3:
            if vadd(pt, d) in outside:
                total += 1

    print(total)

if __name__ == '__main__':
    main(sys.argv)
