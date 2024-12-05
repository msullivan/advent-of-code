#!/usr/bin/env python3

import sys
from collections import defaultdict, Counter, deque
from parse import parse
import re
import math
import functools

def extract(s):
    return [int(x) for x in re.findall(r'(-?\d+).?', s)]

def vadd(v1, v2):
    return tuple([x + y for x, y in zip(v1, v2)])

def ichr(i):
    return chr(ord('a') + i)

def iord(c):
    return ord(c.lower()) - ord('a')

def optidx(d, opt=max, nth=0):
    if not isinstance(d, dict):
        d = dict(enumerate(d))
    rv = opt(d.values())
    return [i for i, v in d.items() if v == rv][nth], rv

LETTERS = "abcdefghijklmnopqrstuvwxyz"

UP, RIGHT, DOWN, LEFT = VDIRS = (0, -1), (1, 0), (0, 1), (-1, 0),
DIRS = {'N': UP, 'E': RIGHT, 'S': DOWN, 'W': LEFT }
ALL_DIRS = [(x, y) for x in [-1,0,1] for y in [-1,0,1] if not x == y == 0]

def turn(v, d='left'):
    n = -1 if d == 'left' else 1
    return VDIRS[(VDIRS.index(v) + n) % len(VDIRS)]


##############################

def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    data = [x.rstrip('\n').split('\n') for x in file.read().split('\n\n')]
    # data = [int(s.rstrip('\n')) for s in file]
    # data = [s.rstrip('\n') for s in file]

    print(data[0])
    print(data[1])

    deps = {}
    for x in data[0]:
        pre, post = extract(x)
        deps.setdefault(post, []).append(pre)

    def compare(x, y):
        if x == y:
            return 0
        elif y in deps.get(x, []):
            return -1
        else:
            return 1

    s = 0
    s2 = 0
    for line in data[1]:
        nums = extract(line)
        seen = set()
        print(nums)
        ok = True
        for num in nums:
            for other in deps.get(num, []):
                if other in nums and other not in seen:
                    print('!', other)
                    ok = False
            seen.add(num)
        if ok:
            print('OK', nums, nums[len(nums)//2 + 1])
            s += nums[len(nums)//2]

        if not ok:
            nums2 = sorted(nums, key=functools.cmp_to_key(compare))
            s2 += nums2[len(nums)//2]


    print(s)
    print(s2)


if __name__ == '__main__':
    main(sys.argv)
