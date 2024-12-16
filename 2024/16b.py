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
# This is A* if you pass a heuristic and a target, otherwise Dijkstra's
# edges should return a sequence of (nbr, weight) pairs
def dijkstra(m, edges, start, heuristic=None, target=None, cap=None):
    cost = {start: 0}
    path = {}
    todo = [(0, 0, start)]
    explored = 0

    while todo and todo[0][-1][0] != target:
        _, k, cur = heapq.heappop(todo)
        if k != cost[cur]:
            continue
        explored += 1

        nbrs = list(edges(m, cur))
        # print('!', nbrs)
        for nbr, weight in nbrs:
            ncost = cost[cur] + weight
            if nbr not in cost or ncost < cost[nbr]:
                cost[nbr] = ncost
                path[nbr] = cur
                hcost = ncost if not heuristic else ncost + heuristic(nbr)
                heapq.heappush(todo, (hcost, ncost, nbr))

    return cost, path



def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    # data = [x.rstrip('\n').split('\n') for x in file.read().split('\n\n')]
    # data = [int(s.rstrip('\n')) for s in file]
    data = [s.rstrip('\n') for s in file]

    #### Read grid
    m = defaultdict(lambda: '.')
    for y, l in enumerate(data):
        for x, c in enumerate(l):
            if c == 'E':
                end = x, y
                c = '.'
            elif c == 'S':
                start = x, y
                c = '.'

            m[x,y] = c

    pos = start, RIGHT

    reverse = False

    def nbrs(m, cur):
        pos, dir = cur
        if dir is None:
            for a in VDIRS:
                yield (pos, a), 0
            return

        if pos == end:
            yield (pos, None), 0

        # print(pos, dir)
        d2 = dir
        if reverse:
            d2 = turn(turn(dir))
        x = vadd(pos, d2)
        if m[x] == '.':
            yield (x, dir), 1

        for d in 'left', 'right':
            yield (pos, turn(dir, d)), 1000


    c, _ = dijkstra(m, nbrs, pos)
    reverse = True
    cr, _ = dijkstra(m, nbrs, (end, None))

    best_score = c[end, None]

    on_path = set()
    for (pos, dir), score in c.items():
        if score + cr[pos, dir] == best_score:
            on_path.add(pos)

    print(on_path)

    # best_outs = {}
    # print(len(c))
    # for st2 in c:
    #     allcs[st2] = dijkstra(m, nbrs, st2)


    # for k, cs in allcs.items():
    #     best_outs[k] = min(c[x] for x in cs if x[0] == end)

    # print(best_outs[start])
    print(c[end, None])
    print(len(on_path))

if __name__ == '__main__':
    main(sys.argv)
