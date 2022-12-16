#!/usr/bin/env python3

import sys
from collections import defaultdict, Counter, deque
from parse import parse
import re
import math

def extract(s):
    return [int(x) for x in re.findall(r'(-?\d+).?', s)]

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

# state is (valves on, time left, position)

def score_step(m, rates, state):
    pos, open, time = state
    return sum(rates[x] for x in open)

def next_states(m, rates, state):
    pos, open, time = state
    if time == 30:
        return []

    next = []
    for nbr in m[pos]:
        next.append((nbr, open, time+1))
    if rates[pos] != 0:
        next.append((pos, open|frozenset([pos]), time+1))

    return next


CACHE = {}
def optimize(m, rates, state):
    if state in CACHE:
        return CACHE[state]
    pos, open, time = state
    if time == 0:
        return 0  # ??

    opts = [optimize(m, rates, st) for st in next_states(m, rates, state)]
    best = max(opts, default=0)
    score = best + score_step(m, rates, state)
    print(state, score)
    CACHE[state] = score
    return score



def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    # data = [x.rstrip('\n').split('\n') for x in file.read().split('\n\n')]
    # data = [int(s.rstrip('\n')) for s in file]
    data = [s.rstrip('\n') for s in file]


    rates = {}
    map = {}
    for line in data:
        x = line.split(' ')[1]
        rate = extract(line)[0]
        # print(line.replace('valve', 'valves').split('valves '))
        rest = line.replace('valves', 'valve').split('valve ')[1].split(', ')
        rates[x] = rate
        map[x] = rest

    starting = ('AA', frozenset(), 1)

    print(rates)
    print(map)

    score = optimize(map, rates, starting)
    print(score)

if __name__ == '__main__':
    main(sys.argv)
