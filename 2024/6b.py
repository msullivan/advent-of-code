#!/usr/bin/env python3

import sys
from collections import defaultdict, Counter, deque
import re
import math

def extract(s):
    return [int(x) for x in re.findall(r'(-?\d+).?', s)]

def vadd(v1, v2):
    if len(v1) == 2:
        return v1[0] + v2[0], v1[1] + v2[1]
    elif len(v1) == 2:
        return v1[0] + v2[0], v1[1] + v2[1], v1[2] + v2[2]
    else:
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

def _try(m, pos, fuck):
    # print(pos)
    m = m.copy()
    m[fuck] = '#'

    seen = set()
    dir = UP
    while m[pos] != 'O':
        # print(pos, dir)
        if (pos, dir) in seen:
            # print("!!!!")
            return True
        seen.add((pos, dir))
        nxt = vadd(dir, pos)
        if m[nxt] == '#':
            dir = turn(dir, d='right')
        else:
            pos = nxt

    return False



def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    # data = [x.rstrip('\n').split('\n') for x in file.read().split('\n\n')]
    # data = [int(s.rstrip('\n')) for s in file]
    data = [s.rstrip('\n') for s in file]


    m = defaultdict(lambda: 'O')
    for y, l in enumerate(data):
        for x, c in enumerate(l):
            m[x, y] = c
            if c == '^':
                pos = x, y

    print(len(m))

    n = 0
    i = 0
    for spot, c in m.items():
        i += 1
        if spot != pos and c == '.':
            print(i, spot)
            if _try(m, pos, spot):
                n += 1
    # print(m)
    # m[pos] = '.'
    # print(pos)

    # print(_try(m, pos, (3, 6)))


    # print(len(seen))
    print(n)


if __name__ == '__main__':
    main(sys.argv)
