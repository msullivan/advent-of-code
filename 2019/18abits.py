#!/usr/bin/env python3

# This is *slower* and I don't understand why.
# This is a very confusing performance charecteristic even for python.

from collections import defaultdict, deque
import sys
import time
import math

DIRS = [(0, -1), (1, 0), (0, 1), (-1, 0)]

def add(v1, v2):
    return tuple(x + y for x, y in zip(v1, v2))


def ichr(i):
    return chr(ord('a') + i)

def iord(c):
    return ord(c.lower()) - ord('a')


def main(args):
    data = [s.strip() for s in sys.stdin]

    board = defaultdict(lambda: " ")
    m = data

    for y in range(len(m)):
        for x in range(len(m[y])):
            board[x,y] = m[y][x]

    source = next(k for k, v in board.items() if v == "@")
    keyvals = {v: 1 << iord(v) for v in board.values() if v.islower()}
    allkeys = sum(keyvals.values())
    keyvals.update({k.upper(): v for k, v in keyvals.items()})

    nokeys = 0

    print(keyvals)
    print(bin(allkeys))

    q = deque([(0, (source, nokeys))])
    seen = {(source, nokeys)}

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
                nkeys = keys | keyvals[board[nextpos]]
            if (nextpos, nkeys) in seen:
                continue

            seen.add((nextpos, nkeys))

            if not tp.isupper() or (keyvals[tp] & keys):
                q.append((steps+1, (nextpos, nkeys)))

    print(len(seen))
    print(steps)


if __name__ == '__main__':
    main(sys.argv)
