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


def bfs(m, edges, start, color=None):
    cost = {start: (0, color)}
    todo = deque([start])

    while todo:
        cur = todo.popleft()

        nbrs = list(edges(m, cur))
        for nbr in nbrs:
            if nbr not in cost:
                cost[nbr] = cost[cur][0] + 1, color
                todo.append(nbr)

    return cost


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


def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    data = [s.rstrip('\n') for s in file]
    data = [tuple(extract(l)) for l in data]

    M = 70

    def nbrs(m, p):
        for _, n in gnbrs(p):
            if 0 <= n[0] <= M and 0 <= n[1] <= M and n not in m:
                yield n

    start = 0, 0

    ds = bfs(set(data[:1024]), nbrs, start)
    p1 = ds[M, M]

    def check(n):
        print('==', n)
        m = set(data[:n+1])
        ds = bfs(m, nbrs, start)
        return (M, M) not in ds

    i = binary_search(check, 0, len(data))
    print(i)
    x, y = data[i]

    print(p1)
    print(f'{x},{y}')


if __name__ == '__main__':
    main(sys.argv)
