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

def xgcd(a, b):
    """return (g, x, y) such that a*x + b*y = g = gcd(a, b)"""
    x0, x1, y0, y1 = 0, 1, 1, 0
    while a != 0:
        q, b, a = b // a, a, b % a
        y0, y1 = y1, y0 - q * y1
        x0, x1 = x1, x0 - q * x1
    return b, x0, y0


def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    data = [x.rstrip('\n').split('\n') for x in file.read().split('\n\n')]
    # data = [int(s.rstrip('\n')) for s in file]
    # data = [s.rstrip('\n') for s in file]

    ans = 0
    best = None
    for group in data:
        xa, ya = extract(group[0])
        xb, yb = extract(group[1])
        xt, yt = extract(group[2])

        # A = ((tx - ty) - b*(xb - yb)) / (xa - ya)

        xbp = xb * ya
        xtp = xt * ya
        ybp = yb * xa
        ytp = yt * xa
        if (xtp - ytp) == (xbp - ybp):
            print("FUCK", (xa, ya, xb, yb, xt, yt))
            continue  # ???

        B = (xtp - ytp) / (xbp - ybp)
        A = (xt - B * xb) / xa

        # print(xa, ya, xb, yb, xt, yt)
        # print(A, B)
        if int(A) == A and int(B) == B and A > 0 and B > 0:
            assert A*xa + B*xb == xt
            assert A*ya + B*yb == yt

            tokens = A*3 + B
            if tokens < ans:
                print('??', A, B, A*3 + B)
                # ans = tokens
                best = A, B, (xa, ya, xb, yb, xt, yt)
            ans += tokens
            # ans = min(tokens, ans)
            # if ans == tokens:
            #     best = A, B

    print('!!', best)
    print(int(ans))


if __name__ == '__main__':
    main(sys.argv)
