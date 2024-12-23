#!/usr/bin/env python3

import sys
from collections import defaultdict, Counter, deque
# from parse import parse
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

def ichr(i):
    return chr(ord('a') + i)

def iord(c):
    return ord(c.lower()) - ord('a')

def optidx(d, opt=max, nth=0):
    if not isinstance(d, dict):
        d = dict(enumerate(d))
    rv = opt(d.values())
    return [i for i, v in d.items() if v == rv][nth], rv

LETTERS = "abcdefghijklmnopqrstuvwxyz"

UP, RIGHT, DOWN, LEFT = VDIRS = (0, -1), (1, 0), (0, 1), (-1, 0),
DIRS = {'N': UP, 'E': RIGHT, 'S': DOWN, 'W': LEFT }
ALL_DIRS = [(x, y) for x in [-1,0,1] for y in [-1,0,1] if not x == y == 0]

def gnbrs(s, dirs=VDIRS):
    return [(dir, vadd(s, dir)) for dir in dirs]

def turn(v, d='left'):
    n = -1 if d == 'left' else 1
    return VDIRS[(VDIRS.index(v) + n) % len(VDIRS)]



def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    # data = [x.rstrip('\n').split('\n') for x in file.read().split('\n\n')]
    # data = [int(s.rstrip('\n')) for s in file]
    data = [s.rstrip('\n') for s in file]

    m = defaultdict(set)

    for line in data:
        x, y = line.split('-')
        m[x].add(y)
        m[y].add(x)


    trips = set()
    for nobe in m:
        for nbr in m[nobe]:
            for nbr2 in m[nobe]:
                if nbr == nbr2:
                    continue
                if nbr2 in m[nbr]:
                    trips.add(frozenset([nobe, nbr, nbr2]))


    # cliques = trips
    # while len(cliques) > 1:
    #     print(len(list(cliques)[0]), len(cliques))
    #     ncliques = set()
    #     for c1 in cliques:
    #         for c2 in cliques:
    #             if c1 is c2:
    #                 continue
    #             inter = c1 & c2
    #             if len(inter) + 1 == len(c1):
    #                 # print(c1, c2, inter)
    #                 c1x = next(iter(c1 - c2))
    #                 c2x = next(iter(c2 - c1))
    #                 if c1x in m[c2x]:
    #                     ncliques.add(c1 | c2)

    #     cliques = ncliques

    cliques = trips
    while len(cliques) > 1:
        print(len(list(cliques)[0]), len(cliques))
        ncliques = set()
        for c1 in cliques:
            x = next(iter(c1))
            for n in m[x]:
                if n not in c1:
                    ns = m[n]
                    if all(c in ns for c in c1):
                        ncliques.add(c1 | {n})


            # for c2 in cliques:
            #     if c1 is c2:
            #         continue
            #     inter = c1 & c2
            #     if len(inter) + 1 == len(c1):
            #         # print(c1, c2, inter)
            #         c1x = next(iter(c1 - c2))
            #         c2x = next(iter(c2 - c1))
            #         if c1x in m[c2x]:
            #             ncliques.add(c1 | c2)

        cliques = ncliques


    # n = 0
    # for x, y, z in trips:
    #     if any(t[0] == 't' for t in (x, y, z)):
    #         n += 1


    # seen = set()
    # biggest = set()
    # for nobe in m:
    #     ds, _ = dijkstra(m, nbrs, nobe)
    #     if len(ds) > len(biggest):
    #         biggest = ds

    x = ','.join(sorted(list(cliques)[0]))
    print(x)

    # print(len(trips))
    # print(n)

if __name__ == '__main__':
    main(sys.argv)
