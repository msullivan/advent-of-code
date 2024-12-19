#!/usr/bin/env python3

import sys
import functools


def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    data = [x.rstrip('\n').split('\n') for x in file.read().split('\n\n')]

    patterns = data[0][0].split(', ')
    lines = data[1]

    @functools.cache
    def pos(s, i):
        if i == len(s):
            return 1
        n = 0
        for pat in patterns:
            if pat == s[i:i+len(pat)] :
                n += pos(s, i+len(pat))
        return n

    vals = [pos(s, 0) for s in lines]

    print(sum(v > 0 for v in vals))
    print(sum(vals))


if __name__ == '__main__':
    main(sys.argv)
