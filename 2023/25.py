#!/usr/bin/env python3

import sys
import itertools
from collections import defaultdict
import random

def lookup(merges, k):
    e0 = k
    while e0 in merges:
        e0 = merges[e0]

    # Path compression actually made things slower in practice
    # while k in merges:
    #     p = merges[k]
    #     merges[k] = e0
    #     k = p

    return e0


def union(merges, ranks, e0, e1):
    rank0 = ranks.get(e0, 0)
    rank1 = ranks.get(e1, 0)
    if rank0 < rank1:
        e0, e1 = e1, e0
    elif rank0 == rank1:
        ranks[e0] = rank0 + 1
    merges[e1] = e0


# Implement Karger's randomized algorithm for computing minimum cut
# We'll loop until we get something where the cut is 3
# https://en.wikipedia.org/wiki/Karger%27s_algorithm
def contract(graph, edges):
    edges = list(edges)

    merges, ranks = {}, {}

    N = len(graph)
    M = len(edges)
    while N > 2:
        i = random.randrange(0, M)
        e = edges[i]
        edges[i], edges[M-1] = edges[M-1], edges[i]
        M -= 1

        e0 = lookup(merges, e[0])
        e1 = lookup(merges, e[1])

        if e0 == e1:
            continue

        union(merges, ranks, e0, e1)

        N -= 1

    groups = {}
    for n in graph:
        n0 = lookup(merges, n)
        groups.setdefault(n0, []).append(n)

    n1s, n2s = groups.values()

    cutedges = {(s, d) for s in n1s for d in graph[s] if d in n2s}
    return cutedges, n1s, n2s


def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    data = [s.rstrip('\n') for s in file]

    random.seed(1338)

    graph = defaultdict(list)
    edges = []

    for line in data:
        s, ks = line.split(': ')
        for k in ks.split(' '):
            graph[s].append(k)
            graph[k].append(s)
            edges.append(tuple(sorted([k, s])))

    first = None
    # for i in itertools.count(1):
    for i in range(400):
        cuts, n1s, n2s = contract(graph, edges)
        print(i, cuts)
        if len(cuts) == 3:
            if first is None:
                first = i
            res = len(n1s)*len(n2s)
            # break

    print(first)
    print(res)

if __name__ == '__main__':
    main(sys.argv)
