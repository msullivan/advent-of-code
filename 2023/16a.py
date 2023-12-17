#!/usr/bin/env python3

import sys
from collections import defaultdict, Counter, deque
from parse import parse
import re
import math

def extract(s):
    return [int(x) for x in re.findall(r'(-?\d+).?', s)]

def vadd(v1, v2):
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
U, R, D, L = VDIRS
DIRS = {'N': UP, 'E': RIGHT, 'S': DOWN, 'W': LEFT }
ALL_DIRS = [(x, y) for x in [-1,0,1] for y in [-1,0,1] if not x == y == 0]

def turn(v, d='left'):
    n = -1 if d == 'left' else 1
    return VDIRS[(VDIRS.index(v) + n + len(VDIRS))%len(VDIRS)]


MOVES = {
    '|': { R: [U, D], L: [U, D] },
    '-': { U: [L, R], D: [L, R] },
    '/': { R: [U], D: [L], L: [D], U: [R]},
    '\\': { R: [D], D: [R], L: [U], U: [L]},
}

##############################

def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    # data = [x.rstrip('\n').split('\n') for x in file.read().split('\n\n')]
    # data = [int(s.rstrip('\n')) for s in file]
    data = [s.rstrip('\n') for s in file]

    m = {}
    for y, l in enumerate(data):
        for x, c in enumerate(l):
            m[x, y] = c

    q = [((-1, 0), R)]
    seen = set()
    while q:
        print(len(q))
        el = q.pop()
        if el in seen:
            continue
        seen.add(el)
        sp, dir = el

        nsp = vadd(sp, dir)
        if nsp not in m:
            # print("SKIP")
            continue
        c = m[nsp]
        if c in MOVES and dir in MOVES[c]:
            for ndir in MOVES[c][dir]:
                q.append((nsp, ndir))
        else:
            q.append((nsp, dir))

    print(len({x for x, _ in seen}) - 1)

if __name__ == '__main__':
    main(sys.argv)
