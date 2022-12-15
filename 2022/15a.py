#!/usr/bin/env python3

import sys
import re

def extract(s):
    return [int(x) for x in re.findall(r'(-?\d+).?', s)]

def vsub(v1, v2):
    return (v1[0]-v2[0], v1[1]-v2[1])

def mag(v):
    return abs(v[0]) + abs(v[1])

def turn(v, d='left'):
    n = -1 if d == 'left' else 1
    return VDIRS[(VDIRS.index(v) + n + len(VDIRS))%len(VDIRS)]


##############################

def isin(spots, pos):
    for p, _, sz in spots:
        if mag(vsub(p, pos)) <= sz:
            return True
    return False

def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    data = [extract(s) for s in file]

    xmin = 1000000000000000000
    xmax = -100000000000000000
    maxsz = 0
    spots = []
    beacs = set()
    for line in data:
        a, b, c, d = line
        xmin = min(xmin, a)
        xmax = max(xmax, b)
        p1, p2 = (a, b), (c, d)
        beacs.add(p2)
        sz = mag(vsub(p2, p1))
        maxsz = max(sz, maxsz)
        spots.append((p1, p2, sz))

    Y = 2000000
    cnt = 0
    for x in range(xmin-maxsz-20, xmax+maxsz+20):
        if x % 10000 == 0:
            print(x, xmax+maxsz+20)
        p = (x, Y)
        if p not in beacs and isin(spots, p):
            cnt += 1

    print(xmin, xmax)
    print(maxsz)
    print(cnt)



if __name__ == '__main__':
    main(sys.argv)
