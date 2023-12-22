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

def gspots(p):
    p0, p1 = p
    if p0[0] != p1[0]:
        s, e = sorted([p0[0], p1[0]])
        for i in range(s, e+1):
            yield i, p0[1], p1[2]
    elif p0[1] != p1[1]:
        s, e = sorted([p0[1], p1[1]])
        for i in range(s, e+1):
            yield p0[0], i, p1[2]
    elif p0[2] != p1[2]:
        s, e = sorted([p0[2], p1[2]])
        for i in range(s, e+1):
            yield p0[0], p0[1], i
    else:
        yield p0

def spots(p):
    return set(gspots(p))

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


def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    # data = [x.rstrip('\n').split('\n') for x in file.read().split('\n\n')]
    # data = [int(s.rstrip('\n')) for s in file]
    data = [extract(s.rstrip('\n')) for s in file]

    data = [(tuple(x[:3]), tuple(x[3:])) for x in data]

    asdf = LETTERS
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

        nactive = set()
        for x in data:
            nactive |= set(spots(x))
        assert active == nactive


            # for i, x in enumerate(data):
            #     for j, y in enumerate(data):
            #         if i == j:
            #             continue
            #         assert not (spots(x) & spots(y))


    for i, x in enumerate(data):
        print('BLOCK', asdf[i], x)

    for i, x in enumerate(data):
        for j, y in enumerate(data):
            if i == j:
                continue
            assert not (spots(x) & spots(y))


    num = 0
    for i, x in enumerate(data):
        active -= spots(x)

        can = True
        for j, y in enumerate(data):
            if i == j:
                continue
            if uh := candrop(data, active, y) :
                print(asdf[i], 'fails', y, asdf[j], 'drops')
                print(uh)
                can = False

        if can:
            print('kill', x, asdf[i])
            num += 1
        active |= spots(x)

    print(num)

if __name__ == '__main__':
    main(sys.argv)
