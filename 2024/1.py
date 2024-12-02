#!/usr/bin/env python3

import sys
import re
from collections import Counter

def extract(s):
    return [int(x) for x in re.findall(r'(-?\d+).?', s)]


def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    data = [extract(s.rstrip('\n')) for s in file]

    # ... I couldn't remember the unzip trick
    # xs, ys = [], []
    # for x, y in data:
    #     xs.append(x)
    #     ys.append(y)
    xs, ys = zip(*data)

    xs = sorted(xs)
    ys = sorted(ys)

    asdf = Counter(ys)

    print(sum(abs(x-y) for x, y in zip(xs, ys)))
    print(sum(x * asdf[x] for x in xs))


if __name__ == '__main__':
    main(sys.argv)
