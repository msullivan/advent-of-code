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

ROCKS2 = []
for r in ROCKS:
    sqs = []
    for y, l in enumerate(reversed(r)):
        for x, c in enumerate(l):
            if c == '#':
                sqs.append((x, y))
    ROCKS2.append(tuple(sqs))

ROCKS = ROCKS2

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

    top = -1
    i = 0
    stopat = -1
    rnum = 0
    while True:
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


        # print(rnum, top+1)
        # Part 1!
        if rnum == 2022 - 1:
            print(top+1)

        # Part 2

        # Take a snapshot of the top 50 rows and use it to look for repeats.
        # I think this isn't technically sound, and you really ought to also
        # make sure there is no path from top to bottom, or something.
        snapshot = "\n".join([
            "".join(grid[c, r] for c in range(7))
            for r in range(top, top-50, -1)
        ])
        # If we've seen a repeat for the first time, compute a bunch of info
        # about the loop, then run a bit more to figure out the remainder.
        if rnum > 2022 and (snapshot, i % len(data)) in seen and stopat == -1:
            last, lastheight = seen[(snapshot, i % len(data))]
            startheight = top+1
            togo = (1000000000000-1)-rnum
            looplen = rnum - last
            loops = togo // looplen
            remainder = togo % looplen
            loopsize = startheight - lastheight

            stopat = rnum + remainder

        if rnum == stopat:
            answer = top+1 + loops*loopsize
            print(answer)
            break

        seen[snapshot, i % len(data)] = (rnum, top+1)

        rnum += 1


if __name__ == '__main__':
    main(sys.argv)
