#!/usr/bin/env python3

import sys
import re
import heapq


def extract(s):
    return [int(x) for x in re.findall(r'(-?\d+).?', s)]

def vadd(v1, v2):
    return tuple(x + y for x, y in zip(v1, v2))

UP, RIGHT, DOWN, LEFT = VDIRS = (0, -1), (1, 0), (0, 1), (-1, 0),

####

def draw(painted):
    minx = min(x for x, y in painted)
    miny = min(y for x, y in painted)
    maxx = max(x for x, y in painted)
    maxy = max(y for x, y in painted)

    l = ""
    for y in (list((range(miny, maxy+1)))):
        for x in range(minx, maxx+1):
            l += painted.get((x,y), " ")
        l += "\n"
    print(l)


def draw2(package, state):
    orig_map = package[-1]
    d, tomove = fromkey(state)
    m = orig_map.copy()

    if d['C'] == {(5,2),(5,3)}:
        breakpoint()


    for kind, poses in d.items():
        for pos in poses:
            m[pos] = kind
    draw(m)
    print(d)
    print("TO MOVE:", tomove)


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
        if explored % 1000 == 0:
            print("explored", explored)
            draw2(m, cur)
            print(cost[cur])
            print()

        # print("AT")
        # draw2(m, cur)
        # print()
        nbrs = list(edges(m, cur))
        for nbr, weight in nbrs:

            ncost = cost[cur] + weight
            if nbr not in cost or ncost < cost[nbr]:
                # print("EXPLORING")
                # print(draw2(m, nbr))
                # print()

                cost[nbr] = ncost
                path[nbr] = cur
                hcost = ncost if not heuristic else ncost + heuristic(nbr)
                heapq.heappush(todo, (hcost, ncost, nbr))
        # print("-----------------\n")

    print("TOTAL EXPLORED", explored)
    return cost, path


##############################

ROOMS = None

costs = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}

def fromkey(d):
    d, x = d
    return dict(d), x
def tokey(d, x):
    return tuple(sorted((k, frozenset(v)) for k, v in d.items())), x

target_cols = {'A': 3, 'B': 5, 'C': 7, 'D': 9}

def heuristic(state):
    c = 0
    for kind, poses in state[0]:
        for pos in poses:
            c += abs(target_cols[kind] - pos[0]) * costs[kind]
            if pos[1] == 1:
                c += costs[kind]
    return c

def edges(z, state):
    HALLWAY = 1
    hallway, rooms, above, targets, _ = z

    all = hallway|rooms
    d, tomove = fromkey(state)
    allposes = {x for s in d.values() for x in s}

    if tomove:
        (tm_k, tm_pos, tm_stopped) = tomove
        others = {x for k, p in d.items() if k != tm_k for x in p}  # perf??
        tm_occupado = (others & targets[tm_k])

        # stop the dude
        if not tm_stopped:
            if tm_pos[0] not in {3,5,7,9} or tm_pos in targets[tm_k]:
                yield (state[0], ()), 0
        if tm_pos in targets[tm_k]:
            if not tm_occupado:
                yield tokey(d, ()), 0

    else:
        for kind, poses in d.items():
            for pos in poses:
                occupado = (
                    {x for k, p in d.items() if k != kind for x in p} & targets[kind])
                if (pos not in targets[kind]) or occupado:
                    if pos in hallway:
                        if occupado:
                            continue
                        tgt = target_cols[kind]
                        no = False
                        for i in range(min(pos[0], tgt), max(pos[0], tgt)+1):
                            if i != pos[0] and (i, 1) in allposes:
                                no = True
                                break
                        if no:
                            continue
                    yield (state[0], (kind, pos, pos in hallway)), 0

    if not tomove:
        return

    for dir in VDIRS:
        nbr = vadd(dir, tm_pos)
        if nbr not in all:
            continue
        if nbr in allposes:
            continue
        if nbr[1] > tm_pos[1]:
            if nbr[0] != target_cols[tm_k]:
                continue
            if tm_occupado:
                continue

        nd = d.copy()
        nd[tm_k] = nd[tm_k] - {tm_pos} | {nbr}
        yield tokey(nd, (tm_k, nbr, tm_stopped)), costs[tm_k]

EXTRA = '''\
  #D#C#B#A#
  #D#B#A#C#'''.split('\n')


def main(args):
    PART2 = True
    if args[1] == '-1':
        PART2 = False
        args.pop(1)

    data = [s for s in open(args[1])]
    if PART2:
        data[3:3] = EXTRA


    m = {(x, y): v for y, l in enumerate(data) for x, v in enumerate(l) if v != "\n"}
    blank_map = {k: v if not v.isalpha() else " " for k, v in m.items()}

    print(m)

    hallway = {(x, 1) for x in range(1, 12)}

    noobs = {
        noob: {k for k, v in m.items() if v == noob}
        for noob in 'ABCD'
    }

    print(hallway)
    print("NOOBS", noobs)
    targets = {
        k: {(target_cols[k], i) for i in range(2,3+2*PART2+1)}
        for k in 'ABCD'
    }

    rooms = {v for s in targets.values() for v in s}
    above = hallway & {vadd(UP, x) for x in rooms}

    package = hallway, rooms, above, targets, blank_map

    target = tokey(targets, ())
    start = tokey(noobs, ())

    cost, _ = dijkstra(package, edges, start, heuristic=heuristic, target=target)
    print(cost[target])

if __name__ == '__main__':
    main(sys.argv)
