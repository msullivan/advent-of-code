#!/usr/bin/env python3

import sys
from collections import defaultdict, Counter, deque


def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    data = [s.rstrip('\n') for s in file]

    m = defaultdict(set)

    for line in data:
        x, y = line.split('-')
        m[x].add(y)
        m[y].add(x)


    trips = set()
    for nobe in m:
        for nbr in m[nobe]:
            for nbr2 in m[nobe]:
                if nbr == nbr2:
                    continue
                if nbr2 in m[nbr]:
                    trips.add(frozenset([nobe, nbr, nbr2]))


    cliques = trips
    while len(cliques) > 1:
        print(len(list(cliques)[0]), len(cliques))
        ncliques = set()
        for c1 in cliques:
            x = next(iter(c1))
            for n in m[x]:
                if n not in c1:
                    ns = m[n]
                    if all(c in ns for c in c1):
                        ncliques.add(c1 | {n})

        cliques = ncliques

    x = ','.join(sorted(list(cliques)[0]))
    print(x)

if __name__ == '__main__':
    main(sys.argv)
