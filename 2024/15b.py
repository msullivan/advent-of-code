#!/usr/bin/env python3

import sys
from collections import defaultdict, Counter, deque
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

UP, RIGHT, DOWN, LEFT = VDIRS = (0, -1), (1, 0), (0, 1), (-1, 0),
DIRS = {'^': UP, '>': RIGHT, 'v': DOWN, '<': LEFT }

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

    nls = []
    for l in data[0]:
        nl = ""
        for c in l:
            if c == '#':
                nl += '##'
            elif c == 'O':
                nl += '[]'
            elif c == '.':
                nl += '..'
            elif c == '@':
                nl += '@.'
        nls.append(nl)


    #### Read grid
    m = defaultdict(lambda: '#')
    for y, l in enumerate(nls):
        for x, c in enumerate(l):
            m[x,y] = c
            if c == '@':
                robot = x,y
                m[x,y] = '.'

    def can(p, dir):
        np = vadd(p, dir)
        if m[p] in '[]' and dir in (UP, DOWN):
            if m[p] == '[':
                lc = can(np, dir)
                rc = can(vadd(np, RIGHT), dir)
            else:
                lc = can(vadd(np, LEFT), dir)
                rc = can(np, dir)
            return lc and rc
        elif m[p] in '[]':
            # return can(vadd(np, dir), dir)
            return can(np, dir)
        elif m[p] == '.':
            return True
        else:
            return False

    def move(p, dir):
        np = vadd(p, dir)
        if m[p] in '[]' and dir in (UP, DOWN):
            if m[p] == '[':
                move(np, dir)
                move(vadd(np, RIGHT), dir)
                m[p] = '.'
                m[np] = '['
                m[vadd(p, RIGHT)] = '.'
                m[vadd(np, RIGHT)] = ']'

            else:
                move(vadd(np, LEFT), dir)
                move(np, dir)

                m[p] = '.'
                m[np] = ']'
                m[vadd(p, LEFT)] = '.'
                m[vadd(np, LEFT)] = '['

        elif m[p] in '[]':
            move(vadd(np, dir), dir)
            m[vadd(np, dir)] = m[np]
            m[np] = m[p]
            m[p] = '.'

    for l in data[1]:
        for mc in l:
            dir = DIRS[mc]
            np = vadd(robot, dir)
            if can(np, dir):
                move(np, dir)
                robot = np

            # print(mc)
            # m[robot] = '@'
            # draw(m)
            # m[robot] = '.'

    draw(m)

    cksum = 0
    for (x, y), c in m.items():
        if c == '[':
            cksum += 100*(y) + x
    print(cksum)

if __name__ == '__main__':
    main(sys.argv)
