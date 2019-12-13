#!/usr/bin/env python3

import sys
import re
import time
from typing import Set


def extract(s):
    return [int(x) for x in re.findall(r'-?\d+', s)]

def add(v1, v2):
    return tuple(x + y for x, y in zip(v1, v2))

def gravity(r1, r2):
    return tuple(
        1 if x < y else 0 if x == y else -1
        for x, y in zip(r1, r2)
    )

def energy(r):
    return sum(abs(x) for x in r)


def main(args):
    data = [s.strip() for s in sys.stdin]
    xs = [tuple(extract(s)) for s in data]
    vs = [(0, 0, 0) for _ in xs]

    for i in range(1000):
        print(xs)
        for i in range(len(xs)):
            for j in range(len(xs)):
                vs[i] = add(vs[i], gravity(xs[i], xs[j]))

        for i in range(len(xs)):
            xs[i] = add(xs[i], vs[i])

    print(sum(energy(x)*energy(v) for x, v in zip(xs, vs)))



if __name__ == '__main__':
    main(sys.argv)
