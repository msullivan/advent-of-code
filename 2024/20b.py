#!/usr/bin/env python3

import sys
from collections import defaultdict
import heapq


def vadd(v1, v2):
    if len(v1) == 2:
        return v1[0] + v2[0], v1[1] + v2[1]
    elif len(v1) == 3:
        return v1[0] + v2[0], v1[1] + v2[1], v1[2] + v2[2]
    else:
        # ... this is so slow.
        return tuple([x + y for x, y in zip(v1, v2)])

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


def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
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

    def nbrs(m, p):
        for d, n in gnbrs(p):
            if m[n] == '.':
                yield n, 1

    from_start, _ = dijkstra(m, nbrs, start)
    to_end, _ = dijkstra(m, nbrs, end)

    honest = from_start[end]

    p1 = p2 = 0
    opens = [p for p, c in m.items() if c == '.']
    for i, cs in enumerate(opens):
        for ce in opens:
            (x1, y1), (x2, y2) = cs, ce
            dist = abs(x1 - x2) + abs(y1 - y2)
            if dist <= 20:
                time = from_start[cs] + to_end[ce] + dist
                if time + 100 <= honest:
                    p2 += 1
                    if dist <= 2:
                        p1 += 1
    print(p1)
    print(p2)


if __name__ == '__main__':
    main(sys.argv)
