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

def mix(s, n):
    return s ^ n

def prune(s):
    return s % 16777216

def compute(n, i):
    for _ in range(i):
        n = mix(n * 64, n) % 16777216
        n = mix(n // 32, n) % 16777216
        n = mix(n * 2048, n) % 16777216
    return n


def compute(n, i):
    prices = []
    prices.append(n % 10)
    for _ in range(i):
        n = mix(n * 64, n) % 16777216
        n = mix(n // 32, n) % 16777216
        n = mix(n * 2048, n) % 16777216
        prices.append(n % 10)
    return prices


def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    # data = [x.rstrip('\n').split('\n') for x in file.read().split('\n\n')]
    data = [int(s.rstrip('\n')) for s in file]
    # data = [s.rstrip('\n') for s in file]

    scores = defaultdict(int)
    for n in data:
        seen = set()
        prices = compute(n, 2000)
        diffs = [None] + [prices[i] - prices[i-1] for i in range(1, len(prices))]
        for i in range(4, len(prices)):
            d = tuple(diffs[i-3:i+1])
            if d not in seen:
                seen.add(d)
                scores[d] += prices[i]


    print(max(scores.values()))
    # print(sum(compute(n, 2000) for n in data))


if __name__ == '__main__':
    main(sys.argv)
