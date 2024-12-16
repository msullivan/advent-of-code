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

    reverse = False

    def nbrs(m, cur):
        pos, dir = cur
        if dir is None:
            for a in VDIRS:
                yield (pos, a), 0
            return

        if pos == end:
            yield (pos, None), 0

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

    print(c[end, None])
    print(len(on_path))

if __name__ == '__main__':
    main(sys.argv)
