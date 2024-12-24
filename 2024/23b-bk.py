#!/usr/bin/env python3

import sys
from collections import defaultdict, Counter, deque

def bron_kerbosch(r, p, x, n, out):
    if not p and not x:
        out.append(frozenset(r))

    for v in list(p):
        bron_kerbosch(r | {v}, p & n[v], x & n[v], n, out)
        p.discard(v)
        x.add(v)
        # p = p - {v}
        # x = x | {v}


def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    data = [s.rstrip('\n') for s in file]

    m = defaultdict(set)

    for line in data:
        x, y = line.split('-')
        m[x].add(y)
        m[y].add(x)


    cliques = []
    bron_kerbosch(set(), set(m), set(), m, cliques)

    x = ','.join(sorted(list(cliques)[0]))
    print(x)

if __name__ == '__main__':
    main(sys.argv)
