#!/usr/bin/env python3

import sys

import re

def extract(s, pos=False):
    p = '' if pos else '-?'
    return [int(x) for x in re.findall(fr'{p}\d+', s)]

def main(args):
    data = [extract(s.strip()) for s in sys.stdin]

    grid = defaultdict(int)
    for x1,y1,x2,y2 in data:
        x1, x2 = min(x1, x2), max(x1, x2)
        y1, y2 = min(y1, y2), max(y1, y2)
        assert x1 <= x2
        assert y1 <= y2, (y1, y2)

        if x1 == x2:
            for y in range(y1, y2+1):
                grid[x1,y] += 1
        elif y1 == y2:
            for x in range(x1, x2+1):
                grid[x,y1] += 1

    num = 0
    for val in grid.values():
        if val > 1:
            num += 1
    print(grid)

    print(num)

if __name__ == '__main__':
    sys.exit(main(sys.argv))
