#!/usr/bin/env python3

import sys
from collections import defaultdict, Counter, deque
import re

def extract(s):
    return [int(x) for x in re.findall(r'(-?\d+).?', s)]

LETTERS = "abcdefghijklmnopqrstuvwxyz"

def dropx(p):
    return (p[0], p[1], p[2]-1)
def drop(p):
    return dropx(p[0]), dropx(p[1])

def spots(p):
    sp = set()
    p0, p1 = p
    for x in range(p0[0], p1[0]+1):
        for y in range(p0[1], p1[1]+1):
            for z in range(p0[2], p1[2]+1):
                sp.add((x, y, z))
    return sp

def collides(x, y):
    sy = list(spots(y))
    return bool(set(spots(x)) & set(sy))

def candrop(data, live, x):
    if x[0][2] == 1 or x[1][2] == 1:
        return None

    nx = drop(x)
    sx = spots(x)
    overlap = spots(nx) & live
    if overlap - sx:
        return None
    return nx

def go(data, kill, active):
    data = list(data)
    active = set(active)
    chained = set()

    dropped = True
    while dropped:
        print("LOOP", kill)
        dropped = False
        for i, x in enumerate(data):
            if i == kill:
                continue
            if nx := candrop(data, active, x):
                chained.add(i)
                data[i] = nx
                # print("DROPPED", x, nx)
                dropped = True
                active -= spots(x)
                active |= spots(nx)

    return len(chained)


def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    # data = [x.rstrip('\n').split('\n') for x in file.read().split('\n\n')]
    # data = [int(s.rstrip('\n')) for s in file]
    data = [extract(s.rstrip('\n')) for s in file]

    data = [(tuple(x[:3]), tuple(x[3:])) for x in data]

    # data.sort(key=lambda x: min(x[0][2], x[1][2]))

    if len(data) <= len(LETTERS):
        asdf = LETTERS
    else:
        asdf = defaultdict(lambda: '')

    print(data)
    for x in data:
        print(list(spots(x)))

    active = set()
    for x in data:
        active |= set(spots(x))

    dropped = True
    while dropped:
        print("LOOP")
        dropped = False
        for i, x in enumerate(data):
            if nx := candrop(data, active, x):
                data[i] = nx
                print("DROPPED", asdf[i], x, nx)
                dropped = True
                active -= spots(x)
                active |= spots(nx)


    for i, x in enumerate(data):
        print('BLOCK', asdf[i], x)

    p1 = 0
    num = 0
    for i, x in enumerate(data):
        active -= spots(x)

        new = go(data, i, active)
        if new == 0:
            p1 += 1
        num += new

        active |= spots(x)

    print(p1)
    print(num)

if __name__ == '__main__':
    main(sys.argv)
