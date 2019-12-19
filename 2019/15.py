#!/usr/bin/env python3

import copy
import sys
import time
from collections import defaultdict, deque
from intcode import IntCode

DIRS = [(0, -1), (0, 1), (1, 0), (-1, 0)]

def draw(painted):
    minx = min(x for x, y in painted)
    miny = min(y for x, y in painted)
    maxx = max(x for x, y in painted)
    maxy = max(y for x, y in painted)
    l = ""
    for y in range(miny, maxy+1):
        for x in range(minx, maxx+1):
            l += painted[x,y]
        l += "\n"
    print(l)


def step(p, i):
    p2 = copy.deepcopy(p)
    asdf = p2.run([i])
    assert not p2.done
    (out,) = asdf
    return p2, out

def add(v1, v2):
    return tuple(x + y for x, y in zip(v1, v2))

def main(args):
    data = [s.strip() for s in sys.stdin]
    lp = [int(x) for x in data[0].split(",")]
    p = defaultdict(int, [(i, x) for i, x in enumerate(lp)])
    board = defaultdict(lambda: " ")

    # Part 1
    interp = IntCode(p)
    q = deque([(interp, 0, (0, 0))])
    seen = {(0, 0)}

    while q:
        p, steps, pos = q.popleft()
        for dir in range(0, 4):
            nextpos = add(pos, DIRS[dir])
            if nextpos in seen:
                continue
            seen.add(nextpos)

            p2, state = step(p, dir+1)
            if state == 2:
                part1 = steps+1
                source = nextpos
                board[nextpos] = "."
                print(nextpos, steps+1)
            elif state == 1:
                board[nextpos] = "."
                q.append((p2, steps+1, nextpos))
            elif state == 0:
                board[nextpos] = "#"

    draw(board)


    # Part 2
    q = deque([(0, source)])
    seen = {source}

    while q:
        steps, pos = q.popleft()
        for dir in range(0, 4):
            nextpos = add(pos, DIRS[dir])
            if nextpos in seen:
                continue
            seen.add(nextpos)

            if board[nextpos] == ".":
                q.append((steps+1, nextpos))

    print(part1)
    print(steps)


if __name__ == '__main__':
    sys.exit(main(sys.argv))
