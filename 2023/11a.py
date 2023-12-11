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
DIRS = {'N': UP, 'E': RIGHT, 'S': DOWN, 'W': LEFT }
ALL_DIRS = [(x, y) for x in [-1,0,1] for y in [-1,0,1] if not x == y == 0]

def turn(v, d='left'):
    n = -1 if d == 'left' else 1
    return VDIRS[(VDIRS.index(v) + n + len(VDIRS))%len(VDIRS)]


##############################

def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    # data = [x.rstrip('\n').split('\n') for x in file.read().split('\n\n')]
    # data = [int(s.rstrip('\n')) for s in file]
    data = [s.rstrip('\n') for s in file]

    cols = set()
    rows = set()
    galaxies = set()

    m = defaultdict(lambda: '.')
    for y, l in enumerate(data):
        for x, c in enumerate(l):
            m[x, y] = c
            if c == '#':
                galaxies.add((x, y))
                rows.add(y)
                cols.add(x)

    new = []
    for i, x in enumerate(data):
        new.append(x)
        if '#' not in x:
            new.append(x)
    data = new

    new2 = []
    for y, r in enumerate(data):
        row = ""
        for x, c in enumerate(r):
            row += c
            if x not in cols:
                row += c
        new2.append(row)

    galaxies = []

    m = defaultdict(lambda: '.')
    for y, l in enumerate(new2):
        for x, c in enumerate(l):
            m[x, y] = c
            if c == '#':
                galaxies.append((x, y))
                rows.add(y)
                cols.add(x)

    print(galaxies)

    galaxies = list(galaxies)
    sum = 0
    n = 0
    for i, (x1, y1) in enumerate(galaxies):
        for j, (x2, y2) in enumerate(galaxies[i+1:]):
            j += i+1
            n += 1
            dst = abs(y2-y1) + abs(x2-x1)
            print(i+1, j+1, dst)
            sum += dst

    print(n)
    print(sum)

if __name__ == '__main__':
    main(sys.argv)
