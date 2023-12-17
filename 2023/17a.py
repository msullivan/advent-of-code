#!/usr/bin/env python3

import sys
from collections import defaultdict, Counter, deque

def vadd(v1, v2):
    return tuple([x + y for x, y in zip(v1, v2)])

UP, RIGHT, DOWN, LEFT = VDIRS = (0, -1), (1, 0), (0, 1), (-1, 0),

def turn(v, d='left'):
    n = -1 if d == 'left' else 1
    return VDIRS[(VDIRS.index(v) + n + len(VDIRS))%len(VDIRS)]

import heapq
# This is A* if you pass a heuristic and a target, otherwise Dijkstra's
def dijkstra(m, edges, start, heuristic=None, target=None):
    cost = {start: 0}
    path = {}
    todo = [(0, 0, start)]
    explored = 0

    while todo and todo[0][-1] != target:
        _, k, cur = heapq.heappop(todo)
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
                heapq.heappush(todo, (hcost, ncost, nbr))

    return cost, path


def edges(m, st):
    p, dir, cnt = st
    ops = []
    if cnt < 2 and (nxt := vadd(p, dir)) in m:
        ops.append(((nxt, dir, cnt + 1), m[nxt]))

    ldir = turn(dir)
    if (nxt := vadd(p, ldir)) in m:
        ops.append(((nxt, ldir, 0), m[nxt]))

    ldir = turn(dir, 'right')
    if (nxt := vadd(p, ldir)) in m:
        ops.append(((nxt, ldir, 0), m[nxt]))

    return ops



def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    # data = [x.rstrip('\n').split('\n') for x in file.read().split('\n\n')]
    # data = [int(s.rstrip('\n')) for s in file]
    data = [s.rstrip('\n') for s in file]

    m = {}
    for y, l in enumerate(data):
        for x, c in enumerate(l):
            m[x, y] = int(c)

    asdf = []

    ## BOTH
    st = ((0, 0), RIGHT, 0)
    res, _ = dijkstra(m, edges, st)

    for (k, _, _), v in res.items():
        if k == (len(data[0])-1, len(data)-1):
            asdf.append(v)
            print(k, v)

    st = ((0, 0), DOWN, 0)
    res, _ = dijkstra(m, edges, st)

    for (k, _, _), v in res.items():
        if k == (len(data[0])-1, len(data)-1):
            asdf.append(v)
            print(k, v)

    print(min(asdf))

if __name__ == '__main__':
    main(sys.argv)
