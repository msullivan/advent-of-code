#!/usr/bin/env python3

import sys
from collections import defaultdict

def left(dx,dy):
    if (dx,dy) == (1,0):
        return (0,-1)
    elif (dx,dy) == (0,-1):
        return (-1,0)
    elif (dx,dy) == (-1,0):
        return (0,1)
    else:
        return (1,0)

def right(dx,dy):
    return left(*left(*left(dx,dy)))

CLEAN = 0
WEAKENED = 1
INFECTED = 2
FLAGGED = 3

def main(args):
    nubs = [s.strip() for s in sys.stdin]

    grid = defaultdict(int)
    for y in range(len(nubs)):
        for x in range(len(nubs[0])):
            if nubs[y][x] == '#':
                grid[(x,y)] = INFECTED

    mid = len(nubs)//2

    dx, dy = 0, -1
    x, y = mid, mid

    made = 0
    for i in range(10000000):
        if grid[(x,y)] == CLEAN:
            dx, dy = left(dx, dy)
        elif grid[(x,y)] == WEAKENED:
            made += 1
        elif grid[(x,y)] == INFECTED:
            dx, dy = right(dx, dy)
        else:
            dx, dy = right(*right(dx, dy))
        grid[(x,y)] = (grid[(x,y)] + 1) % 4
        x += dx
        y += dy
    print(made)


if __name__ == '__main__':
    sys.exit(main(sys.argv))
