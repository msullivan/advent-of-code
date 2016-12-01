#!/usr/bin/env python3

import sys

DIRS = [(0,1), (1,0), (0,-1), (-1,0)]

def main(args):
    s = input()
    cmds = s.split(", ")
    visited = set()
    visited.add((0,0))

    d = 0
    x = 0
    y = 0

    for a in cmds:
        turn = a[0]
        amt = int(a[1:])
        if turn == 'R': d += 1
        else: d -= 1
        d %= 4

        for i in range(amt):
            x += DIRS[d][0]
            y += DIRS[d][1]
#            print((x,y))
            if (x,y) in visited:
                print(abs(x)+abs(y))
                return
            visited.add((x,y))

if __name__ == '__main__':
    sys.exit(main(sys.argv))
