#!/usr/bin/env python3

from collections import defaultdict, deque
import heapq
import sys

DIRS = [(0, -1), (1, 0), (0, 1), (-1, 0)]


def add(v1, v2):
    return (v1[0] + v2[0], v1[1] + v2[1])


def trace(board, sources):
    sources = list(sources)
    sources += [k for k, v in board.items() if v.islower()]

    routes = {}

    for source in sources:
        routes[source] = set()

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

                if tp.islower():
                    routes[source].add((nextpos, steps+1, doors))
                    continue

                ndoors = doors
                if tp.isupper():
                    ndoors = doors | {tp.lower()}

                if nextpos in seen:
                    continue
                seen.add(nextpos)
                q.append((steps+1, ndoors, nextpos))

    return routes


def dijkstra(edges, start, target=None):
    cost = {start: 0}
    todo = [(0, start)]
    explored = 0
    relaxed = 0

    while todo and todo[0][-1][-1] != target:
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

    print(f'{explored=}, {relaxed=}')

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

    routes = trace(board, sources)

    def edges(cur):
        poses, keys = cur
        es = []

        for i, pos in enumerate(poses):
            for target, dist, doors in routes[pos]:
                if doors.issubset(keys):
                    nextposes = list(poses)
                    nextposes[i] = target
                    nextposes = tuple(nextposes)

                    nextkeys = keys | {board[target]}

                    es.append(((nextposes, nextkeys), dist))

        # print(board[cur[0][0]], cur, '==================')
        # for x in es:
        #     print(board[x[0][0][0]], x)
        # print()

        return es

    cost, final = dijkstra(edges, (sources, frozenset()), target=allkeys)

    return cost[final]


def main(args):
    data = [s.strip() for s in sys.stdin]

    part1 = go(data, part1=True)
    part2 = go(data, part1=False)
    print(part1)
    print(part2)

if __name__ == '__main__':
    main(sys.argv)
