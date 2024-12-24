#!/usr/bin/env python3

import sys
from collections import defaultdict, Counter, deque
# from parse import parse
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
    data = [x.rstrip('\n').split('\n') for x in file.read().split('\n\n')]
    # data = [int(s.rstrip('\n')) for s in file]
    # data = [s.rstrip('\n') for s in file]

    inits = data[0]
    exprs = data[1]

    vals = {}
    for init in inits:
        print(init)
        n, v = init.split(': ')
        vals[n] = int(v)

    evals = {}
    for cmd in exprs:
        v1, op, v2, _, res = cmd.split(' ')
        evals[res] = v1, op, v2

    def eval(v):
        if v in vals:
            return vals[v]

        v1, op, v2 = evals[v]
        n1 = eval(v1)
        n2 = eval(v2)
        if op == 'AND':
            r = n1 & n2
        elif op == 'OR':
            r = n1 | n2
        else:
            r = n1 ^ n2
        vals[v] = r
        return r


    names = vals.keys() | evals.keys()
    zs = [z for z in names if z[0] == 'z']
    zs.sort()
    zs.reverse()

    v = 0
    for z in zs:
        v <<= 1
        v |= eval(z)

    print(v)

if __name__ == '__main__':
    main(sys.argv)
