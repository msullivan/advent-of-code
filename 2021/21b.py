#!/usr/bin/env python3

import sys
from collections import defaultdict, Counter, deque
import re

def extract(s):
    return [int(x) for x in re.findall(r'(-?\d+).?', s)]

def upd(t, i, x):
    t = list(t)
    t[i] = x
    return tuple(t)


def go(player, states, done):
    # advance all the pieces three times
    for _ in range(3):
        nstates = defaultdict(int)
        for move in range(1, 4):
            for state, cnt in states.items():
                p, score = state[player]
                np = p + move
                while np > 10:
                    np -= 10
                nstates[upd(state, player, (np, score))] += cnt
        states = nstates

    # score
    nstates = defaultdict(int)
    for state, cnt in states.items():
        p, score = state[player]
        nstates[upd(state, player, (p, p+score))] += cnt
    states = nstates

    dead = [
        (((b, p1), (a, p2)), n)
        for ((b, p1), (a, p2)), n in states.items()
        if (n == 0 or p1 >= 21 or p2 >= 21)
    ]
    done.update(dead)
    for x, _ in dead:
        del states[x]

    return states


def main(args):
    data = [s.strip() for s in sys.stdin]
    p1 = extract(data[0])[1]
    p2 = extract(data[1])[1]

    done = set()
    states = defaultdict(int, {((p1, 0), (p2, 0)): 1})

    while states:
        for player in range(2):
            states = go(player, states, done)

    n1 = sum(n for ((_, p1), (_, p2)), n in done if p1 >= 21)
    n2 = sum(n for ((_, p1), (_, p2)), n in done if p2 >= 21)
    print(max(n1, n2))


if __name__ == '__main__':
    main(sys.argv)
