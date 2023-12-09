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

def extrapolate(l):
    ls = [l]
    while any(l):
        nl = []
        for i in range(len(l)-1):
            nl.append(l[i+1] - l[i])
        l = nl
        ls.append(nl)

    ls[-1].append(0)
    for i in reversed(list(range(len(ls)-1))):
        xl = ls[i+1]
        ls[i].append(ls[i][-1] + xl[-1])

    # for x in ls:
    #     print(x)
    # print(ls[0][-1])
    return ls[0][-1]


def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    # data = [x.rstrip('\n').split('\n') for x in file.read().split('\n\n')]
    # data = [int(s.rstrip('\n')) for s in file]
    data = [extract(s.rstrip('\n')) for s in file]

    # print(data)
    print(sum(extrapolate(d) for d in data))
    # extrapolate(data[0])

if __name__ == '__main__':
    main(sys.argv)
