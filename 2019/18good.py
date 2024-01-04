#!/usr/bin/env python3

from collections import deque
import heapq
import sys

DIRS = [(0, -1), (1, 0), (0, 1), (-1, 0)]


def add(v1, v2):
    return (v1[0] + v2[0], v1[1] + v2[1])

# Trace out (via BFS) every direct source|key->key path, along with
# whatever doors and keys they pass. This is used to determine edges
# for a pass of Dijkstra's.
def trace(board, sources):
    sources = list(sources)
    sources += [k for k, v in board.items() if v.islower()]

    routes = {}

    for source in sources:
        routes[board[source]] = set()

        q = deque([(0, frozenset(), source)])
        seen = {source}

        while q:
            steps, doors, pos = q.popleft()
            # print(steps, pos, keys)

            for dir in DIRS:
                nextpos = add(pos, dir)
                tp = board[nextpos]
                if tp == '#':
                    continue
                if nextpos in seen:
                    continue
                seen.add(nextpos)

                ndoors = doors
                if tp.islower():
                    routes[board[source]].add((board[nextpos], steps+1, doors))
                    # Treat a key like a door: you can't pass a key without
                    # picking it up. (This is a *big* optimization.)
                    ndoors = doors | {tp}

                if tp.isupper():
                    ndoors = doors | {tp.lower()}

                q.append((steps+1, ndoors, nextpos))

    return routes


def dijkstra(edges, start, target=None):
    cost = {start: 0}
    todo = [(0, start)]
    explored = 0
    relaxed = 0

    max_size = 0
    while todo and todo[0][-1][-1] != target:
        max_size = max(max_size, len(todo))
        k, cur = heapq.heappop(todo)
        if k != cost[cur]:
            relaxed += 1
            continue
        explored += 1

        nbrs = edges(cur)
        for nbr, weight in nbrs:
            ncost = cost[cur] + weight
            if nbr not in cost or ncost < cost[nbr]:
                cost[nbr] = ncost
                heapq.heappush(todo, (ncost, nbr))

    print(f'{explored=}, {relaxed=}, {len(todo)=}, {max_size=}')

    last = None
    if todo:
        last = todo[0][-1]

    return cost, last


def go(m, part1):
    board = {}
    for y in range(len(m)):
        for x in range(len(m[y])):
            board[x,y] = m[y][x]

    source = next(k for k, v in board.items() if v == "@")
    allkeys = {v for v in board.values() if v.islower()}

    if not part1 and len(tuple(k for k, v in board.items() if v == "@")) == 1:
        sx, xy = source
        board[source] = '#'
        for dir in DIRS:
            board[add(source, dir)] = '#'
        for dx in (-1,1):
            for dy in (-1, 1):
                board[add(source, (dx, dy))] = '@'

    sources = tuple(sorted(k for k, v in board.items() if v == "@"))
    ssources = ''.join(str(i) for i in range(len(sources)))
    for src, name in zip(sources, ssources):
        board[src] = name

    routes = trace(board, sources)

    def edges(cur):
        poses, keys = cur

        # print()
        # print(cur, '==================')
        for pos in poses:
            for target, dist, doors in routes[pos]:
                if target not in keys and doors.issubset(keys):
                    nextposes = poses.replace(pos, target)
                    nextkeys = keys | {target}

                    nxt = (nextposes, nextkeys)
                    # print(nxt, dist)
                    yield nxt, dist

    cost, final = dijkstra(edges, (ssources, frozenset()), target=allkeys)

    return cost[final]


def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    data = [s.strip() for s in file]

    part1 = go(data, part1=True)
    part2 = go(data, part1=False)
    print(part1)
    print(part2)


if __name__ == '__main__':
    main(sys.argv)
