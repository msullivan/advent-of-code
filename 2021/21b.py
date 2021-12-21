#!/usr/bin/env python3

import sys
from collections import defaultdict, Counter, deque
import re

def extract(s):
    return [int(x) for x in re.findall(r'(-?\d+).?', s)]


def main(args):
    data = [s.strip() for s in sys.stdin]
    p1 = extract(data[0])[1]
    p2 = extract(data[1])[1]

    die = 1
    nrolls = 0

    def roll():
        nonlocal die, nrolls
        nrolls += 1
        x = die
        die = (die + 1)
        if die == 101:
            die = 1
        return x

    done = set()

    s1 = s2 = 0
    states = defaultdict(int, {((p1, 0), (p2, 0)): 1})
    while True:
        # print(states)
        for _ in range(3):
            nstates = defaultdict(int)
            for move in range(3):
                for ((p, score), z), cnt in states.items():
                    np = p + move + 1
                    while np > 10:
                        np -= 10
                    nstates[(np, score), z] += cnt
            states = nstates
        # score
        nstates = defaultdict(int)
        for ((p, score), z), cnt in states.items():
            nstates[(p, p+score), z] += cnt
        states = nstates

        # WIN CHECK
        dead = [
            (((b, p1), (a, p2)), n)
            for ((b, p1), (a, p2)), n in states.items()
            if (n == 0 or p1 >= 21 or p2 >= 21)
        ]
        done.update(dead)
        for x, _ in dead:
            del states[x]

        if not states:
            break

        # COPY PASTE
        for _ in range(3):
            nstates = defaultdict(int)
            for move in range(3):
                for (z, (p, score)), cnt in states.items():
                    np = p + move + 1
                    while np > 10:
                        np -= 10
                    nstates[z, (np, score)] += cnt
            states = nstates
        # score
        nstates = defaultdict(int)
        for (z, (p, score)), cnt in states.items():
            nstates[z, (p, p+score)] += cnt
        states = nstates

        dead = [
            (((b, p1), (a, p2)), n)
            for ((b, p1), (a, p2)), n in states.items()
            if (n == 0 or p1 >= 21 or p2 >= 21)
        ]
        done.update(dead)
        for x, _ in dead:
            del states[x]

        if not states:
            break

    n1 = sum(n for ((_, p1), (_, p2)), n in done if p1 >= 21)
    n2 = sum(n for ((_, p1), (_, p2)), n in done if p2 >= 21)
    print(max(n1, n2))


if __name__ == '__main__':
    main(sys.argv)
