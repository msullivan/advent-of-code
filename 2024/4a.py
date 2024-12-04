#!/usr/bin/env python3

import sys
from collections import defaultdict, Counter, deque


def vadd(v1, v2):
    return tuple([x + y for x, y in zip(v1, v2)])

ALL_DIRS = [(x, y) for x in [-1,0,1] for y in [-1,0,1] if not x == y == 0]

##############################

def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    data = [s.rstrip('\n') for s in file]

    m = defaultdict(lambda: '.')
    for y, l in enumerate(data):
        for x, c in enumerate(l):
            m[x, y] = c

    n = 0
    for y in range(len(data)):
        for x in range(len(data[0])):
            for dir in ALL_DIRS:
                v = [(x, y)]
                for i in range(3):
                    v.append(vadd(dir, v[-1]))
                s = ''.join(m[a] for a in v)
                if s == 'XMAS':
                    n += 1


    print(n)

if __name__ == '__main__':
    main(sys.argv)
