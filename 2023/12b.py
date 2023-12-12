#!/usr/bin/env python3

import sys
import re
import functools


def extract(s):
    return [int(x) for x in re.findall(r'(-?\d+).?', s)]

# @functools.cache
def check(line, cnts):
    v = _check(line, cnts)
    # print(line, cnts, '->', v)
    return v

@functools.cache
def _check(line, cnts):
    if not line:
        if not cnts:
            return 1
        else:
            return 0
    if line[0] == '.':
        return check(line[1:], cnts)
    if line[0] == '#':
        if not cnts:
            return 0
        if '.' in line[:cnts[0]]:
            return 0
        if line[cnts[0]] == '#':
            return 0
        return check(line[cnts[0]+1:], cnts[1:])
    return (
        check('.' + line[1:], cnts)
        + check('#' + line[1:], cnts)
    )

def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    data = [s.rstrip('\n') for s in file]

    sum = 0
    i = 0
    for l in data:
        i += 1

        l, nums = l.split(' ')
        nums = tuple(extract(nums))

        l = "?".join([l]*5)
        nums *= 5
        l += '.'
        v = check(l, nums)
        print('=============', i-1, v)
        sum += v

    print(sum)

if __name__ == '__main__':
    main(sys.argv)
