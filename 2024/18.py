#!/usr/bin/env python3

import sys
import re
import heapq

def extract(s):
    return [int(x) for x in re.findall(r'(-?\d+).?', s)]

def vadd(v1, v2):
    return v1[0] + v2[0], v1[1] + v2[1]

UP, RIGHT, DOWN, LEFT = VDIRS = (0, -1), (1, 0), (0, 1), (-1, 0),

def gnbrs(s, dirs=VDIRS):
    return [(dir, vadd(s, dir)) for dir in dirs]

# This is A* if you pass a heuristic and a target, otherwise Dijkstra's
# edges should return a sequence of (nbr, weight) pairs
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


def binary_search(pred, lo, hi=None):
    """Finds the first n in [lo, hi) such that pred(n) holds.

    hi == None -> infty
    """
    # assert not pred(lo)

    if hi is None:
        hi = max(lo, 1)
        while not pred(hi):
            hi *= 2

    # assert pred(hi)

    while lo < hi:
        mid = (lo + hi) // 2
        if pred(mid):
            hi = mid
        else:
            lo = mid + 1

    return lo


import time
def main(args):
    t0 = time.time()
    file = open(args[1]) if len(args) > 1 else sys.stdin
    data = [s.rstrip('\n') for s in file]
    data = [tuple(extract(l)) for l in data]

    N = 1024
    M = 70

    def nbrs(m, p):
        for _, n in gnbrs(p):
            if 0 <= n[0] <= M and 0 <= n[1] <= M and n not in m:
                yield n, 1

    start = 0, 0
    end = M, M

    ds, _ = dijkstra(set(data[:N]), nbrs, start)
    p1 = ds[end]

    def check(n):
        print('==', n)
        m = set(data[:n+1])
        ds, _ = dijkstra(m, nbrs, start)
        return end not in ds

    i = binary_search(check, N, len(data))
    print(i)
    x, y = data[i]

    print(f'{time.time() - t0:.3f}')
    print(p1)
    print(f'{x},{y}')


if __name__ == '__main__':
    main(sys.argv)
