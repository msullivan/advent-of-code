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


#####




##############################

def draw(painted, fuck, lu):
    minx = min(x for x, y in painted)
    miny = min(y for x, y in painted)
    maxx = max(x for x, y in painted)
    maxy = max(y for x, y in painted)

    l = ""
    maxx *= 1
    maxy *= 1
    # XXX: add reversed if needed
    for y in list((range(miny, maxy+1))):
        for x in range(minx, maxx+1):
            # x += 131
            # y += 131
            if (x,y) in fuck:
                l += "O"
            else:
                # l += painted.get((x,y), ".")
                l += lu((x,y))
        l += "\n"
    print(l)


def amod(x, n):
    return ((x % n) + n) % n


def run(data, m, start):

    def lu(p):
        x, y = p
        x = amod(x, len(data[0]))
        y = amod(y, len(data))
        return m[x, y]

    cnt = []
    spots = {start}
    back = None
    while True:
        cnt.append(len(spots))
        # draw(m, spots, lu)
        nxt = set()
        for n in spots:
            for dnbr in VDIRS:
                nbr = vadd(n, dnbr)
                if lu(nbr) == '.' and nbr in m:
                    nxt.add(nbr)
        # print(len(cnt)-1, len(nxt), len(nxt) - len(spots))
        if nxt == back:
            break
        back = spots
        spots = nxt

    return cnt



def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    # data = [x.rstrip('\n').split('\n') for x in file.read().split('\n\n')]
     # data = [int(s.rstrip('\n')) for s in file]
    data = [s.rstrip('\n') for s in file]

    m = {}
    for y, l in enumerate(data):
        for x, c in enumerate(l):
            if c == 'S':
                start = (x,y)
                c = '.'
            m[x, y] = c

    print(len(data[0]), len(data))
    print(start)

    N = len(data)
    S = start[0]

    cnts = run(data, m, start)
    print(cnts)
    print(len(cnts))

    fcnts = []
    flat = [(0, S), (N-1, S), (S, 0), (S, N-1)]
    for s in flat:
        cnts = run(data, m, s)
        fcnts.append(cnts)
        print(cnts)
        print(len(cnts))

    dcnts = []
    diag = [(0, 0), (N-1, 0), (0, N-1), (N-1, N-1)]
    for s in flat:
        cnts = run(data, m, s)
        dcnts.append(cnts)
        print(cnts)
        print(len(cnts))


if __name__ == '__main__':
    main(sys.argv)
