#!/usr/bin/env python3

import sys
import re
from collections import defaultdict
import math

def extract(s):
    return [int(x) for x in re.findall(r'(-?\d+).?', s)]

def vadd(v1, v2):
    return tuple(x + y for x, y in zip(v1, v2))

def vsub(v1, v2):
    return tuple(x - y for x, y in zip(v1, v2))

def sign(x):
    return 0 if x == 0 else -1 if x < 0 else 1

UP, RIGHT, DOWN, LEFT = VDIRS = (0, -1), (1, 0), (0, 1), (-1, 0),

def draw(painted):
    minx = min(x for x, y in painted)
    miny = min(y for x, y in painted)
    maxx = max(x for x, y in painted)
    maxy = max(y for x, y in painted)

    l = ""
    for y in (list((range(miny, maxy+1)))):
        for x in range(minx, maxx+1):
            l += painted.get((x,y), ".")
        l += "\n"
    print(l)

def simulate(pos, m):
    while True:
        down = vadd(pos, DOWN)
        if m[down] == '.':
            pos = down
        elif m[dl := vadd(down, LEFT)] == '.':
            pos = dl
        elif m[dr := vadd(down, RIGHT)] == '.':
            pos = dr
        else:
            break
        if pos[1] > 1000:
            break
    return pos

def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    data = [s.rstrip('\n') for s in file]
    paths = [[tuple(extract(s)) for s in x.split('->')] for x in data]

    m = defaultdict(lambda: ".")
    for path in paths:
        start, *rest = path
        for end in rest:
            dx_ = vsub(end, start)
            dxn = tuple(sign(c) for c in dx_)
            m[end] = '#'
            while start != end:
                m[start] = '#'
                start = vadd(start, dxn)

    maxy = max(y for x, y in m)
    cnt = 0
    while True:
        new = simulate((500, 0), m)
        if new[1] > maxy:
            break
        m[new] = 'o'
        cnt += 1
        # print(new)
        # print()
        # print(cnt)
        # draw(m)

    draw(m)
    print(cnt)

if __name__ == '__main__':
    main(sys.argv)
