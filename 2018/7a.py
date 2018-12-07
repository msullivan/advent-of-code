#!/usr/bin/env python3

import sys
from collections import defaultdict

def build_rgraph(graph):
    rgraph = {k: set() for k in graph.keys()}
    for u in graph.keys():
        for v in graph[u]:
            rgraph[v].add(u)
    return rgraph

def main(args):
    data = list([s.strip().split(' ') for s in sys.stdin])
    asdf = [(x[1], x[-3]) for x in data]

    xs, ys = zip(*asdf)
    all = set(xs + ys)
    graph = {x: set() for x in all}
    for a, b in asdf:
        graph[a].add(b)
    rgraph = build_rgraph(graph)

    seen = set()
    avail = list(all - set(ys))
    order = []
    while avail:
        avail.sort()
        x = avail.pop(0)
        order.append(x)
        seen.add(x)
        for y in graph[x]:
            rgraph[y].discard(x)
            if not rgraph[y] and y not in seen:
                seen.add(y)
                avail.append(y)
    print(''.join(order))

if __name__ == '__main__':
    sys.exit(main(sys.argv))
