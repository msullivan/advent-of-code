#!/usr/bin/env python3

import sys

from collections import defaultdict, Counter, deque
from parse import parse
import re

def extract(s):
    return [int(x) for x in re.findall(r'(-?\d+).?', s)]

def vadd(v1, v2):
    return tuple(x + y for x, y in zip(v1, v2))

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

def step(cnt, rules):
    ncnt = Counter()
    for k, v in cnt.items():
        if k in rules:
            c = rules[k]
            ncnt[k[0] + c] += v
            ncnt[c + k[1]] += v
        else:
            ncnt[k] += v
    return ncnt


def main(args):
    # data = [x.split('\n') for x in sys.stdin.read().split('\n\n')]
    # data = [int(s.strip()) for s in sys.stdin]
    data = [s.strip() for s in sys.stdin]
    target = data[0]
    rules = [x.split(" -> ") for x in data[2:]]
    rules = {k: v for k, v in rules}

    # s = target
    # for _ in range(10):
    #     s = step(s, rules)
    #     # print(s)
    #     cnt = Counter(s)
    #     print(max(cnt.values()), min(cnt.values()))

    s = target
    cnt = Counter(s[i:i+2] for i in range(len(s)-1))
    print(cnt)

    for _ in range(40):
        cnt = step(cnt, rules)
        # print(cnt)
        # print(s)

    lcnt = Counter()
    for k, v in cnt.items():
        lcnt[k[1]] += v

    lcnt[target[0]] += 1

    print(max(lcnt.values()) - min(lcnt.values()))


if __name__ == '__main__':
    main(sys.argv)
