#!/usr/bin/env python3

import sys
import copy

def first(grid, x, y, dx, dy):
    while True:
        x += dx
        y += dy
        if x < 0 or x >= len(grid[0]) or y < 0 or y >= len(grid):
            return ''
        if grid[y][x] in ('L', '#'):
            return grid[y][x]

def step(grid):
    ngrid = copy.deepcopy(grid)
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            cnt = 0
            for i in range(-1,2):
                for j in range(-1,2):
                    if (i, j) == (0, 0): continue
                    # if x+i < 0 or x+i >= len(grid[0]) or y+j < 0 or y+j >= len(grid):
                    #     continue
                    tgt = first(grid, x, y, i, j)
                    if tgt == '#':
                        cnt += 1

            if grid[y][x] == 'L' and cnt == 0:
                ngrid[y][x] = '#'
            if grid[y][x] == '#' and cnt >= 5:
                ngrid[y][x] = 'L'

    return ngrid

def pp(grid):
    print("\n".join("".join(x) for x in grid))
    print()

def main(args):
    data = [s.strip() for s in sys.stdin]
    data = [list(s) for s in data]

    while True:
        pp(data)
        ndata = step(data)
        if ndata == data:
            break
        data = ndata

    cnt = 0
    for r in data:
        for x in r:
            if x == '#':
                cnt += 1

    print(cnt)

if __name__ == '__main__':
    sys.exit(main(sys.argv))
