#!/usr/bin/env python3

import sys
from collections import defaultdict, deque
import math
import itertools

# I didn't actually use this when solving but maybe I should have!

def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    data = [s.rstrip('\n') for s in file]


    inputs = defaultdict(list)
    nodes = {}

    for line in data:
        l, r = line.split(' -> ')
        outs = r.split(', ')

        c, n = l[0], l[1:]
        nodes[n] = (c, outs)
        for out in outs:
            inputs[out].append(n)

    print('digraph nodes {')
    print('rankdir="LR"')
    for node, (typ, _) in nodes.items():
        print(f'{node} [label="{typ}{node}"]')

    for node, (typ, outs) in nodes.items():
        for out in outs:
            print(f'{node} -> {out}')

    print('}')

if __name__ == '__main__':
    main(sys.argv)
