#!/usr/bin/env python3

import sys

def lcheck(x):
    for i in range(1, len(x)):
        start = x[:i]
        end = x[i:]
        if len(start) < len(end):
            if start == end[:len(start)][::-1]:
                return i
        else:
            if start[-len(end):] == end[::-1]:
                return i


def check(x):
    # horiz
    if n := lcheck(x):
        return n * 100

    x = [list(c) for c in zip(*x)]
    if n := lcheck(x):
        return n


def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    data = [x.rstrip('\n').split('\n') for x in file.read().split('\n\n')]

    sum = 0
    for x in data:
        v = check(x)
        # print('\n'.join(x))
        # print(v)
        sum += v


    print(sum)

if __name__ == '__main__':
    main(sys.argv)
