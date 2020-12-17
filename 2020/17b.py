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
    ngrid = copy.deepcopy(grid)
    # ngrid = [x[:] for x in grid]
    change = False
    for pos in list(grid):
        for dx in nbrs + [(0, 0, 0, 0)]:
            npos = add(dx, pos)
            cnt = 0
            for d in nbrs:
                if grid[add(npos, d)] == "#":
                    cnt += 1

            # print(cnt)
            if grid[npos] == '#' and not (cnt == 2 or cnt == 3):
                ngrid[npos] = '.'
                change = True
            elif grid[npos] == '.' and cnt == 3:
                ngrid[npos] = '#'
                change = True

    return ngrid, change


def main(args):
    # data = [x.split('\n') for x in sys.stdin.read().split('\n\n')]
    data = [list(s.strip()) for s in sys.stdin]
    grid = defaultdict(lambda: ".")

    for y in range(len(data)):
        for x in range(len(data[0])):
            grid[x,y,0,0] = data[y][x]

    for i in range(6):
        print(i, grid)
        grid, _ = step(grid)

    print(len(grid))
    print(len([x for x in grid.values() if x == '#']))

if __name__ == '__main__':
    sys.exit(main(sys.argv))
