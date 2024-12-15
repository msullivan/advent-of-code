#!/usr/bin/env python3

import sys
from collections import defaultdict, Counter, deque
from parse import parse
import re
import math
import itertools
import heapq

def extract(s):
    return [int(x) for x in re.findall(r'(-?\d+).?', s)]

def vadd(v1, v2):
    if len(v1) == 2:
        return v1[0] + v2[0], v1[1] + v2[1]
    elif len(v1) == 3:
        return v1[0] + v2[0], v1[1] + v2[1], v1[2] + v2[2]
    else:
        # ... this is so slow.
        return tuple([x + y for x, y in zip(v1, v2)])

def ichr(i):
    return chr(ord('a') + i)

def iord(c):
    return ord(c.lower()) - ord('a')

def optidx(d, opt=max, nth=0):
    if not isinstance(d, dict):
        d = dict(enumerate(d))
    rv = opt(d.values())
    return [i for i, v in d.items() if v == rv][nth], rv

LETTERS = "abcdefghijklmnopqrstuvwxyz"

UP, RIGHT, DOWN, LEFT = VDIRS = (0, -1), (1, 0), (0, 1), (-1, 0),
DIRS = {'N': UP, 'E': RIGHT, 'S': DOWN, 'W': LEFT }
ALL_DIRS = [(x, y) for x in [-1,0,1] for y in [-1,0,1] if not x == y == 0]

def gnbrs(s, dirs=VDIRS):
    return [(dir, vadd(s, dir)) for dir in dirs]

def turn(v, d='left'):
    n = -1 if d == 'left' else 1
    return VDIRS[(VDIRS.index(v) + n) % len(VDIRS)]


##############################

def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    # data = [x.rstrip('\n').split('\n') for x in file.read().split('\n\n')]
    # data = [int(s.rstrip('\n')) for s in file]
    data = [s.rstrip('\n') for s in file]

    ps = []
    vs = []
    for line in data:
        a, b, c, d = extract(line)
        ps.append((a, b))
        vs.append((c, d))

    W = 101
    H = 103
    #11 7

    print(ps)
    print(vs)
    for i in range(100):
        nps = []
        for p, v in zip(ps, vs):
            a, b = vadd(p, v)
            np = (a % W, b % H)
            nps.append(np)

        ps = nps

    q1 = q2 = q3 = q4 = 0
    for x, y in nps:
        if x < W//2 and y < H//2:
            q1 += 1
        elif x < W//2 and y > H//2:
            q2 += 1
        elif x > W//2 and y > H//2:
            q3 += 1
        elif x > W//2 and y < H//2:
            q4 += 1

    print(q1*q2*q3*q4)

if __name__ == '__main__':
    main(sys.argv)
