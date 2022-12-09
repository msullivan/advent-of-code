#!/usr/bin/env python3

import sys

def vadd(v1, v2):
    return tuple(x + y for x, y in zip(v1, v2))

UP, RIGHT, DOWN, LEFT = VDIRS = (0, -1), (1, 0), (0, 1), (-1, 0),
DIRS = {'U': UP, 'R': RIGHT, 'D': DOWN, 'L': LEFT }

def move(nhead, tail):
    hx, hy = nhead
    tx, ty = tail
    # I started by cases... and then decided to be general? idk
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

    return tail

def main(args):
    data = [s.rstrip('\n') for s in sys.stdin]

    p1spots = set()
    p2spots = set()

    spots = [(0, 0) for _ in range(10)]
    head = tail = (0, 0)
    for x in data:
        d, n = x.split(' ')
        d = DIRS[d]
        n = int(n)
        for _ in range(n):
            nhead = vadd(spots[0], d)
            nspots = [nhead]
            for sp in spots[1:]:
                nhead = move(nhead, sp)
                nspots.append(nhead)
            spots = nspots
            p1spots.add(spots[1])
            p2spots.add(spots[-1])


    print(len(p1spots))
    print(len(p2spots))

if __name__ == '__main__':
    main(sys.argv)
