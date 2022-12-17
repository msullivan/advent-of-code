#!/usr/bin/env python3

import sys
from collections import defaultdict

def vadd(v1, v2):
    return tuple(x + y for x, y in zip(v1, v2))

UP, RIGHT, DOWN, LEFT = VDIRS = (0, 1), (1, 0), (0, -1), (-1, 0),

ROCKS = '''\
####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##
'''


ROCKS = [r.split('\n') for r in ROCKS.strip().split('\n\n')]
print(ROCKS)

ROCKS2 = []
for r in ROCKS:
    sqs = []
    for y, l in enumerate(reversed(r)):
        for x, c in enumerate(l):
            if c == '#':
                sqs.append((x, y))
    ROCKS2.append(tuple(sqs))

OROCKS = ROCKS
ROCKS = ROCKS2
print(ROCKS)

def out(grid, rock):
    for p in rock:
        if grid[p] == '#':
            return True
        if p[1] < 0:
            return True
        if p[0] < 0:
            return True
        if p[0] >= 7:
            return True
    return False


def draw(painted):
    minx = 0
    miny = 0
    maxx = 6
    maxy = max(y for x, y in painted)

    l = ""
    for y in (list(reversed(range(miny, maxy+1)))):
        for x in range(minx, maxx+1):
            l += painted.get((x,y), ".")
        l += "\n"
    print(l)


def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    data = [s.rstrip('\n') for s in file][0]

    grid = defaultdict(lambda: '.')

    seen = {}

    scores = {}
    top = -1
    no = 0
    i = 0
    stopat = -1
    # for rnum in range(2022):
    for rnum in range(100000):
        rock = ROCKS[rnum % len(ROCKS)]

        origin = (2, top + 4)

        rock = [vadd(p, origin) for p in rock]
        while True:
            d = RIGHT if data[(i)%len(data)] == '>' else LEFT
            i = (i + 1)

            nrock = [vadd(p, d) for p in rock]
            if not out(grid, nrock):
                rock = nrock

            nrock = [vadd(p, DOWN) for p in rock]
            if out(grid, nrock):
                break
            rock = nrock

        for p in rock:
            grid[p] = '#'
            top = max(top, p[1])

        if rnum < 100:
            continue

        snapshot = "\n".join([
            "".join(grid[c, r] for c in range(7))
            for r in range(top, top-1000, -1)
        ])
        # print(list(range(top, top-10, -1)))
        print(snapshot)
        # print(grid)
        if (snapshot, i % len(data)) in seen and not no:
            last, lastheight = seen[(snapshot, i % len(data))]
            startheight = top+1
            togo = (1000000000000-1)-rnum
            looplen = rnum - last
            loops = togo // looplen
            remainder = togo % looplen
            loopsize = startheight - lastheight

            no = 1
            stopat = rnum + remainder

        if rnum == stopat:
            growth = top+1 - startheight
            answer = top+1 + loops*loopsize
            print(answer)
            break

        seen[snapshot, i % len(data)] = (rnum, top+1)

        scores[rnum] = top + 1
        print(rnum, top+1)


if __name__ == '__main__':
    main(sys.argv)
