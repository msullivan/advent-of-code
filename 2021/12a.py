#!/usr/bin/env python3

import sys

from collections import defaultdict

def go(m, paths, path, u):
    if path in paths:
        return
    paths.add(path)
    if u == 'end':
        return

    for v in m[u]:
        if v.islower() and v in path:
            continue
        go(m, paths, path + (v,), v)


def main(args):
    data = [s.strip() for s in sys.stdin]

    m = defaultdict(set)
    for line in data:
        u, v = line.split('-')
        m[u].add(v)
        m[v].add(u)

    paths = set()

    go(m, paths, ('start',), 'start')
    rpaths = {x for x in paths if x and x[-1] == 'end'}

    print(len(rpaths))


if __name__ == '__main__':
    main(sys.argv)
