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
    pos, _, open, time = state
    return sum(rates[x] for x in open)

def next_states(shortest, rates, state):
    (pos1, t1), (pos2, t2), open, time = state
    if time == 26:
        return []

    next = []
    if pos1 == 'done':
        t1opts = []
    elif t1 == 0:
        open |= frozenset([pos1])
        t1opts = [(pos1, -1)]
    elif t1 > 0:
        t1opts = [(pos1, t1 - 1)]
    else:
        # PICK
        t1opts = [
            (p, s)
            for p in rates.keys() - open
            if time+(s := (shortest[pos1, p]-1)) < 25
        ]

    if pos2 == 'done':
        t2opts = []
    elif t2 == 0:
        open |= frozenset([pos2])
        t2opts = [(pos2, -1)]
    elif t2 > 0:
        t2opts = [(pos2, t2 - 1)]
    else:
        # PICK
        t2opts = [
            (p, s)
            for p in rates.keys() - open
            if time+(s := (shortest[pos2, p]-1)) < 25
        ]

    # t2opts.append(('done', 0))
    if len(t1opts) == len(t2opts) == 1 and t1opts[0][0] == t2opts[0][0]:
        t1opts.append(('done', 0))
        t2opts.append(('done', 0))

    if not t1opts:
        t1opts = [('done', 0)]
    if not t2opts:
        t2opts = [('done', 0)]

    next = []
    for t1o in t1opts:
        for t2o in t2opts:
            # print('?', t1o, t2o)
            if t1o[0] != t2o[0] or t1o[0] == 'done':
                next.append((t1o, t2o, open, time+1))

    next2 = set()
    for a, b, c, d in next:
        a, b = sorted([a, b])
        next2.add((a, b, c, d))

    return list(next2)


# WA: 2452 too low, 2459 too low
ROUTE = {}
CACHE = {}
ASDF = 0
PRUNES = 0
HIT = 0
GOS = 0
def optimize(shortest, rates, state, prune=0):
    global PRUNES, HIT, GOS
    GOS += 1
    # ours = score_step(shortest, rates, state)
    # if prune > ASDF*(27-state[-1]):
    #     print("PRUNE", state, prune, ASDF*(27-state[-1]), state[-1], ours)
    #     PRUNES += 1
    #     return 0
    if state in CACHE:
        # print("HIT", state, CACHE[state])
        HIT += 1
        return CACHE[state]
    pos, pos2, open, time = state

    ours = score_step(shortest, rates, state)
    nexts = next_states(shortest, rates, state)

    # best = max(0, prune-ours)
    best = ours
    opts = []
    for st in nexts:
        val = optimize(shortest, rates, st, prune=best) + ours * (st[-1]-time)
        opts.append(val)
        best = max(best, val)

    score = best

    # if opts:
    #     which = nexts[opts.index(best)]
    #     print("BEST OPTION FROM", state, which, best)
    #     ROUTE[state] = (which, score, score-best)
    # print(state, score)
    if GOS % 10000 == 0:
        print(GOS, len(CACHE), PRUNES, HIT, state)
    if time <= 23:
        CACHE[state] = score
    return score


def shortest_paths(m):
    allshortest = {}
    for n in m:
        wl = deque([(n, 0)])
        seen = set()
        while wl:
            nbr, cost = wl.popleft()
            if nbr in seen:
                continue
            seen.add(nbr)
            allshortest[n, nbr] = cost
            for nbr2 in m[nbr]:
                wl.append((nbr2, cost+1))
    return allshortest


def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    data = [s.rstrip('\n') for s in file]


    rates = {}
    map = {}
    for line in data:
        x = line.split(' ')[1]
        rate = extract(line)[0]
        rest = line.replace('valves', 'valve').split('valve ')[1].split(', ')
        if rate:
            rates[x] = rate
        map[x] = rest

    short = shortest_paths(map)

    starting = (('AA', -1), ('AA', -1), frozenset(), 1)

    print('MAX', sum(rates.values()))
    global ASDF
    ASDF = sum(rates.values())
    print('num real valves', len(rates))


    score = optimize(short, rates, starting)
    print()
    n = starting
    i = 1
    # while True:
    #     print(i, n, ROUTE[n][-1] if n in ROUTE else -1)
    #     if n not in ROUTE:
    #         break
    #     n = ROUTE[n][0]
    #     i += 1

    print(len(CACHE))
    print(score)

if __name__ == '__main__':
    main(sys.argv)
