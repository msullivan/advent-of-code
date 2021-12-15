#!/usr/bin/env python3

import sys

from collections import defaultdict, Counter, deque
from parse import parse
import re

def vadd(v1, v2):
    return tuple(x + y for x, y in zip(v1, v2))

UP, RIGHT, DOWN, LEFT = VDIRS = (0, -1), (1, 0), (0, 1), (-1, 0),

##############################

def edges(m, v):
    l = [vadd(v, e) for e in VDIRS]
    return [x for x in l if x in m]


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


def main(args):
    data = [s.strip() for s in sys.stdin]
    data = [[int(x) for x in l] for l in data]
    data = [repeat_l(l) for l in data]
    data = repeat_d(data)

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
            if nbr not in cost:
                todo.append(nbr)
                cost[nbr] = cost[cur] + m[nbr]

    print(cost[target])

if __name__ == '__main__':
    main(sys.argv)
