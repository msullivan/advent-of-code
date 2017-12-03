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
    x = 0
    y = 0
    n = 1

    dx, dy = 1, 0
    # last = 0
    size = 0

    num = 312051


    vals = {(0,0): 1}
    while True:
        #print(n, x, y, size)
        if max(abs(x+dx), abs(y+dy)) > size:
            if x == size and y == -size:
                size += 1
            else:
                dx, dy = left(dx, dy)
        x += dx
        y += dy
        n += 1

        val = 0
        for ix in [-1,0,1]:
            for iy in [-1,0,1]:
                if ix == 0 and iy == 0: continue
                val += vals.get((x+ix, y+iy), 0)
        vals[(x,y)] = val

        if val >= num: break
    print(val)


if __name__ == '__main__':
    sys.exit(main(sys.argv))
