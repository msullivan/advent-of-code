#!/usr/bin/env python3

import sys
import re
import time
import math
from fractions import Fraction


def extract(s):
    return [int(x) for x in re.findall(r'\d+', s)]


def ordered(x, y, z):
    return [x, y, z] == sorted([x, y, z]) or [x, y, z] == list(reversed(sorted([x, y, z])))


def colinear(a, b, c):
    x1, y1 = a
    x2, y2 = b
    x3, y3 = c
    return (y2 - y1) * (x3 - x1) == (y3 - y1) * (x2 - x1) and ordered(x1, x2, x3) and ordered(y1, y2, y3)

def distance(a, b):
    x1, y1 = a
    x2, y2 = b
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def norm(a):
    return distance(a, (0, 0))


def main(args):
    data = [s.strip() for s in sys.stdin]
    nobes = set()
    for y, s in enumerate(data):
        for x, c in enumerate(s):
            if c == "#":
                nobes.add((x, y))

    # print(nobes)
    # print(len(nobes))

    seen = {}
    for c in nobes:
        count = 0
        for other in nobes:
            if c == other: continue
            if not any(colinear(c, x, other) for x in nobes - {c, other}):
                count += 1
        seen[c] = count

    m = max(seen.values())
    print(m)
    best = next(k for k, v in seen.items() if m == v)

    # best = (22, 19)

    xb, yb = best

    def key(a):
        x, y = a
        return (-math.atan2(x - xb, y - yb), distance(a, best))

    last = (1, 0)
    num = 0
    dead = set()
    while True:
        for target in sorted(nobes - {best}, key=key):
            if target not in dead and not colinear(best, last, target):
                dead.add(target)
                last = target
                # print("Shooting", target, len(dead))
            if len(dead) == 200:
                # print(target)
                print(target[0]*100 + target[1])
                return


if __name__ == '__main__':
    sys.exit(main(sys.argv))
