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

def vsub(v1, v2):
    return tuple([x - y for x, y in zip(v1, v2)])

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

conns = {
    '|': 'NS',
    '-': 'EW',
    'L': 'NE',
    'J': 'NW',
    '7': 'SW',
    'F': 'SE',
}

##############################

def bfs(sset, inside, start):
    if start in sset or start in inside:
        return
    inside.add(start)
    q = deque([start])
    while q:
        n = q.popleft()
        if n == (-1, -1):
            print('ABORT')
            raise IndexError

        for d in DIRS.values():
            nbr = vadd(n, d)
            if nbr not in sset and nbr not in inside:
                inside.add(nbr)
                q.append(nbr)


def go(m, squares, dir):
    sset = set(squares)
    inside = set()
    for i in range(1, len(squares)):
        c = squares[i-1]
        n = squares[i]
        d = vsub(n, c)
        td = turn(d, dir)
        side1 = vadd(c, td)
        side2 = vadd(n, td)
        print(f'{c=} {n=} {d=} {td=} {side1=} {side2=}')
        bfs(sset, inside, side1)
        bfs(sset, inside, side2)

    print(len(inside))
    return inside



def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    # data = [x.rstrip('\n').split('\n') for x in file.read().split('\n\n')]
    # data = [int(s.rstrip('\n')) for s in file]
    data = [s.rstrip('\n') for s in file]


    m = defaultdict(lambda: '.')
    for y, l in enumerate(data):
        for x, c in enumerate(l):
            # if c == 'O' or c == 'I':
            #     c = '.'
            m[x, y] = c
            if c == 'S':
                start = (x, y)

    print(m)
    print(start)

    # for dname, x in DIRS.items():
    for dname in 'NWES':
        x = DIRS[dname]
        n = vadd(start, x)
        print(m[n])
        if m[n] in conns:
            k = conns[m[n]]
            out = None
            for i in range(2):
                if vadd(n, DIRS[k[i]]) == start:
                    out = i-1
                    outc = dname
            if out is not None:
                break

    print(n, out)
    cur = n
    ldir = outc
    print('fuck', ldir)
    # ldir = 'N' if ldir == 'S' else 'S' if ldir == 'N' else 'E' if ldir == 'W' else 'W'
    cnt = 1

    squares = [start, cur]

    print('start', cur, ldir)
    while cur != start:
        print('???', cur, m[cur], conns[m[cur]], ldir)
        ldir = 'N' if ldir == 'S' else 'S' if ldir == 'N' else 'E' if ldir == 'W' else 'W'
        ldir = conns[m[cur]].replace(ldir, '')
        cur = vadd(cur, DIRS[ldir])
        cnt += 1

        squares.append(cur)


    print(cnt//2)
    try:
        go(m, squares, 'left')
    except IndexError:
        go(m, squares, 'right')


if __name__ == '__main__':
    main(sys.argv)
