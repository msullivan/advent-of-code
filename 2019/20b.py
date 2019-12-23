#!/usr/bin/env python3

from __future__ import print_function

from collections import defaultdict, deque
import sys
import time
import math

DIRS = [(0, -1), (1, 0), (0, 1), (-1, 0)]

def add(v1, v2):
    return tuple(x + y for x, y in zip(v1, v2))


def main(args):
    data = [s.rstrip() for s in sys.stdin]

    board = defaultdict(lambda: " ")
    m = data

    for y in range(len(m)):
        for x in range(len(m[y])):
            board[x,y] = m[y][x]

    # Parsing this is annoying!
    portals = {}
    for (x, y), val in list(board.items()):
        if not val.isupper():
            continue
        if board[x+1,y].isupper():
            s = val + board[x+1,y]
            ny = y
            if board[x+2,y] == ".":
                nx = x+2
            else:
                nx = x-1
        elif board[x,y+1].isupper():
            s = val + board[x,y+1]
            nx = x
            if board[x,y+2] == ".":
                ny = y+2
            else:
                ny = y-1
        else:
            continue

        portals.setdefault(s, []).append((nx, ny))

    portal_dests = {}
    for vs in portals.values():
        if len(vs) > 1:
            a, b = vs
            portal_dests[a] = b
            portal_dests[b] = a

    xvals = [x for x, y in portal_dests]
    yvals = [y for x, y in portal_dests]
    outerx = {min(xvals), max(xvals)}
    outery = {min(yvals), max(yvals)}
    print(outerx, outery)

    print(portal_dests)


    source = (portals['AA'][0], 0)
    dest =  (portals['ZZ'][0], 0)
    # Another BFS.
    q = deque([(0, source)])
    seen = {source}

    while True:
        steps, (pos, level) = q.popleft()

        if (pos, level) == dest:
            break

        options = [(add(pos, DIRS[dir]), level) for dir in range(0, 4)]
        if pos in portal_dests:
            if pos[0] in outerx or pos[1] in outery:
                if level > 0:
                    options.append((portal_dests[pos], level-1))
            else:
                options.append((portal_dests[pos], level+1))

        for nextpos in options:
            if nextpos in seen:
                continue
            seen.add(nextpos)

            if board[nextpos[0]] == ".":
                q.append((steps+1, nextpos))

    print(steps)



if __name__ == '__main__':
    main(sys.argv)
