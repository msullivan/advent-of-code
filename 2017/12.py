#!/usr/bin/env python3

import sys

# copied from some other code I wrote sometime
def dfs(graph, seen, node, val=0, ordering=None):
    if node in seen: return

    seen[node] = val
    for child in graph[node]:
        dfs(graph, seen, child, val, ordering)
    if ordering is not None: ordering.append(node)

def main(args):
    data = [s.strip() for s in sys.stdin]
    graph = {}
    for line in data:
        k, vs = line.split(" <-> ")
        vs = vs.split(", ")
        graph[k] = set(vs)

    seen = {}
    dfs(graph, seen, "0")
    print(len(seen))

    num = 1
    for k in graph.keys():
        if k not in seen: num += 1
        dfs(graph, seen, k)
    print(num)


if __name__ == '__main__':
    sys.exit(main(sys.argv))
