#!/usr/bin/env python3

import sys
import re
import time
import math
from typing import Set


def extract(s):
    return [int(x) for x in re.findall(r'-?\d+', s)]

def add(v1, v2):
    return tuple(x + y for x, y in zip(v1, v2))

def sub(v1, v2):
    return tuple(x - y for x, y in zip(v1, v2))

def gravity(r1, r2):
    return tuple(
        1 if x < y else 0 if x == y else -1
        for x, y in zip(r1, r2)
    )

def energy(r):
    return sum(abs(x) for x in r)

def lcm(a, b):
    return a*b // math.gcd(a, b)

def main(args):
    data = [s.strip() for s in sys.stdin]
    xs = [tuple(extract(s)) for s in data]
    vs = [(0, 0, 0) for _ in xs]

    seen = [set() for _ in xs]
    times = [0] * 3

    #for i in range(1000):
    count = 0
    while not all(x for x in times):
        #print(xs)
        for i in range(len(xs)):
            for j in range(len(xs)):
                vs[i] = add(vs[i], gravity(xs[i], xs[j]))

        for i in range(len(xs)):
            xs[i] = add(xs[i], vs[i])

        re_xd = [tuple(x[i] for x in xs) for i in range(3)]
        re_vd = [tuple(v[i] for v in vs) for i in range(3)]
        for i in range(3):
            if (re_xd[i], re_vd[i]) in seen[i] and not times[i]:
                print("YO", i)
                times[i] = count
                print(times)
            seen[i].add((re_xd[i], re_vd[i]))

        count += 1

    # For the solution I just plugged the numbers that got printed
    # into LCM on wolfram alpha but I might as well make it really
    # work
    a, b, c = times
    print((math.gcd(math.gcd(a, b), c)))
    repeat_time = lcm(lcm(a, b), c)
    print(repeat_time)


if __name__ == '__main__':
    main(sys.argv)
