#!/usr/bin/env python3

import sys

from collections import defaultdict, Counter, deque
from parse import parse
import re
import heapq


def vadd(v1, v2):
    return tuple(x + y for x, y in zip(v1, v2))

UP, RIGHT, DOWN, LEFT = VDIRS = (0, -1), (1, 0), (0, 1), (-1, 0),


##############################


def wrap(i):
    if i >= 10:
        return wrap(i - 9)
    return i


def repeat_l(l):
    o = []
    for i in range(5):
        o.extend([wrap(x+i) for x in l])
    return o

def repeat_d(ls):
    o = []
    for i in range(5):
        for l in ls:
            o.append([wrap(x+i) for x in l])
    return o


def edges(m, v):
    l = [vadd(v, e) for e in VDIRS]
    return [x for x in l if x in m]


def weight(m, u, v):
    return m[v]


def dijkstra(m, edges, weight, start, target=None):
    cost = {start: 0}
    path = {}
    todo = [(0, start)]

    while todo and todo[0][-1] != target:
        k, cur = heapq.heappop(todo)
        if k != cost[cur]:
            continue

        for nbr in edges(m, cur):
            ncost = cost[cur] + weight(m, cur, nbr)
            if nbr not in cost or ncost < cost[nbr]:
                cost[nbr] = ncost
                path[nbr] = cur
                heapq.heappush(todo, (ncost, nbr))

    return cost, path


def main(args):
    data = [s.strip() for s in sys.stdin]
    data = [[int(x) for x in l] for l in data]
    data = [repeat_l(l) for l in data]
    data = repeat_d(data)

    m = {(i, j): v for i, l in enumerate(data) for j, v in enumerate(l)}

    start = (0, 0)
    target = (len(data[0])-1, len(data)-1)
    cost, _ = dijkstra(m, edges, weight, start, target)

    print(cost[target])

if __name__ == '__main__':
    main(sys.argv)
