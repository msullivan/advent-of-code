#!/usr/bin/env python3

import sys

def hash(lens):
    l = list(range(256))
    cur = 0
    skip = 0

    for i in range(64):
        for ln in lens:
            lurr = l+l
            sub = list(reversed(lurr[cur:cur+ln]))
            for i in range(ln):
                l[(cur+i)%len(l)] = sub[i]
            cur = (cur + ln + skip) % len(l)
            skip += 1

    return l

def ihash(s):
    lens = list(map(ord, s))+[17, 31, 73, 47, 23]

    h = hash(lens)
    sparse = []
    for i in range(16):
        x = 0
        for j in range(16):
            x ^= h[i*16+j]
        sparse += [x]

    return sparse

def idx(h, i):
    # asdf endian
    return (h[i//8]&(1<<(7-(i%8)))) != 0

def floodfill(grid, x, y):
    if x < 0 or x >= len(grid) or y < 0 or y >= len(grid[0]): return
    if not grid[x][y]: return
    grid[x][y] = None
    floodfill(grid, x-1, y)
    floodfill(grid, x+1, y)
    floodfill(grid, x, y+1)
    floodfill(grid, x, y-1)


def main(args):
    s = args[0] if len(args) > 1 else "ffayrhll"

    grid = []
    count = 0
    for i in range(128):
        data = ihash(s + "-" + str(i))
        row = []
        for j in range(128):
            row.append(idx(data, j))
            if idx(data, j): count+=1
        grid += [row]

    print(count)

    regions = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j]:
                regions += 1
                floodfill(grid, i, j)

    print(regions)

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
