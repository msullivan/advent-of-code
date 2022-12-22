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
FDIRS = [RIGHT, DOWN, LEFT, UP]

def turn(v, d='left'):
    n = -1 if d == 'left' else 1
    return VDIRS[(VDIRS.index(v) + n + len(VDIRS))%len(VDIRS)]


##############################
def draw(painted):
    minx = min(x for x, y in painted)
    miny = min(y for x, y in painted)
    maxx = max(x for x, y in painted)
    maxy = max(y for x, y in painted)

    l = ""
    # XXX: add reversed if needed
    for y in list((range(miny, maxy+1))):
        for x in range(minx, maxx+1):
            l += painted.get((x,y), ".")
        l += "\n"
    print(l)


def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    data = [x.rstrip('\n').split('\n') for x in file.read().split('\n\n')]
    # data = [int(s.rstrip('\n')) for s in file]
    # data = [s.rstrip('\n') for s in file]
    mapo, cmd = data

    m = defaultdict(lambda: ' ')
    for y, line in enumerate(mapo):
        for x, c in enumerate(line):
            m[(x, y)] = c

    cmd = cmd[0].replace('R', ' R ').replace('L', ' L ').split()
    print(cmd)

    # print(mapo)
    draw(m)

    for x in range(len(mapo[0])):
        if m[(x, 0)] == '.':
            start = (x, 0)
            break

    def wrap(p, f):
        if m[p] != ' ':
            return p
        rf = (-f[0], -f[1])
        while True:
            np = vadd(p, rf)
            if m[np] == ' ':
                return p
            p = np

    print(start)
    facing = (1, 0)
    for entry in cmd:
        if entry == 'L':
            facing = turn(facing, 'left')
        elif entry == 'R':
            facing = turn(facing, 'right')
        else:
            amt = int(entry)
            for _ in range(amt):
                nstart = wrap(vadd(start, facing), facing)
                if m[nstart] == '#':
                    break
                start = nstart

        print(start, facing)

    print(start, facing)
    print((start[1]+1)*1000 + 4*(start[0]+1) + FDIRS.index(facing))



if __name__ == '__main__':
    main(sys.argv)
