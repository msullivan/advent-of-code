#!/usr/bin/env python3

import sys
import re

def game(d1, d2):
    seen = set()

    while d1 and d2:
        if (d1, d2) in seen:
            return True, d1, d2
        seen.add((d1, d2))

        x1, d1 = d1[0], d1[1:]
        x2, d2 = d2[0], d2[1:]

        if len(d1) >= x1 and len(d2) >= x2:
            p1w, _, _ = game(d1[:x1], d2[:x2])
        else:
            p1w = x1 > x2

        if p1w:
            d1 = d1 + (x1, x2)
        else:
            d2 = d2 + (x2, x1)

    return bool(d1), d1, d2


def main(args):
    data = [x.strip().split('\n') for x in sys.stdin.read().split('\n\n')]
    d1 = tuple([int(x) for x in data[0][1:]])
    d2 = tuple([int(x) for x in data[1][1:]])

    p1w, d1, d2 = game(d1, d2)

    print(d1, d2)
    xs = list(reversed(d1 + d2))
    s = 0
    for i, x in enumerate(xs):
        s += (i+1)*x

    print(s)

if __name__ == '__main__':
    sys.exit(main(sys.argv))
