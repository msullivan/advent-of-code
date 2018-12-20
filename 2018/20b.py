#!/usr/bin/env python3


import sys
from collections import defaultdict, deque

sys.setrecursionlimit(1500)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

DIRS = { 'E': RIGHT, 'W': LEFT, 'N': UP, 'S': DOWN }

def go(x, dir):
    dx, dy = DIRS[dir]
    return (x[0] + dx, x[1] + dy)

def distances(map, y, x):
    d = deque([(y, x)])
#    dists = defaultdict(lambda x: 100000000000)
    dists = {}
    dists[y, x] = 0
    while d:
        pos = d.popleft()
        for nbr in map[pos]:
            if nbr not in dists:
                dists[nbr] = dists[pos] + 1
                d.append(nbr)
    return dists


def main(args):
    map = defaultdict(set)

    data = [s.strip() for s in sys.stdin]
#    re = '(' + data[0][1:-2] + ')'
    re = data[0][1:-1]
    print(re)

    print(len([x for x in re if x == '(']))


    positions = {(0, 0)}
    stack = []
    for j in range(len(re)):
        print(j, len(positions))
        if re[j] == '(':
            stack.append((set(positions), set()))
        elif re[j] == '|':
            stack[-1][1].update(positions)
            positions = set(stack[-1][0])
        elif re[j] == ')':
            stack[-1][1].update(positions)
            positions = stack[-1][1]
            stack.pop()
        else:
            npositions = set()
            for pos in positions:
                npos = go(pos, re[j])
#                print(pos, re[j], npos)
                map[pos].add(npos)
                map[npos].add(pos)
                npositions.add(npos)
            positions = npositions


    print(map)
    print(len(map))
    print(sum([len(x) for x in map.values()]) / 2)

    dists = distances(map, 0, 0)
    print(len([x for x in dists.values() if x >= 1000]))

if __name__ == '__main__':
    sys.exit(main(sys.argv))

# E(N|)EE
