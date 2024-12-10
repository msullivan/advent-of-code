#!/usr/bin/env python3

import sys
from collections import defaultdict, Counter, deque
from parse import parse
import re
import math
import itertools

def extract(s):
    return [int(x) for x in re.findall(r'(-?\d+).?', s)]

def vadd(v1, v2):
    if len(v1) == 2:
        return v1[0] + v2[0], v1[1] + v2[1]
    elif len(v1) == 2:
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

def turn(v, d='left'):
    n = -1 if d == 'left' else 1
    return VDIRS[(VDIRS.index(v) + n) % len(VDIRS)]


##############################

def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    # data = [x.rstrip('\n').split('\n') for x in file.read().split('\n\n')]
    # data = [int(s.rstrip('\n')) for s in file]
    data = [s.rstrip('\n') for s in file]

    zeros = set()
    m = defaultdict(lambda: -1)
    for y, l in enumerate(data):
        for x, c in enumerate(l):
            m[x, y] = int(c) if c != '.' else -1
            if c == '0':
                zeros.add((x, y))


    print(m)
    print(zeros)

    fuck = set()
    def cnt(v):
        if m[v] == 9:
            fuck.add(v)
            return 1

        if m[v] == -1:
            return 0

        s = 0
        for d in VDIRS:
            p = vadd(v, d)
            if m[p] == m[v] + 1:
                s += cnt(p)

        return s

    s = 0
    for v in zeros:
        fuck.clear()
        cnt(v)
        s += len(fuck)

    x = sum(cnt(v) for v in zeros)
    print(s)

if __name__ == '__main__':
    main(sys.argv)
