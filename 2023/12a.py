#!/usr/bin/env python3

import sys
import re

def extract(s):
    return [int(x) for x in re.findall(r'(-?\d+).?', s)]

def check(line, cnts):
    if '?' not in line:
        ls = [len(x) for x in line.split('.') if '.' not in x and len(x)]
        return ls == cnts

    return (
        check(line.replace('?', '.', 1), cnts)
        + check(line.replace('?', '#', 1), cnts)
    )

def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    data = [s.rstrip('\n') for s in file]

    sum = 0
    for l in data:
        l, nums = l.split(' ')
        nums = extract(nums)
        sum += check(l, nums)

    print(sum)

if __name__ == '__main__':
    main(sys.argv)
