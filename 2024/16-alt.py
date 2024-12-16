#!/usr/bin/env python3

import sys
from collections import defaultdict, Counter, deque
import heapq

UP, RIGHT, DOWN, LEFT = VDIRS = (0, -1), (1, 0), (0, 1), (-1, 0),
DIRS = {'N': UP, 'E': RIGHT, 'S': DOWN, 'W': LEFT }

def vadd(v1, v2):
    return v1[0] + v2[0], v1[1] + v2[1]

def turn(v, d='left'):
    n = -1 if d == 'left' else 1
    return VDIRS[(VDIRS.index(v) + n) % len(VDIRS)]


def dijkstra_funny(m, edges, start, target=None, heuristic=None):
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
                path[nbr] = [cur]
                hcost = ncost if not heuristic else ncost + heuristic(nbr)
                heapq.heappush(todo, (hcost, ncost, nbr))
            elif ncost == cost[nbr]:
                path[nbr].append(cur)

    return cost, path


def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
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

    def nbrs(m, cur):
        pos, dir = cur
        if dir is None:
            return

        if pos == end:
            yield (pos, None), 0

        d2 = dir
        x = vadd(pos, d2)
        if m[x] == '.':
            yield (x, dir), 1

        for d in 'left', 'right':
            yield (pos, turn(dir, d)), 1000


    c, ps = dijkstra_funny(m, nbrs, pos)

    best_score = c[end, None]

    seen = set()
    def collect(nobe):
        if nobe in seen:
            return
        seen.add(nobe)
        if nobe in ps:
            for nbr in ps[nobe]:
                collect(nbr)
    collect((end, None))

    on_path = {pos for pos, _ in seen}

    print(c[end, None])
    print(len(on_path))

if __name__ == '__main__':
    main(sys.argv)
