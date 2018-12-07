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

    workers = 5
    extra = 60

    time = 0
    finish_times = defaultdict(list)

    while True:
        done = finish_times.get(time, [])
        for x in done:
            order.append(x)
            workers += 1
            for y in graph[x]:
                rgraph[y].discard(x)
                if not rgraph[y] and y not in seen:
                    seen.add(y)
                    avail.append(y)

        if len(order) == len(all): break
        avail.sort()

        while workers > 0 and avail:
            x = avail.pop(0)
            workers -= 1
            finish_times[time + extra + ord(x) - ord('A') + 1] += [x]

        time += 1

    print(time)
    print(''.join(order))

if __name__ == '__main__':
    sys.exit(main(sys.argv))
