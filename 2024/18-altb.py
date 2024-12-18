#!/usr/bin/env python3

import sys
from collections import deque
import re
import heapq

def extract(s):
    return [int(x) for x in re.findall(r'(-?\d+).?', s)]

def vadd(v1, v2):
    return v1[0] + v2[0], v1[1] + v2[1]

UP, RIGHT, DOWN, LEFT = VDIRS = (0, -1), (1, 0), (0, 1), (-1, 0),

def gnbrs(s, dirs=VDIRS):
    return [(dir, vadd(s, dir)) for dir in dirs]


def bfs(m, edges, start, cost=None):
    if cost is None:
        cost = {}
    cost[start] = 0
    todo = deque([start])

    while todo:
        cur = todo.popleft()

        nbrs = list(edges(m, cur))
        for nbr in nbrs:
            if nbr not in cost:
                cost[nbr] = cost[cur] + 1
                todo.append(nbr)

    return cost


import time
def main(args):
    t0 = time.time()
    file = open(args[1]) if len(args) > 1 else sys.stdin
    data = [s.rstrip('\n') for s in file]
    data = [tuple(extract(l)) for l in data]

    M = 70

    def nbrs(m, p):
        for _, n in gnbrs(p):
            if 0 <= n[0] <= M and 0 <= n[1] <= M and n not in m:
                yield n

    start = 0, 0
    end = M, M

    ds = bfs(set(data[:1024]), nbrs, start)
    p1 = ds[end]

    m = set(data)
    ds = bfs(m, nbrs, start)

    for i, p in enumerate(reversed(data)):
        m.discard(p)
        # If any neighbor of the rock we are removing is already
        # visible from the start, do a BFS to extend what we've seen.
        if any(nbr in ds for _, nbr in gnbrs(p)):
            ds = bfs(m, nbrs, p, cost=ds)
            if end in ds:
                break

    assert end in ds
    x, y = p

    print(f'{time.time() - t0:.3f}')
    print(p1)
    print(f'{x},{y}')


if __name__ == '__main__':
    main(sys.argv)
