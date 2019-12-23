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

N = 10007
#N = 10

def main(args):
    data = [s.strip() for s in sys.stdin]
    data *= int(args[1]) if args[1:] else 1

    cards = list(range(N))

    for s in data:
        if s == "deal into new stack":
            cards.reverse()
        elif s.startswith("deal with"):
            (increment,) = extract(s)
            new = [None] * len(cards)
            i = 0
            j = 0
            while i < len(cards):
                assert new[j] is None
                new[j] = cards[i]
                i += 1
                j = (j + increment) % len(cards)
            cards = new
        else:
            (cut,) = extract(s)
            cards = cards[cut:] + cards[:cut]

    # print(cards)
    # print(cards[-1])
    print(cards.index(2019))

if __name__ == '__main__':
    main(sys.argv)
