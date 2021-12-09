#!/usr/bin/env python3

import sys


def vadd(v1, v2):
    return tuple(x + y for x, y in zip(v1, v2))

UP, RIGHT, DOWN, LEFT = VDIRS = (0, -1), (1, 0), (0, 1), (-1, 0),

def search(m, spot):
    seen = set()
    stack = [spot]
    while stack:
        spot = stack.pop()
        if spot in seen:
            continue
        seen.add(spot)
        for dir in VDIRS:
            nbr = vadd(spot, dir)
            if nbr in m and m[nbr] != 9:
                stack.append(nbr)
    return seen


def main(args):
    data = [s.strip() for s in sys.stdin]
    data = [[int(x) for x in l] for l in data]

    m = {(i, j): v for i, l in enumerate(data) for j, v in enumerate(l)}

    lows = set()
    for spot, val in m.items():
        z = 0
        for dir in VDIRS:
            nbr = vadd(spot, dir)
            if nbr not in m or m[nbr] > val:
                z += 1
        if z == 4:
            lows.add(spot)

    basins = {lo: search(m, lo) for lo in lows}

    sizes = sorted([len(v) for v in basins.values()])
    lasts = sizes[-3:]

    print(sum(m[lo] for lo in lows) + len(lows))
    print(lasts[0]*lasts[1]*lasts[2])

if __name__ == '__main__':
    main(sys.argv)
