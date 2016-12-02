#!/usr/bin/env python3

import sys

DIRS = {"U": (0,-1), "D": (0,1), "L": (-1,0), "R": (1,0)}
ass = ["123", "456", "789"]

def main(args):
    nubs = [s.strip() for s in sys.stdin]

    x = 1
    y = 1

    for nub in nubs:
        for c in nub:
            x += DIRS[c][0]
            y += DIRS[c][1]
            if x < 0: x = 0
            if x > 2: x = 2
            if y < 0: y = 0
            if y > 2: y = 2
#            print(c, x,y, ass[y][x])
#        print(": ", ass[y][x])
        print(ass[y][x], end="")
    print()
if __name__ == '__main__':
    sys.exit(main(sys.argv))
