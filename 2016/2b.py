#!/usr/bin/env python3

import sys

DIRS = {"U": (0,-1), "D": (0,1), "L": (-1,0), "R": (1,0)}
ass = [
    "  1  ",
    " 234 ",
    "56789",
    " ABC ",
    "  D  "]

def main(args):
    nubs = [s.strip() for s in sys.stdin]

    x = 0
    y = 2
#    print(ass[y][x])
    for nub in nubs:
        for c in nub:
            old = x,y
            x += DIRS[c][0]
            y += DIRS[c][1]
            try:
                if ass[y][x] == " ": raise 5
                if x < 0 or y < 0: raise 2
            except:
                x, y = old
#            print(c, x,y, ass[y][x])
#        print(": ", ass[y][x])
        print(ass[y][x], end="")
    print()
if __name__ == '__main__':
    sys.exit(main(sys.argv))
