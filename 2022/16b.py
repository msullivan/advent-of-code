#!/usr/bin/env python3

import os
import sys
from collections import deque
import re
from itertools import chain, combinations
import functools

def extract(s):
    return [int(x) for x in re.findall(r'(-?\d+).?', s)]

def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))


# This is a big memory use optimization for frozensets
@functools.lru_cache(None)
def canonicalize(x):
    return x

MAX = 26
# MAX = 30

def next_states1(shortest, rates, state):
    pos, avail, time = state

    if time == MAX:
        return []

    avail = canonicalize(avail - {pos})

    nexts = []
    for p in avail:
        s = shortest[pos, p] + 1
        if time + s < MAX:
            nexts.append((p, avail, time+s))

    return nexts

ROUTE = {}
CACHE = {}
HIT = 0
GOS = 0
def optimize(shortest, rates, state):
    global PRUNES, HIT, GOS
    if state in CACHE:
        # print("HIT", state, CACHE[state])
        HIT += 1
        return CACHE[state]
    pos, avail, time = state

    nexts = next_states1(shortest, rates, state)

    ours = rates[pos] * (MAX-time) if pos in rates else 0
    opts = []
    for st in nexts:
        val = optimize(shortest, rates, st) + ours
        opts.append(val)

    score = max(opts, default=ours)

    # if opts:
    #     which = nexts[opts.index(best)]
    #     print("BEST OPTION FROM", state, which, best)
    #     ROUTE[state] = (which, score, score-best)
    # print(state, score)
    GOS += 1
    if GOS % 10000 == 0:
        print(GOS, len(CACHE), HIT, state)
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

    print('num real valves', len(rates))

    # We could handle this case but do not
    assert 'AA' not in rates

    # Compute the best answer for the powerset of everything
    # (they will share a lot of cache hits)
    powers = [frozenset(s) for s in powerset(rates.keys())]
    bests = {}
    for s in powers:
        print('=============', s)
        bests[s] = optimize(short, rates, ('AA', s, 0))

    score = 0
    best = None
    for s in powers:
        other = frozenset(rates.keys() - s)
        sscore = bests[s] + bests[other]
        score = max(score, sscore)
        if score == sscore:
            best = (s, other)

    # print()
    # n = starting
    # i = 1
    # while True:
    #     print(i, n, ROUTE[n][-1] if n in ROUTE else -1)
    #     if n not in ROUTE:
    #         break
    #     n = ROUTE[n][0]
    #     i += 1

    print(len(CACHE))
    print(best)
    print(score)

    os._exit(0)  # ... this is like a 5 second speedup

if __name__ == '__main__':
    main(sys.argv)
