#!/usr/bin/env python3

import sys
import time
import math

def distance(a, b):
    (x1, y1), (x2, y2) = a, b
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)


def angle(a, b):
    (x1, y1), (x2, y2) = a, b
    return -math.atan2(x2 - x1, y2 - y1)
    return distance(a, (0, 0))


def main(args):
    data = [s.strip() for s in sys.stdin]
    nobes = set()
    for y, s in enumerate(data):
        for x, c in enumerate(s):
            if c == "#":
                nobes.add((x, y))

    # My original solution used a brute force N^3 colinearity check
    seen = {}
    for c in nobes:
        seen[c] = len({angle(c, d) for d in nobes - {c}})

    m, best = max((v, k) for k, v in seen.items())
    print(m)

    def key(a):
        return (angle(best, a), distance(best, a))

    last = (1, 0)
    num = 0
    dead = set()
    while True:
        for target in sorted(nobes - {best}, key=key):
            if target not in dead and not key(last)[0] == key(target)[0]:
                dead.add(target)
                last = target
                # print("Shooting", target, len(dead))
            if len(dead) == 200:
                # print(target)
                print(target[0]*100 + target[1])
                return


if __name__ == '__main__':
    main(sys.argv)
