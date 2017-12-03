#!/usr/bin/env python3

import sys

def left(dx,dy):
    if (dx,dy) == (1,0):
        return (0,1)
    elif (dx,dy) == (0,1):
        return (-1,0)
    elif (dx,dy) == (-1,0):
        return (0,-1)
    else:
        return (1,0)

def main(args):
#    nubs = [s.strip() for s in sys.stdin]

    x = 0
    y = 0
    n = 1

    dx, dy = 1, 0
    # last = 0
    size = 0

#    num = int(args[1])
    num = 312051
#    num = 12
    while True:
        #print(n, x, y, size)
        if n == num: break
        if max(abs(x+dx), abs(y+dy)) > size:
            if x == size and y == -size:
                size += 1
            else:
                dx, dy = left(dx, dy)
        x += dx
        y += dy
        n += 1
    print(abs(x) + abs(y))


if __name__ == '__main__':
    sys.exit(main(sys.argv))
