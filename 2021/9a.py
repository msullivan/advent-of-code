#!/usr/bin/env python3

import sys

import re

def vadd(v1, v2):
    return tuple(x + y for x, y in zip(v1, v2))

UP, RIGHT, DOWN, LEFT = VDIRS = (0, -1), (1, 0), (0, 1), (-1, 0),

def main(args):
    data = [s.strip() for s in sys.stdin]
    data = [[int(x) for x in l] for l in data]

    m = {}
    for i in range(len(data)):
        for j in range(len(data[0])):
            m[i,j] = data[i][j]

    lows = set()
    for spot, val in m.items():
        z = 0
        for dir in VDIRS:
            nbr = vadd(spot, dir)
            if nbr not in m or m[nbr] > val:
                z += 1
        if z == 4:
            lows.add(spot)


    print(sum(m[lo] for lo in lows) + len(lows))

if __name__ == '__main__':
    main(sys.argv)
