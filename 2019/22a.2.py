#!/usr/bin/env python3

from __future__ import print_function

from collections import defaultdict, deque
import sys
import time
import math
import re

def extract(s):
    return [int(x) for x in re.findall(r'-?\d+', s)]

DIRS = [(0, -1), (1, 0), (0, 1), (-1, 0)]

def add(v1, v2):
    return tuple(x + y for x, y in zip(v1, v2))

def deal(l):
    l.reverse()

N = 10007
#N = 10

def main(args):
    data = [s.strip() for s in sys.stdin]

    cards = list(range(N))


    pos = 2019
    for s in data:
        if s == "deal into new stack":
            pos = N - 1 - pos
        elif s.startswith("deal with"):
            (increment,) = extract(s)
            pos = (pos * increment) % N
        else:
            (cut,) = extract(s)
            pos = (pos - cut) % N

    print(pos)

if __name__ == '__main__':
    main(sys.argv)
