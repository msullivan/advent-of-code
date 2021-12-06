#!/usr/bin/env python3

import sys
from collections import defaultdict
import re

def extract(s, pos=False):
    p = '' if pos else '-?'
    return [int(x) for x in re.findall(fr'{p}\d+', s)]


def main(args):
    data = [extract(s.strip()) for s in sys.stdin]

    grid = defaultdict(int)
    # this is incredibly shit
    for x1,y1,x2,y2 in data:
        asdf = x1,y1,x2,y2
        x1, x2 = min(x1, x2), max(x1, x2)
        y1, y2 = min(y1, y2), max(y1, y2)

        if x1 == x2:
            for y in range(y1, y2+1):
                grid[x1,y] += 1
        elif y1 == y2:
            for x in range(x1, x2+1):
                grid[x,y1] += 1
        else:
            xf = asdf[0] != x1
            yf = asdf[1] != y1
            r = x2-x1 + 1
            x1,y1,x2,y2 = asdf
            xm = -1 if xf else 1
            ym = -1 if yf else 1
            for i in range(r):
                grid[x1+i*xm,y1+i*ym] += 1

    num = 0
    for val in grid.values():
        if val > 1:
            num += 1
    print(grid)

    print(num)

if __name__ == '__main__':
    sys.exit(main(sys.argv))
