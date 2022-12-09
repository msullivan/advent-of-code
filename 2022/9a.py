#!/usr/bin/env python3

import sys

def vadd(v1, v2):
    return tuple(x + y for x, y in zip(v1, v2))

UP, RIGHT, DOWN, LEFT = VDIRS = (0, -1), (1, 0), (0, 1), (-1, 0),
DIRS = {'U': UP, 'R': RIGHT, 'D': DOWN, 'L': LEFT }

def move(head, tail, dir):
    nhead = vadd(head, dir)
    hx, hy = nhead
    tx, ty = tail
    if hx == tx and hy + 2 == ty:
        tail = (hx, hy+1)
    elif hx == tx and hy - 2 == ty:
        tail = (hx, hy-1)
    elif hy == ty and hx - 2 == tx:
        tail = (hx-1, hy)
    elif hy == ty and hx + 2 == tx:
        tail = (hx+1, hy)
    elif abs(hy-ty) + abs(hx-tx) > 2:
        mx = (hx-tx)//abs(hx-tx)
        my = (hy-ty)//abs(hy-ty)
        tail = vadd(tail, (mx, my))

    return nhead, tail

def main(args):
    data = [s.rstrip('\n') for s in sys.stdin]

    spots = set()
    head = tail = (0, 0)
    for x in data:
        d, n = x.split(' ')
        d = DIRS[d]
        n = int(n)
        for _ in range(n):
            head, tail = move(head, tail, d)
            spots.add(tail)

    print(len(spots))

if __name__ == '__main__':
    main(sys.argv)
