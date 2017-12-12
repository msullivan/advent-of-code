#!/usr/bin/env python3

import sys

def dfs(graph, seen, nobe):
    if nobe in seen: return
    seen.add(nobe)
    for child in graph[nobe]:
        dfs(graph, seen, child)

def main(args):
    data = [s.strip() for s in sys.stdin]
    graph = {}
    for line in data:
        k, vs = line.split(" <-> ")
        vs = vs.split(", ")
        graph[k] = set(vs)

    seen = set()
    dfs(graph, seen, "0")
    print(len(seen))

    num = 1
    for k in graph.keys():
        if k not in seen: num += 1
        dfs(graph, seen, k)
    print(num)


if __name__ == '__main__':
    sys.exit(main(sys.argv))
