#!/usr/bin/env python3

import sys


def vadd(v1, v2, n=1):
    return tuple([x + n*y for x, y in zip(v1, v2)])

UP, RIGHT, DOWN, LEFT = VDIRS = (0, -1), (1, 0), (0, 1), (-1, 0),
DIRS = {'U': UP, 'R': RIGHT, 'D': DOWN, 'L': LEFT }
ALL_DIRS = [(x, y) for x in [-1,0,1] for y in [-1,0,1] if not x == y == 0]

# Lol: https://stackoverflow.com/questions/451426/how-do-i-calculate-the-area-of-a-2d-polygon
def area(p):
    return abs(sum(x0*y1 - x1*y0 for ((x0, y0), (x1, y1)) in segments(p))) // 2

def segments(p):
    return zip(p, p[1:] + [p[0]])

def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    data = [s.rstrip('\n') for s in file]

    pos = (0, 0)
    poses = [pos]
    perim = 0
    for line in data:
        d, n, x = line.split(' ')
        # n = int(n)
        n = int(x[2:-2], 16)
        d = 'RDLU'[int(x[-2])]

        npos = vadd(pos, DIRS[d], n)

        if d in 'RD':
            perim += n
        poses.append(npos)
        pos = npos

    print(int(area(poses)) + perim + 1)


if __name__ == '__main__':
    main(sys.argv)
