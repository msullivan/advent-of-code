#!/usr/bin/env python3

import sys

# From https://rosettacode.org/wiki/Chinese_remainder_theorem#Python_3.6
# But tweaked to use python3.8 pow
from functools import reduce
def chinese_remainder(n, a):
    sum = 0
    prod = reduce(lambda a, b: a*b, n)
    for n_i, a_i in zip(n, a):
        p = prod // n_i
        sum += a_i * pow(p, -1, n_i) * p
    return sum % prod


def main(args):
    data = [s.strip() for s in sys.stdin]
    early = int(data[0])
    stamps = [int(x) if x != "x" else None for x in data[1].split(",")]

    i = early
    while True:
        matches = [x for x in stamps if x and i % x == 0]
        if matches:
            break
        i += 1

    print((i - early) * matches[0])

    bcrap = [(x,((x-i)%x)) for i,x in enumerate(stamps) if x]
    ns, bs = zip(*bcrap)
    # print(bs, ns)
    crt = chinese_remainder(ns, bs)
    print(crt)


if __name__ == '__main__':
    sys.exit(main(sys.argv))
