#!/usr/bin/env python3

import sys
from collections import defaultdict
import heapq
import functools

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


UP, RIGHT, DOWN, LEFT = VDIRS = (0, -1), (1, 0), (0, 1), (-1, 0),
DIRS = {'^': UP, '>': RIGHT, 'v': DOWN, '<': LEFT }
RDIRS = {v: k for k, v in DIRS.items()}

def gnbrs(s, dirs=VDIRS):
    return [(dir, vadd(s, dir)) for dir in dirs]


# This is super overkill
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
    data = [s.rstrip('\n') for s in file]

    #### Read grid
    m_num = defaultdict(lambda: 'X')
    rnum = {}
    for y, l in enumerate(NUM):
        for x, c in enumerate(l):
            m_num[x,y] = c
            rnum[c] = x, y

    m_dir = defaultdict(lambda: 'X')
    rdir = {}
    for y, l in enumerate(DIR):
        for x, c in enumerate(l):
            m_dir[x,y] = c
            rdir[c] = x, y

    num_costs = {start: dijkstra(m_num, nbrs, start) for start in list(m_num)}
    dir_costs = {start: dijkstra(m_dir, nbrs, start) for start in list(m_dir)}

    def gets(m, src, tgt):
        if tgt == src:
            return [""]
        _, mp = m[src]

        res = []
        nxts = mp[tgt]
        for nxt in nxts:
            dir = RDIRS[vsub(tgt, nxt)]
            for r in gets(m, src, nxt):
                res.append(r + dir)

        return res

    MAPS = [(num_costs, rnum)] + [(dir_costs, rdir)] * 25

    @functools.cache
    def go(csrc, ctgt, i):
        if i == len(MAPS):
            return 1
        cost, rm = MAPS[i]
        src, tgt = rm[csrc], rm[ctgt]
        min_path = float('inf')
        for path in gets(cost, src, tgt):
            spath = go_str(path + 'A', i+1)
            min_path = min(spath, min_path)

        return min_path

    def go_str(path, i):
        pos = 'A'
        spath = 0
        for c in path:
            spath += go(pos, c, i)
            pos = c
        return spath

    res = 0
    for line in data:
        oline = line
        print('=', line)
        num = int(''.join(c for c in line if c.isnumeric()))

        spath = go_str(line, 0)
        res += spath * num

    print(res)


if __name__ == '__main__':
    main(sys.argv)
