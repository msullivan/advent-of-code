#!/usr/bin/env python3

# in case anybody need a sub ms python solution
# not counting interpreter startup or imports :P
# sigh.

import sys
import re

def extract(s):
    return [int(x) for x in re.findall(r'(-?\d+).?', s)]


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

    n = 1
    while True:
        if passes(time, dist, n):
            break
        n *= 2

    good = n

    while True:
        if not passes(time, dist, n):
            break
        n *= 2

    bad = n

    lo = good // 2
    hi = good
    while lo < hi:
        mid = (lo + hi) // 2
        n = mid
        if passes(time, dist, n):
            hi = mid
        else:
            lo = mid + 1

    bot = lo

    lo = good
    hi = bad
    while lo < hi:
        mid = (lo + hi) // 2
        n = mid
        if passes(time, dist, n):
            lo = mid + 1
        else:
            hi = mid

    print(lo - bot)

if __name__ == '__main__':
    main(sys.argv)
