#!/usr/bin/env python3

import sys

DIRS = [(0,1), (1,0), (0,-1), (-1,0)]

def main(args):
    s = input()
    cmds = s.split(", ")

    d = 0
    x = 0
    y = 0

    for a in cmds:
        turn = a[0]
        amt = int(a[1:])
        if turn == 'R': d += 1
        else: d -= 1
        d %= 4
        x += amt * DIRS[d][0]
        y += amt * DIRS[d][1]

    print(abs(x)+abs(y))

if __name__ == '__main__':
    sys.exit(main(sys.argv))
