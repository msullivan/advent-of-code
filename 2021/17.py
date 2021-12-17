#!/usr/bin/env python3

import sys
import re

def extract(s):
    return [int(x) for x in re.findall(r'(-?\d+).?', s)]


def inside(coord, box):
    minx, maxx, miny, maxy = box
    x, y = coord
    return (minx <= x <= maxx) and (miny <= y <= maxy)

def step(pos, v):
    x, y = pos
    dx, dy = v
    x += dx
    y += dy
    dy -= 1
    if dx > 0:
        dx -= 1
    elif dx < 0:
        dx += 1

    return (x, y), (dx, dy)

def sim(pos, v, box):
    trace = [pos]
    while True:
        if inside(pos, box):
            return True, trace
        if pos[0] > box[1]:
            return 0, trace
        if pos[1] < box[2]:
            return 0, trace

        pos, v = step(pos, v)
        trace.append(pos)

def main(args):
    data = [s.strip() for s in sys.stdin]
    minx, maxx, miny, maxy = extract(data[0])
    box = minx, maxx, miny, maxy

    topy = 0
    count = 0
    N = 1000  # sure, whatever
    for dx in range(N):
        for dy in range(-N, N):
            if dx == dy == 0: continue
            hit, trace = sim((0, 0), (dx, dy), box)
            if hit:
                top = max(y for x, y in trace)
                topy = max(top, topy)
                count += 1

    print(topy)
    print(count)

if __name__ == '__main__':
    main(sys.argv)
