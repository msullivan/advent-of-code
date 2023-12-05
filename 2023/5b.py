#!/usr/bin/env python3

import sys
import re

def extract(s):
    return [int(x) for x in re.findall(r'(-?\d+).?', s)]


def get_breaks(m):
    b = set()
    for d, s, n in m:
        # b.update({s-1, s, s+n, s+n-1})  # ???
        b.update({s-1, s+n-1})  # ???

    return sorted(b)


def break_range(lo, hi, breaks):
    ranges = []
    for b in breaks:
        if lo < b < hi:  # <=?
            ranges.append((lo, b))
            lo = b + 1

    if lo < hi:
        ranges.append((lo, hi))
    return ranges


def lookup(m, i):
    for d, s, n in m:
        if s <= i < s + n:
            return d + (i - s)
    return i


def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    data = [x.rstrip('\n').split('\n') for x in file.read().split('\n\n')]
    seeds = extract(data[0][0])
    maps = []
    for lines in data[1:]:
        print(lines)
        m = [extract(s) for s in lines[1:] if s]
        maps.append(m)

    iranges = []
    i = 0
    while i < len(seeds):
        iranges.append((seeds[i], seeds[i]+seeds[i+1]))
        i += 2

    nums = []
    for irange in iranges:
        rs = [irange]
        for m in maps:
            breaks = get_breaks(m)
            ir2 = [x for lo, hi in rs for x in break_range(lo, hi, breaks)]
            rsi = rs
            rs = [(lookup(m, x), lookup(m, y)) for x, y in ir2]
            print(rsi, "->", rs)
        nums.extend(rs)

    print(nums)
    print(min(x for x, y in nums))

if __name__ == '__main__':
    main(sys.argv)
