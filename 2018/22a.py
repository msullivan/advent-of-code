#!/usr/bin/env python3

from collections import defaultdict, deque
import sys
import re
import time
from functools import lru_cache
#from dataclasses import dataclass

@lru_cache(None)
def index(target, depth, x, y):
    if x == 0 and y == 0:
        return 0
    if (x, y) == target:
        return 0
    if y == 0:
        return x * 16807
    if x == 0:
        return y * 48271
    return erosion(target, depth, x-1, y) * erosion(target, depth, x, y-1)

@lru_cache(None)
def erosion(target, depth, x, y):
    return (index(target, depth, x, y) + depth) % 20183

def go(depth, target):
    tx, ty = target

    risk = 0
    for x in range(tx+1):
        for y in range(ty+1):
            e = erosion(target, depth, x, y)
            print(x, y, e, e%3, index(target, depth, x, y))
            risk += e%3

    print(risk)


def main(args):
    go(11739, (11, 718))
    #go(510, (10, 10))
if __name__ == '__main__':
    sys.exit(main(sys.argv))
