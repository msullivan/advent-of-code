#!/usr/bin/env python3

# in case anybody need a sub ms python solution
# not counting interpreter startup or imports :P
# sigh.

import sys
import re

def extract(s):
    return [int(x) for x in re.findall(r'(-?\d+).?', s)]


def binary_search(pred, lo, hi=None):
    """Finds the first n in [lo, hi) such that pred(n) holds.

    hi == None -> infty
    """
    assert not pred(lo)

    if hi is None:
        hi = max(lo, 1)
        while not pred(hi):
            hi *= 2

    assert pred(hi)

    while lo < hi:
        mid = (lo + hi) // 2
        if pred(mid):
            hi = mid
        else:
            lo = mid + 1

    return lo


def passes(time, dist, i):
    traved = i * (time-i)
    return traved > dist


def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    data = [s.rstrip('\n') for s in file]
    data[0] = data[0].replace(' ', '')
    data[1] = data[1].replace(' ', '')

    time = extract(data[0])[0]
    dist = extract(data[1])[0]

    first = binary_search((lambda n: passes(time, dist, n)), 1)
    last = binary_search((lambda n: not passes(time, dist, n)), first)

    print(last - first)

if __name__ == '__main__':
    main(sys.argv)
