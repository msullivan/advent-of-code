#!/usr/bin/env python3

import sys
import re
import functools

def extract(s):
    return [int(x) for x in re.findall(r'-?\d+', s)]


def edges(jolts, v):
    # return [v+i for i in [-3,-2,-1,1,2,3] if v+i in jolts]
    return [v+i for i in [1,2,3] if v+i in jolts]

@functools.lru_cache()
def search(jolts, v, tgt):
    if v == tgt:
        return 1
    x = 0
    for e in edges(jolts, v):
        x += search(jolts, e, tgt)
    return x

def main(args):
    # data = [x.split('\n') for x in sys.stdin.read().split('\n\n')]
    data = set(int(s.strip()) for s in sys.stdin)
    tgt = max(data) + 3
    data.add(tgt)
    data = frozenset(data)

    x = search(data, 0, tgt)
    print(x)


if __name__ == '__main__':
    sys.exit(main(sys.argv))
