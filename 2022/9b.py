#!/usr/bin/env python3

import sys

def vadd(v1, v2):
    return tuple(x + y for x, y in zip(v1, v2))

UP, RIGHT, DOWN, LEFT = VDIRS = (0, -1), (1, 0), (0, 1), (-1, 0),
DIRS = {'U': UP, 'R': RIGHT, 'D': DOWN, 'L': LEFT }

def sign(n):
    return -1 if n < 0 else 1 if n > 0 else 0

def move(head, tail):
    hx, hy = head
    tx, ty = tail

    dist = abs(hy-ty) + abs(hx-tx)
    if (dist == 2 and (hx == tx or hy == ty)) or dist > 2:
        mx = sign(hx-tx)
        my = sign(hy-ty)
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
