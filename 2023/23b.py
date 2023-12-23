#!/usr/bin/env python3

import sys
from collections import defaultdict, Counter, deque

def vadd(v1, v2):
    return tuple([x + y for x, y in zip(v1, v2)])

UP, RIGHT, DOWN, LEFT = VDIRS = (0, -1), (1, 0), (0, 1), (-1, 0),

def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    data = [s.rstrip('\n') for s in file]

    m = {}
    sp = set()
    for y, l in enumerate(data):
        for x, c in enumerate(l):
            if c in "v>":
                c = '.'
            m[x, y] = c

    def nbrs(p):
        ns = []
        for dir in VDIRS:
            np = vadd(dir, p)
            if np in m and m[np] != '#':
                ns.append(np)
        return ns

    for p in m:
        if m[p] == '.' and len(nbrs(p)) != 2:
            sp.add(p)

    sx = data[0].index('.')
    start = (sx, 0)
    sx = data[-1].index('.')
    end = (sx, len(data)-1)

    def explore(node):
        q = deque([(node, 0)])
        seen = set()

        targets = {}
        while q:
            n, dst = q.popleft()
            # print(node)
            if n in seen:
                continue
            seen.add(n)

            for nbr in nbrs(n):
                if nbr in sp:
                    # print(n, nbr, dst)
                    targets[nbr] = dst+1
                else:
                    q.append((nbr, dst+1))
        print(len(targets))
        return targets

    tree = {}
    for s in sp:
        tree[s] = explore(s)

    import functools
    seen = set()
    cnted = 0
    # @functools.cache
    def go(node):
        nonlocal cnted
        if node == end:
            return 0
        if node in seen:
            return -1000000000
        seen.add(node)

        cnted += 1
        if cnted % 10000 == 0:
            print(cnted)

        res = max(dst + go(x) for x, dst in tree[node].items())
        seen.remove(node)
        return res

    print(go(start))

if __name__ == '__main__':
    main(sys.argv)
