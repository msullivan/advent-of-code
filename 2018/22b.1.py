#!/usr/bin/env python3

# does A* basically (with some heap funniness). This lets us avoid the
# "x < 100" heuristic that was needed to get acceptable performance
# with Dijkstra's and the hinky BFS version.

from collections import defaultdict, deque
import sys
import re
import time
from functools import lru_cache
from dataclasses import dataclass, field
from heapq import heappop, heappush

@lru_cache(None)
def index(target, depth, x, y):
    if x == 0 and y == 0:
        return 0
    if (x, y) == target:
        return 0
    if y == 0:
        return x * 16807
    if x == 0:
        return y * 48271
    return erosion(target, depth, x-1, y) * erosion(target, depth, x, y-1)

@lru_cache(None)
def erosion(target, depth, x, y):
    return (index(target, depth, x, y) + depth) % 20183

def region(target, depth, x, y):
    return erosion(target, depth, x, y) % 3

ROCKY = 0
WET = 1
NARROW = 2

# Matches the region you can't go in!
NEITHER = 0
TORCH = 1
CLIMBING = 2

# could return self edges, whatever
def edges(target, depth, x, y, gear):
    options = []

    current = region(target, depth, x, y)
    for i in range(3):
        if i != gear and i != current:
            options += [((x, y, i), 7)]

    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        if x+dx >= 0 and y+dy >= 0 and region(target, depth, x+dx, y+dy) != gear:
            options += [((x+dx, y+dy, gear), 1)]

    return options


@dataclass(order=True)
class PrioritizedItem:
    priority: int
    item: object=field(compare=False)

def h(target, x, y, gear):
    return abs(target[0] - x) + abs(target[1] - y)


def go(depth, target):
    tx, ty = target

    start = (0, 0, TORCH)  # can't enter wet, because torch
    cost = {start: 0}
    sitem = PrioritizedItem(h(target, *start), start)

    todo = [sitem]
    items = {start: sitem}

    full_target = (*target, TORCH)

    while True:
        cur = heappop(todo).item
        if not cur:
            continue

        if cur == full_target:
            break
        for nbr, ncost in edges(target, depth, *cur):
            tentative_cost = cost[cur] + ncost
            if nbr not in cost or cost[nbr] > tentative_cost:
                item = PrioritizedItem(cost[cur] + h(target, *nbr), nbr)

                heappush(todo, item)
                cost[nbr] = tentative_cost
                if nbr in items:
                    items[nbr].item = None
                items[nbr] = item

    print(cost[cur])



def main(args):
    go(11739, (11, 718))
    #go(510, (10, 10))
if __name__ == '__main__':
    sys.exit(main(sys.argv))
