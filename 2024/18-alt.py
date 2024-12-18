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


def color_bfs(m, edges, start, cost=None, color=None):
    if cost is None:
        cost = {}
    cost[start] = (0, color)
    todo = deque([start])
    colors = set()

    while todo:
        cur = todo.popleft()

        nbrs = list(edges(m, cur))
        for nbr in nbrs:
            if nbr not in cost:
                cost[nbr] = cost[cur][0] + 1, color
                todo.append(nbr)
            else:
                colors.add(cost[nbr][1])

    return cost, colors


# union-find??
def uf_create(uf, k):
    assert k not in uf, k
    uf[k] = k
    return k


def uf_find(uf, k):
    k2 = uf[k]
    if k2 == k:
        return k
    else:
        k3 = uf_find(uf, k2)
        uf[k] = k3
        return k3


def uf_union(uf, k1, k2):
    k1 = uf_find(uf, k1)
    uf[k1] = uf_find(uf, k2)
    return k1



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

    ds, _ = color_bfs(set(data[:1024]), nbrs, start)
    p1, _ = ds[end]

    uf = {}
    START_COLOR = -1
    END_COLOR = -2
    m = set(data)
    ds = {}
    # Paint the areas reachable from the start and the end with
    # START_COLOR and END_COLOR.
    ds, colors = color_bfs(m, nbrs, start, cost=ds, color=START_COLOR)
    ds, colors = color_bfs(m, nbrs, end, cost=ds, color=END_COLOR)
    assert START_COLOR not in colors

    uf_create(uf, START_COLOR)
    uf_create(uf, END_COLOR)
    for i, p in enumerate(reversed(data)):
        # Remove a rock and then paint every unpainted square reachable from that
        # rock with the color `i`
        m.discard(p)
        ds, colors = color_bfs(m, nbrs, p, cost=ds, color=i)
        # Union every color that was seen on the frontier with `i`
        uf_create(uf, i)
        for color in colors:
            uf_union(uf, i, color)

        # If START_COLOR and END_COLOR are unioned now, then this rock made it work
        if uf_find(uf, START_COLOR) == uf_find(uf, END_COLOR):
            break
    else:
        print(uf)
        raise AssertionError('path never worked')

    x, y = p

    print(f'{time.time() - t0:.3f}')
    print(p1)
    print(f'{x},{y}')


if __name__ == '__main__':
    main(sys.argv)
