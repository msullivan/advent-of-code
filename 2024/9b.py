#!/usr/bin/env python3

import sys
from collections import defaultdict, Counter, deque
from parse import parse
import re
import math
import itertools

def extract(s):
    return [int(x) for x in re.findall(r'(-?\d+).?', s)]

def vadd(v1, v2):
    if len(v1) == 2:
        return v1[0] + v2[0], v1[1] + v2[1]
    elif len(v1) == 2:
        return v1[0] + v2[0], v1[1] + v2[1], v1[2] + v2[2]
    else:
        # ... this is so slow.
        return tuple([x + y for x, y in zip(v1, v2)])

def ichr(i):
    return chr(ord('a') + i)

def iord(c):
    return ord(c.lower()) - ord('a')

def optidx(d, opt=max, nth=0):
    if not isinstance(d, dict):
        d = dict(enumerate(d))
    rv = opt(d.values())
    return [i for i, v in d.items() if v == rv][nth], rv

LETTERS = "abcdefghijklmnopqrstuvwxyz"

UP, RIGHT, DOWN, LEFT = VDIRS = (0, -1), (1, 0), (0, 1), (-1, 0),
DIRS = {'N': UP, 'E': RIGHT, 'S': DOWN, 'W': LEFT }
ALL_DIRS = [(x, y) for x in [-1,0,1] for y in [-1,0,1] if not x == y == 0]

def turn(v, d='left'):
    n = -1 if d == 'left' else 1
    return VDIRS[(VDIRS.index(v) + n) % len(VDIRS)]


##############################

def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    # data = [x.rstrip('\n').split('\n') for x in file.read().split('\n\n')]
    # data = [int(s.rstrip('\n')) for s in file]
    data = [s.rstrip('\n') for s in file]

    data = [int(x) for x in data[0]]
    i = 0
    spots = []
    free = deque()
    files = {}

    pos = 0
    id = 0
    while i < len(data):
        files[id] = len(spots), data[i]
        for _ in range(data[i]):
            spots.append(id)
        id += 1
        i += 1
        if i >= len(data):
            break
        for _ in range(data[i]):
            free.append(len(spots))
            spots.append(None)
        i += 1

    assert len([x for x in spots if x is None]) == len(free)

    octr = Counter(spots)

    last = len(spots) - 1
    for i in range(len(files)-1, -1, -1):
        # print(spots)
        # fuck = ''.join(['.' if x is None else str(x) for x in spots])
        # print(fuck)

        start, tsize = files[i]
        j = 0
        lmost = None
        size = 0
        while j < start:
            if spots[j] is None:
                size += 1
                if lmost is None:
                    lmost = j
            else:
                size = 0
                lmost = None

            if size == tsize:
                break

            j += 1

        if lmost is not None and size == tsize:
            for k in range(tsize):
                spots[lmost+k] = i
                spots[start+k] = None

    # while last >= 0:
    #     # print(spots)
    #     # fuck = ''.join(['.' if x is None else str(x) for x in spots])
    #     # print(fuck)
    #     if spots[last] is not None and free:
    #         pos = free.popleft()
    #         if pos > last:
    #             break
    #         assert spots[pos] is None
    #         spots[pos] = spots[last]
    #         spots[last] = None
    #     last -= 1

    # while free:
    #     while spots[last] is None:
    #         last -= 1
    #     pos = free.popleft()
    #     # if pos >= len(spots):
    #     #     continue
    #     #     # break
    #     assert spots[pos] is None
    #     val = spots[last]
    #     assert pos != last
    #     spots[pos] = val
    #     spots[last] = None

    #     del spots[last]
    #     # assert all(x is None for x in spots[last:]), (pos, last, spots[pos], spots[last:])
    #     last -= 1
    # # assert len([x for x in spots if x is None]) == len(free)

    cksum = 0
    for i, v in enumerate(spots):
        if v is not None:
            cksum += i * v


    assert octr == Counter(spots)
    print(spots)
    # print(free)
    print(cksum)

if __name__ == '__main__':
    main(sys.argv)
