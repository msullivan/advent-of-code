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

# def done(grid, rock):
#     for p in rock:
#         if p[1] <= 0:
#             return True
#     return False

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
    # data = [x.rstrip('\n').split('\n') for x in file.read().split('\n\n')]
    # data = [int(s.rstrip('\n')) for s in file]
    data = [s.rstrip('\n') for s in file][0]

    grid = defaultdict(lambda: '.')

    top = -1
    i = 0
    for rnum in range(2022):

        # if grid:
        #     draw(grid)
        # print(top)
        # print('=====', rnum)
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

        # print('STOP', rock)
        for p in rock:
            grid[p] = '#'
            top = max(top, p[1])

        print(rnum, top+1)


    print(top+1)

if __name__ == '__main__':
    main(sys.argv)
