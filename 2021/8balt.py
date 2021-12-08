#!/usr/bin/env python3

import sys

import copy
from collections import defaultdict, Counter, deque
from parse import parse
import re
import itertools

def extract(s, pos=False):
    p = '' if pos else '-?'
    return [int(x) for x in re.findall(fr'{p}\d+', s)]

def vadd(v1, v2):
    return tuple(x + y for x, y in zip(v1, v2))

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
    return VDIRS[(VDIRS.index(v) + n + len(VDIRS))%len(VDIRS)]


##############################

CS = [
    "abcefg", "cf", "acdeg", "acdfg", "bcdf",
    "abdfg", "abdefg", "acf", "abcdefg", "abcdfg",
]
LENS = set(len(x) for x in CS)
RCS = {l: [(i, x) for i, x in enumerate(CS) if len(x) == l] for l in LENS}
MCS = {k: i for i, k in enumerate(CS)}

def get(s):
    l = list(s)
    assert len(l) == 1, s
    return l[0]

# easy 1,4, 7, 8
def solve(codes, nums):
    LETS = "abcdefg"
    for perm in itertools.permutations(LETS):
        m = {k: v for k, v in zip(perm, LETS)}
        pcodes = ["".join(sorted(m[c] for c in code)) for code in codes]
        matches = {MCS.get(pcode) for pcode in pcodes}
        if len(matches) == 10 and None not in matches:
            break
    else:
        raise ValueError


    snum = ""
    for num in nums:
        numk = "".join(sorted(m[c] for c in num))
        snum += str(MCS[numk])
    rnum = int(snum)
    print(rnum)
    return rnum




def main(args):
    # data = [x.split('\n') for x in sys.stdin.read().split('\n\n')]
    # data = [int(s.strip()) for s in sys.stdin]
    data = [s.strip() for s in sys.stdin]
    data = [x.split(" | ") for x in data]
    data = [(x.split(" "), y.split(" ")) for x, y in data]

    # solve(*data[0])
    print(sum(solve(*ent) for ent in data))

    # print(RCS)

if __name__ == '__main__':
    main(sys.argv)
