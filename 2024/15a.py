import sys
from collections import defaultdict, Counter, deque
import re
import math
import itertools
import heapq

def extract(s):
    return [int(x) for x in re.findall(r'(-?\d+).?', s)]

def vadd(v1, v2):
    if len(v1) == 2:
        return v1[0] + v2[0], v1[1] + v2[1]
    elif len(v1) == 3:
        return v1[0] + v2[0], v1[1] + v2[1], v1[2] + v2[2]
    else:
        # ... this is so slow.
        return tuple([x + y for x, y in zip(v1, v2)])

UP, RIGHT, DOWN, LEFT = VDIRS = (0, -1), (1, 0), (0, 1), (-1, 0),
DIRS = {'^': UP, '>': RIGHT, 'v': DOWN, '<': LEFT }

def draw(painted):
    minx = min(x for x, y in painted)
    miny = min(y for x, y in painted)
    maxx = max(x for x, y in painted)
    maxy = max(y for x, y in painted)

    l = ""
    # XXX: add reversed if needed
    for y in list((range(miny, maxy+1))):
        for x in range(minx, maxx+1):
            l += painted.get((x,y), ".")
        l += "\n"
    print(l)


def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    data = [x.rstrip('\n').split('\n') for x in file.read().split('\n\n')]
    # data = [int(s.rstrip('\n')) for s in file]
    # data = [s.rstrip('\n') for s in file]

    #### Read grid
    m = defaultdict(lambda: '#')
    for y, l in enumerate(data[0]):
        for x, c in enumerate(l):
            m[x,y] = c
            if c == '@':
                robot = x,y
                m[x,y] = '.'

    for l in data[1]:
        for move in l:
            npos = vadd(robot, DIRS[move])
            npos2 = vadd(npos, DIRS[move])
            if m[npos] == '.':
                robot = npos
            elif m[npos] == 'O':
                x = npos
                while m[x] == 'O':
                    x = vadd(x, DIRS[move])
                if m[x] == '.':
                    m[x] = 'O'
                    m[npos] = '.'
                    robot = npos

            print(move)
            m[robot] = '@'
            draw(m)
            m[robot] = '.'


    draw(m)

    cksum = 0
    for (x, y), c in m.items():
        if c == 'O':
            cksum += 100*y + x
    print(cksum)

if __name__ == '__main__':
    main(sys.argv)
