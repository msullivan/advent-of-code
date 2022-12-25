#!/usr/bin/env python3

import sys
from collections import defaultdict, Counter, deque
from parse import parse
import re
import math
import functools

def extract(s):
    return [int(x) for x in re.findall(r'(-?\d+).?', s)]

def vadd(v1, v2):
    return tuple([x + y for x, y in zip(v1, v2)])

def ichr(i):
    return chr(ord('a') + i)

def iord(c):
    return ord(c.lower()) - ord('a')

def optidx(d, opt=max, nth=0):
    if not isinstance(d, dict):
        d = dict(enumerate(d))
    rv = opt(d.values())
    return [i for i, v in d.items() if v == rv][nth], rv

LETTERS = "abcdefghijklmnopqrstuvwxyz"

UP, RIGHT, DOWN, LEFT = VDIRS = (0, -1), (1, 0), (0, 1), (-1, 0),
DIRS = {'N': UP, 'E': RIGHT, 'S': DOWN, 'W': LEFT }
DIRS = {'^': UP, '>': RIGHT, 'v': DOWN, '<': LEFT }
ALL_DIRS = [(x, y) for x in [-1,0,1] for y in [-1,0,1] if not x == y == 0]

def turn(v, d='left'):
    n = -1 if d == 'left' else 1
    return VDIRS[(VDIRS.index(v) + n + len(VDIRS))%len(VDIRS)]


##############################

import heapq
# This is A* if you pass a heuristic and a target, otherwise Dijkstra's
def dijkstra(m, edges, start, heuristic=None, target=None):
    cost = {start: 0}
    path = {}
    todo = [(0, 0, start)]
    explored = 0

    while todo and todo[0][-1][0] != target:
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
    # data = [x.rstrip('\n').split('\n') for x in file.read().split('\n\n')]
    # data = [int(s.rstrip('\n')) for s in file]
    data = [s.rstrip('\n') for s in file]
    # print('AAA', data)

    MY = len(data)
    MX = len(data[0])
    start = (1, 0)
    end = (MX-2, MY-1)

    @functools.cache
    def bliz_step(blizzards):
        nbliz = set()
        # print(blizzards)
        for pos, dir in blizzards:
            npos = list(vadd(pos, dir))
            if npos[0] == 0:
                npos[0] = MX-2
            elif npos[0] == MX-1:
                npos[0] = 1
            elif npos[1] == 0:
                npos[1] = MY-2
            elif npos[1] == MY-1:
                npos[1] = 1
            nbliz.add((tuple(npos), dir))

        fbliz = frozenset(nbliz)
        bposes = {x for x, _ in nbliz}

        return fbliz, bposes


    def edges(stuff, cur):
        me, blizzards = cur
        fbliz, bposes = bliz_step(blizzards)

        outs = []
        for dir in VDIRS + ((0, 0),):
            new = vadd(dir, me)
            # if (0 < new[0] < MX-1 and 0 < new[1] < MY-1) or new in (start, end):
            # print('?', data[me[1]][me[0]])
            # print(me, new, end)
            if new[1] >= 0 and new[1] < MY and data[new[1]][new[0]] != '#':
                if new not in bposes:
                    outs.append(((new, fbliz), 1))

        return outs

    stuff = set()
    for y, line in enumerate(data):
        for x, c in enumerate(line):
            if c in DIRS:
                stuff.add(((x, y), DIRS[c]))


    cost, path = dijkstra(None, edges, (start, frozenset(stuff)), target=end)
    c1, state = [(v, st) for st, v in cost.items() if st[0] == end][0]

    cost, path = dijkstra(None, edges, state, target=start)
    c2, state = [(v, st) for st, v in cost.items() if st[0] == start][0]

    cost, path = dijkstra(None, edges, state, target=end)
    c3, state = [(v, st) for st, v in cost.items() if st[0] == end][0]

    print(c1, c2, c3)
    print(c1 + c2 + c3)

if __name__ == '__main__':
    main(sys.argv)
