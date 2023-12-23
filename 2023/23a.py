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
            m[x, y] = c
            if c in "v>":
                sp.add((x, y))

    def nbrs(p):
        if m[p] == 'v':
            return [vadd(DOWN, p)]
        if m[p] == '>':
            return [vadd(RIGHT, p)]
        ns = []
        for dir in VDIRS:
            np = vadd(dir, p)
            if np in m and m[np] != '#':
                if m[np] == 'v' and dir == UP:
                    continue
                if m[np] == '>' and dir == LEFT:
                    continue
                ns.append(np)
        return ns

    sx = data[0].index('.')
    start = (sx, 0)
    sp.add(start)
    sx = data[-1].index('.')
    end = (sx, len(data)-1)
    sp.add(end)

    def explore(node):
        q = deque([(node, 0)])
        seen = set()

        targets = {}
        while q:
            n, dst = q.popleft()
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
    @functools.cache
    def go(node):
        print(node)
        if node == end:
            return 0
        tree[node].pop(node, None)
        assert node not in tree[node]
        res = max(dst + go(x) for x, dst in tree[node].items() if node != x)
        return res


    print(go(start))

if __name__ == '__main__':
    main(sys.argv)
