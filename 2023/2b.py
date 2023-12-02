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

    cap = {'red': 12, 'green': 13, 'blue': 14}

    sum = 0
    for line in data:
        game, rest = line.split(": ")
        chunks = rest.split('; ')
        parts = [[y.split(' ') for y in x.split(', ')] for x in chunks]
        ds = []
        for part in parts:
            print(part)
            asdf = {k: int(v) for v, k in part}
            ds.append(asdf)

        pwr = 1
        for c in cap:
            pwr *= max(d.get(c, 0) for d in ds)
            print(pwr)
        sum += pwr

        # ok = all(
        #     all(v <= cap[k] for k, v in d.items())
        #     for d in ds
        # )
        # if ok:
        #     sum += extract(game)[0]

    print(sum)

if __name__ == '__main__':
    main(sys.argv)
