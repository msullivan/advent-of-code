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


##############################

import heapq
import random
# This is A* if you pass a heuristic and a target, otherwise Dijkstra's
# edges should return a sequence of (nbr, weight) pairs
def dijkstra(m, edges, start, heuristic=None, target=None):
    cost = {start: 0}
    path = {}
    todo = [(0, 0, 0, start)]
    explored = 0

    while todo and todo[0][-1] != target:
        _, k, _, cur = heapq.heappop(todo)
        if k != cost[cur]:
            continue
        explored += 1

        nbrs = list(edges(m, cur))
        for nbr, weight in nbrs:
            ncost = cost[cur] + weight
            if nbr not in cost or ncost < cost[nbr]:
                cost[nbr] = ncost
                path[nbr] = cur
                hcost = ncost if not heuristic else ncost + heuristic(nbr)
                heapq.heappush(todo, (hcost, ncost, random.random(), nbr))

    return cost, path


def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    # data = [x.rstrip('\n').split('\n') for x in file.read().split('\n\n')]
    # data = [int(s.rstrip('\n')) for s in file]
    data = [s.rstrip('\n') for s in file]

    m = defaultdict(lambda: '!')

    for y, l in enumerate(data):
        for x, c in enumerate(l):
            if c == 'E':
                end = x, y
                c = '.'
            elif c == 'S':
                start = x, y
                c = '.'

            m[x,y] = c

    print(len(m))
    NO = set()

    possible_cheats = []
    for p, c in list(m.items()):
        if c == '.':
            for d, n in gnbrs(p):
                if m[n] == '#' and m[(n2 := vadd(n, d))] == '.':
                    possible_cheats.append((p, n2))

    print(len(possible_cheats))

    def nbrs(m, p):
        for d, n in gnbrs(p):
            if m[n] == '.':
                yield n, 1

    from_start, _ = dijkstra(m, nbrs, start)
    to_end, _ = dijkstra(m, nbrs, end)

    honest = from_start[end]
    print(honest)

    better = 0
    for cs, ce in possible_cheats:
        time = from_start[cs] + to_end[ce] + 2
        if time < honest:
            print((cs, ce), time, honest - time)
        if time + 100 <= honest:
            better += 1

    print(better)

    # def nbrs(m, p):
    #     if p == ():
    #         return
    #     xy, cheat = p

    #     if xy == end:
    #         yield (), 0
    #         return

    #     for d, n in gnbrs(xy):
    #         if m[n] == '.':
    #             yield (n, cheat), 1
    #         elif cheat is None and m[n] == '#' and m[(n2 := vadd(n, d))] == '.':
    #             nc = (xy, n2)
    #             if nc not in NO:
    #                 yield (n2, nc), 2


    # EX, EY = end
    # def heuristic(p):
    #     if p == ():
    #         return 0
    #     (x, y), _ = p
    #     return abs(x - EX) + abs(y - EY)


    # spos = (start, (True, True))

    # ms, _ = dijkstra(m, nbrs, spos, target=())
    # honest = ms[()]
    # print(honest)

    # better = 0
    # while True:
    #     cheat_spos = (start, None)
    #     ms, paths = dijkstra(m, nbrs, cheat_spos, target=(), heuristic=heuristic)
    #     cheat = ms[()]
    #     # if cheat > honest - 100:
    #     #     break
    #     better += 1
    #     print(cheat)
    #     _, cheatspot = paths[()]
    #     print(cheatspot, honest-cheat)
    #     NO.add(cheatspot)

    # print(better)


if __name__ == '__main__':
    main(sys.argv)
