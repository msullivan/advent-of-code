#!/usr/bin/env python3

import sys
from collections import defaultdict, Counter, deque

def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    # data = [x.rstrip('\n').split('\n') for x in file.read().split('\n\n')]
    # data = [int(s.rstrip('\n')) for s in file]
    data = [s.rstrip('\n') for s in file]

    m = defaultdict(lambda: '.')
    for y, l in enumerate(data):
        for x, c in enumerate(l):
            m[x, y] = c

    n = 0

    for y in range(len(data)):
        for x in range(len(data[0])):
            if (
                m[x,y] == 'A'
                and (
                    (m[x-1,y-1] == 'M' and m[x+1,y+1] == 'S')
                    or (m[x-1,y-1] == 'S' and m[x+1,y+1] == 'M')
                )
                and (
                    (m[x-1,y+1] == 'M' and m[x+1,y-1] == 'S')
                    or (m[x-1,y+1] == 'S' and m[x+1,y-1] == 'M')
                )
            ):
                n += 1

    print(n)

if __name__ == '__main__':
    main(sys.argv)
