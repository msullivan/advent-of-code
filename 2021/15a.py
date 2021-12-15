#!/usr/bin/env python3

import sys

from collections import defaultdict, Counter, deque

def vadd(v1, v2):
    return tuple(x + y for x, y in zip(v1, v2))

UP, RIGHT, DOWN, LEFT = VDIRS = (0, -1), (1, 0), (0, 1), (-1, 0),


def edges(m, v):
    l = [vadd(v, e) for e in VDIRS]
    return [x for x in l if x in m]

def main(args):
    data = [s.strip() for s in sys.stdin]
    data = [[int(x) for x in l] for l in data]

    m = {(i, j): v for i, l in enumerate(data) for j, v in enumerate(l)}

    start = (0, 0)
    cost = {start: 0}
    todo = deque([start])
    cost[start] = 0
    target = (len(data[0])-1, len(data)-1)

    while todo:
        # really this should be a PQ but oh well...
        cur = min(todo, key=lambda x: cost[x])
        todo.remove(cur)
        for nbr in edges(m, cur):
            ncost = cost[cur] + m[nbr]
            if nbr not in cost or cost[nbr] > ncost:
                todo.append(nbr)
                cost[nbr] = ncost

    print(cost[target])

if __name__ == '__main__':
    main(sys.argv)
