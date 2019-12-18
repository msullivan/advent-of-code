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
    data = [s.strip() for s in sys.stdin]

    board = defaultdict(lambda: " ")
    m = data

    for y in range(len(m)):
        for x in range(len(m[y])):
            board[x,y] = m[y][x]

    source = next(k for k, v in board.items() if v == "@")
    allkeys = {v for v in board.values() if v.islower()}

    if len(tuple(k for k, v in board.items() if v == "@")) == 1:
        sx, xy = source
        board[source] = '#'
        for dir in DIRS:
            board[add(source, dir)] = '#'
        for dx in (-1,1):
            for dy in (-1, 1):
                board[add(source, (dx, dy))] = '@'

    sources = tuple(sorted(k for k, v in board.items() if v == "@"))


    #### real one
    bigq = deque([(0, (sources, frozenset()))])
    seen = {(sources, frozenset())}

    i = 0

    best = 100000000000000000000
    while bigq:
#        if not bigq: print(seen)
        i += 1
        bigsteps, (bigposes, bigkeys) = bigq.popleft()
        if i % 100 == 0:
            print("BIG", i, bigsteps, bigposes, bigkeys)
        if bigkeys == allkeys:
            print("FUCK GOT IT", bigsteps)
            best = min(best, bigsteps)

        for robot in range(4):

            q = deque([(bigsteps, (bigposes, bigkeys))])
            j = 0
            while q:
                steps, (poses, keys) = q.popleft()

                j += 1
                # print(i, robot, steps, poses, keys)
                for dir in range(0, 4):
                    nextpos = add(poses[robot], DIRS[dir])
                    # update
                    nextposes = list(poses)
                    nextposes[robot] = nextpos
                    nextposes = tuple(nextposes)

                    # lol
                    nkeys = keys
                    if board[nextpos].islower():
                        nkeys = keys | frozenset([board[nextpos]])
                    if (nextposes, nkeys) in seen:
                        continue

                    seen.add((nextposes, nkeys))


                    tp = board[nextpos]
                    if tp.islower() and tp not in keys:
                        bigq.append((steps+1, (nextposes, nkeys)))
                        # print("YEAAAH", bigq[-1], tp)
                    elif tp != "#" and (not tp.isupper() or tp.lower() in keys):
                        q.append((steps+1, (nextposes, nkeys)))



    # i = 0
    # while q:
    #     i += 1
    #     steps, (poses, keys) = q.popleft()
    #     if i % 1000 == 0:
    #         print(i, steps, poses, keys)
    #     if keys == allkeys:
    #         break

    #     for robot in range(4):
    #         for dir in range(0, 4):
    #             nextpos = add(poses[robot], DIRS[dir])
    #             # update
    #             nextposes = list(poses)
    #             nextposes[robot] = nextpos
    #             nextposes = tuple(nextposes)

    #             # lol
    #             nkeys = keys
    #             if board[nextpos].islower():
    #                 nkeys = keys | frozenset([board[nextpos]])
    #             if (nextposes, nkeys) in seen:
    #                 continue

    #             seen.add((nextposes, nkeys))


    #             tp = board[nextpos]
    #             if tp != "#" and (not tp.isupper() or tp.lower() in keys):
    #                 q.append((steps+1, (nextposes, nkeys)))

    print(bigsteps)
    print(best)


if __name__ == '__main__':
    main(sys.argv)
