#!/usr/bin/env python3

# This is the code I wrote to solve this problem, but the code does
# not produce an answer. The first thing I tried was assuming that the
# pattern would cycle (which was a technique that worked for solving a
# transistion system problem last year), so I wrote code to look for a
# repeat.

# My machine started churning, so I added an if i % 10000 == 0:
# print(i) And it never printed. It turns out that this is basically
# the slowest cellular automata implementation you could imagine.

# Anyways I ended up printing out a bunch of data and noticing that it
# always increased by the same amount, so ctrl-c, and did some
# arithmetic based on the printed values.

import sys
from collections import defaultdict, deque

def main(args):
    data = [s.strip() for s in sys.stdin]

    initial = data[0].split(" ")[2]
    stuff = [x.split(' ') for x in data[2:]]
    stuff = dict([(x, z) for x, _, z in stuff])

    plants = defaultdict(lambda: '.')
    for i, x in enumerate(initial):
        plants[i] = x

    seen = {}

    for i in range(50000000000):
        if i % 10000 == 0: print(i)
        new = defaultdict(lambda: '.')
        bottom = min(plants.keys())
        top = max(plants.keys())
        for j in range(bottom-3, top+3):
            key = "".join(plants[k] for k in range(j-2, j+3))
            assert len(key) == 5
            new[j] = stuff[key]
        plants = new
        real = tuple(k for k, v in plants.items() if v == '#')
        print(i, len(real), real, sum(real))
        if real in seen:
            break
        seen[real] = i

    print(i, seen[real])

#    print([k for k, v in stuff.items() if v == '#'])
    print(sum(k for k, v in plants.items() if v == '#'))

    # print(initial)
    # print(stuff)

if __name__ == '__main__':
    sys.exit(main(sys.argv))
