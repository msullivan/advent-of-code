#!/usr/bin/env python3

import sys
from collections import defaultdict
import re

def extract(s):
    return [int(x) for x in re.findall(r'(-?\d+).?', s)]

def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    data = [s.rstrip('\n') for s in file]

    numbers = {}
    ops = {}

    # This is more complicated than needed.
    deps = defaultdict(list)
    for line in data:
        x, y = line.split(': ')
        nums = extract(line)
        if nums:
            numbers[x] = nums[0]
        else:
            a, op, b = y.split(' ')
            ops[x] = (a, op, b)
            deps[a].append(x)
            deps[b].append(x)

    wl = []
    for k in numbers:
        wl.extend(deps[k])

    while wl:
        x = wl.pop()
        if x in numbers:
            continue
        a, op, b = ops[x]
        if a not in numbers or b not in numbers:
            continue
        z = eval(f'int({numbers[a]} {op} {numbers[b]})')
        numbers[x] = z
        wl.extend(deps[x])

    print(numbers['root'])

if __name__ == '__main__':
    main(sys.argv)
