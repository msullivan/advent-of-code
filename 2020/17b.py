#!/usr/bin/env python3

import copy
from collections import defaultdict
import sys
import re

def extract(s):
    return [int(x) for x in re.findall(r'-?\d+', s)]

def first(grid, x, y, dx, dy):
    while True:
        x += dx
        y += dy
        if x < 0 or x >= len(grid[0]) or y < 0 or y >= len(grid):
            return ''
        if grid[y][x] in ('L', '#'):
            return grid[y][x]

nbrs = [(x, y, z, w) for x in range(-1, 2) for y in range(-1, 2) for z in range(-1, 2) for w in range(-1, 2) if not x == y == z == w == 0]

def add(v1, v2):
    return tuple(x + y for x, y in zip(v1, v2))

def step(grid):
    ngrid = set()

    squares = grid | {add(dx, pos) for pos in grid for dx in nbrs}

    for npos in squares:
        cnt = 0
        for d in nbrs:
            if add(npos, d) in grid:
                cnt += 1

        if npos in grid and (cnt == 2 or cnt == 3):
            ngrid.add(npos)
        elif npos not in grid and cnt == 3:
            ngrid.add(npos)

    return ngrid


def main(args):
    data = [list(s.strip()) for s in sys.stdin]

    grid = set()
    for y in range(len(data)):
        for x in range(len(data[0])):
            if data[y][x] == '#':
                grid.add((x,y,0,0))

    for i in range(6):
        # print(i, grid)
        grid = step(grid)

    print(len(grid))

if __name__ == '__main__':
    sys.exit(main(sys.argv))
