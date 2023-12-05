#!/usr/bin/env python3

import sys
import re

def extract(s):
    return [int(x) for x in re.findall(r'(-?\d+).?', s)]

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

    nums = []
    for seed in seeds:
        for m in maps:
            n = seed
            seed = lookup(m, seed)
            print(n, "->", seed)
            print(m)
        nums.append(seed)

    print(nums)
    print(min(nums))

if __name__ == '__main__':
    main(sys.argv)
