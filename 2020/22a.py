#!/usr/bin/env python3

import sys
import re

def extract(s):
    return [int(x) for x in re.findall(r'-?\d+', s)]


def main(args):
    data = [x.strip().split('\n') for x in sys.stdin.read().split('\n\n')]
    # data = [s.strip() for s in sys.stdin]
    d1 = [int(x) for x in data[0][1:]]
    d2 = [int(x) for x in data[1][1:]]

    while d1 and d2:
        x1 = d1.pop(0)
        x2 = d2.pop(0)
        if x1 > x2:
            d1.append(x1)
            d1.append(x2)
        else:
            d2.append(x2)
            d2.append(x1)

    print(d1, d2)
    xs = list(reversed(d1 + d2))
    s = 0
    for i, x in enumerate(xs):
        s += (i+1)*x

    print(s)

if __name__ == '__main__':
    sys.exit(main(sys.argv))
