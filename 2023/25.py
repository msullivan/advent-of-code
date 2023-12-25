#!/usr/bin/env python3

import sys
import itertools
from collections import defaultdict
import random

# Implement Karger's randomized algorithm for computing minimum cut
# We'll loop until we get something where the cut is 3
# https://en.wikipedia.org/wiki/Karger%27s_algorithm
def contract(graph, edges):
    ograph = graph
    graph = {k: v.copy() for k, v in graph.items()}
    nodes = set(graph)
    edges = list(set(edges))

    merges = dict()

    N = len(edges)
    while len(nodes) > 2:
        i = random.randint(0, len(edges)-1)
        e = edges[i]
        edges[i] = edges[-1]
        del edges[-1]

        e0 = e[0]
        while e0 in merges:
            e0 = merges[e0]
        e1 = e[1]
        while e1 in merges:
            e1 = merges[e1]

        if e1 == e0:
            continue

        new = e0 + '-' + e1
        merges[e0] = merges[e1] = new
        # print('!', len(nodes), e0, e1, new)
        # print(nodes)
        nodes.remove(e0)
        nodes.discard(e1)
        nodes.add(new)

    n1, n2 = list(nodes)
    n1s = n1.split('-')
    n2s = n2.split('-')

    cutedges = {(s, d) for s in n1s for d in graph[s] if d in n2s}
    return cutedges, n1s, n2s


def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    # data = [x.rstrip('\n').split('\n') for x in file.read().split('\n\n')]
    # data = [int(s.rstrip('\n')) for s in file]
    data = [s.rstrip('\n') for s in file]

    graph = defaultdict(set)
    edges = set()

    for line in data:
        s, ks = line.split(': ')
        for k in ks.split(' '):
            graph[s].add(k)
            graph[k].add(s)
            edges.add(tuple(sorted([k, s])))

    print(graph)
    for i in itertools.count(1):
        cuts, n1s, n2s = contract(graph, edges)
        print(i, cuts)
        if len(cuts) == 3:
            break

    print(len(n1s)*len(n2s))

if __name__ == '__main__':
    main(sys.argv)
