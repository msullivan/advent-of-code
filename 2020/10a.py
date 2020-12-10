#!/usr/bin/env python3

# I really don't want to talk about it.

import sys
import re

def extract(s):
    return [int(x) for x in re.findall(r'-?\d+', s)]


def edges(jolts, v):
    # return [v+i for i in [-3,-2,-1,1,2,3] if v+i in jolts]
    return [v+i for i in [1,2,3] if v+i in jolts]

def search(jolts, v, tgt, seen):
    print(v, tgt)
    if v == tgt:
        return []
    # if v in seen:
    #     return None
    seen.add(v)
    for e in edges(jolts, v):
        x = search(jolts, e, tgt, seen)
        if x is not None:
            return [e] + x
    return None

def main(args):
    # data = [x.split('\n') for x in sys.stdin.read().split('\n\n')]
    data = set(int(s.strip()) for s in sys.stdin)
    tgt = max(data) + 3
    data.add(tgt)

    seen = set()
    x = search(data, 0, tgt, seen)
    print(x)

    assert len(seen) == len(data)
    i = 1
    d1 = 0
    d3 = 0
    x = [0] + x
    for i in range(1, len(x)):
        if x[i] - x[i-1] == 3:
            d3 += 1
        if x[i] - x[i-1] == 1:
            d1 += 1

    print(d1, d3)
    print(d1*d3)


if __name__ == '__main__':
    sys.exit(main(sys.argv))
