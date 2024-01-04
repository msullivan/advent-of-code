#!/usr/bin/env python3

from collections import defaultdict, deque
import sys
import time
import math

DIRS = [(0, -1), (1, 0), (0, 1), (-1, 0)]

def add(v1, v2):
    return tuple(x + y for x, y in zip(v1, v2))


def main(args):
    data = [s.strip() for s in sys.stdin]

    board = defaultdict(lambda: " ")
    m = data

    for y in range(len(m)):
        for x in range(len(m[y])):
            board[x,y] = m[y][x]

    source = next(k for k, v in board.items() if v == "@")
    allkeys = {v for v in board.values() if v.islower()}
    print(allkeys)

    q = deque([(0, (source, frozenset()))])
    seen = {(source, frozenset())}

    while q:
        steps, (pos, keys) = q.popleft()
        # print(steps, pos, keys)
        if keys == allkeys:
            break

        for dir in DIRS:
            nextpos = add(pos, dir)
            tp = board[nextpos]
            if tp == '#':
                continue

            nkeys = keys
            if board[nextpos].islower():
                nkeys = keys | frozenset([board[nextpos]])
            if (nextpos, nkeys) in seen:
                continue

            seen.add((nextpos, nkeys))

            if not tp.isupper() or tp.lower() in keys:
                q.append((steps+1, (nextpos, nkeys)))

    print(steps)


if __name__ == '__main__':
    main(sys.argv)
