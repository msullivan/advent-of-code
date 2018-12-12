#!/usr/bin/env python3

import sys
from collections import defaultdict, deque

input = 2694
#input = 18

def eval(x, y, input):
    power = ((x + 10) * y + input) * (x + 10)
    power = (power % 1000) // 100
    power -= 5
    return power


def sums(vals):
    grids = defaultdict(int)
    def f(x, y):
        if (x, y) not in vals: return 0
        if (x, y) in grids: return grids[x, y]
        grids[x, y] = vals[x, y] + f(x - 1, y) + f(x, y - 1) - f(x - 1, y - 1)
        return grids[x, y]
    f(300, 300)
    return grids

def main(args):
    vals = {}
    for x in range(1, 301):
        for y in range(1, 301):
            vals[(x,y)] = eval(x, y, input)

    grids = sums(vals)
    print(grids)

    things = []
    for size in range(1, 301):
        for x in range(1, 301 - size):
            for y in range(1, 301 - size):
                s = size
                val = grids[x+s-1, y+s-1] - grids[x+s-1,y-1] - grids[x-1,y+s-1] + grids[x-1,y-1]
                things += [(val, (x, y, s))]
    print(max(things))

if __name__ == '__main__':
    sys.exit(main(sys.argv))
