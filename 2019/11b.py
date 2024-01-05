#!/usr/bin/env python3

import sys
from collections import defaultdict
from intcode import IntCode

DIRS = [(0, -1), (1, 0), (0, 1), (-1, 0)]

def main(args):
    data = [s.strip() for s in sys.stdin]
    p = [int(x) for x in data[0].split(",")]
    colors = defaultdict(int)
    colors[0,0] = 1
    painted = set()


    interp = IntCode(p)

    pos = (0, 0)
    dir = 0
    while not interp.done:
        ic = colors[pos]

        color, direction = interp.run([colors[pos]])
        print(color, direction)
        colors[pos] = color
        painted.add(pos)
        if direction == 0:
            dir = (dir - 1) % 4
        else:
            dir = (dir + 1) % 4
        pos = (pos[0] + DIRS[dir][0], pos[1] + DIRS[dir][1])

    print(len(painted))

    minx = min(x for x, y in painted)
    miny = min(y for x, y in painted)
    maxx = max(x for x, y in painted)
    maxy = max(y for x, y in painted)
    for y in range(miny, maxy+1):
        l = ""
        for x in range(minx, maxx+1):
            l += " #"[colors[x,y]]
        print(l)


if __name__ == '__main__':
    sys.exit(main(sys.argv))
