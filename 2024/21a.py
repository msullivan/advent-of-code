#!/usr/bin/env python3

import sys
from collections import defaultdict, Counter, deque
# from parse import parse
import re
import math
import itertools
import heapq
import functools

def extract(s):
    return [int(x) for x in re.findall(r'(-?\d+).?', s)]

def vadd(v1, v2):
    if len(v1) == 2:
        return v1[0] + v2[0], v1[1] + v2[1]
    elif len(v1) == 3:
        return v1[0] + v2[0], v1[1] + v2[1], v1[2] + v2[2]
    else:
        # ... this is so slow.
        return tuple([x + y for x, y in zip(v1, v2)])

def vsub(v1, v2):
    if len(v1) == 2:
        return v1[0] - v2[0], v1[1] - v2[1]


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
RDIRS = {v: k for k, v in DIRS.items()}
ALL_DIRS = [(x, y) for x in [-1,0,1] for y in [-1,0,1] if not x == y == 0]

def gnbrs(s, dirs=VDIRS):
    return [(dir, vadd(s, dir)) for dir in dirs]

def turn(v, d='left'):
    n = -1 if d == 'left' else 1
    return VDIRS[(VDIRS.index(v) + n) % len(VDIRS)]


##############################

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
                path[nbr] = [cur]
                hcost = ncost if not heuristic else ncost + heuristic(nbr)
                heapq.heappush(todo, (hcost, ncost, nbr))
            elif ncost == cost[nbr]:
                path[nbr].append(cur)

    return cost, path


NUM = "789\n456\n123\nX0A".split('\n')
DIR = "X^A\n<v>\n".split('\n')

def nbrs(m, p):
    for _, k in gnbrs(p):
        if m[k] != 'X':
            yield k, 1


def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    # data = [x.rstrip('\n').split('\n') for x in file.read().split('\n\n')]
    # data = [int(s.rstrip('\n')) for s in file]
    data = [s.rstrip('\n') for s in file]

    #### Read grid
    m_num = defaultdict(lambda: 'X')
    rnum = {}
    for y, l in enumerate(NUM):
        for x, c in enumerate(l):
            m_num[x,y] = c
            if c == 'A':
                num_a = x, y
            rnum[c] = x, y

    m_dir = defaultdict(lambda: 'X')
    rdir = {}
    for y, l in enumerate(DIR):
        for x, c in enumerate(l):
            m_dir[x,y] = c
            if c == 'A':
                dir_a = x, y
            rdir[c] = x, y

    num_costs = {start: dijkstra(m_num, nbrs, start) for start in list(m_num)}
    dir_costs = {start: dijkstra(m_dir, nbrs, start) for start in list(m_dir)}

    # def gets(m, src, tgt):
    #     mp = m[src][1]
    #     l = []
    #     while tgt != src:
    #         nxt = mp[tgt]
    #         dir = RDIRS[vsub(tgt, nxt)]
    #         l.append(dir)
    #         tgt = nxt

    #     l.reverse()
    #     return "".join(l)

    def gets(m, src, tgt):
        if tgt == src:
            return [""]
        mp = m[src][1]

        res = []
        nxts = mp[tgt]
        # print(tgt, nxts)
        for nxt in nxts:
            # print(tgt, nxt)
            dir = RDIRS[vsub(tgt, nxt)]
            fuck = gets(m, src, nxt)
            print(fuck)
            for r in fuck:
                res.append(r + dir)

        return res

    print(gets(num_costs, rnum['7'], rnum['6']))

    FUCKS = [(num_costs, rnum)] + [(dir_costs, rdir)]*2

    def go(i, csrc, ctgt):
        if i == 3:
            return ctgt
        cost, rm = FUCKS[i]
        src, tgt = rm[csrc], rm[ctgt]
        min_path = None
        for path in gets(cost, src, tgt):
            pos = 'A'
            spath = ""
            for c in path + 'A':
                spath += go(i+1, pos, c)
                pos = c
            if min_path is None or len(spath) < len(min_path):
                min_path = spath

        return min_path

    print(go(0, 'A', '7'))


    res = 0
    # data = [data[2]]
    for line in data:
        oline = line
        print('=', line)
        num = int(''.join(c for c in line if c.isnumeric()))

        pos = 'A'
        spath = ""
        for c in line:
            spath += go(0, pos, c)
            pos = c
        # if min_path is None or len(spath) < len(min_path):
        #     min_path = spath
        line = spath


        # for (costs, rm) in [(num_costs, rnum)] + [(dir_costs, rdir)]*2:
        #     print(line)
        #     pos = rm['A']
        #     nline = ""
        #     for c in line:
        #         tgt = rm[c]
        #         nline += gets(costs, pos, tgt) + "A"
        #         pos = tgt
        #     line = nline

        x =(len(line) * num)
        print(oline, len(line), num, len(line)*num)
        print(line)
        res += x

    print(res)

    # print(data)
    # print(num_costs)

if __name__ == '__main__':
    main(sys.argv)
