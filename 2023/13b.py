#!/usr/bin/env python3

import sys


def lcheck(x, old):
    for i in range(1, len(x)):
        start = x[:i]
        end = x[i:]
        if len(start) < len(end):
            if start == end[:len(start)][::-1] and i != old:
                return i
        else:
            if start[-len(end):] == end[::-1] and i != old:
                return i


def check(x, old):
    # horiz
    if n := lcheck(x, old//100):
        return n * 100

    x = [list(c) for c in zip(*x)]
    if n := lcheck(x, old):
        return n

    return None

def other(x, old):
    x = [list(c) for c in x]
    for i in range(len(x)):
        for j in range(len(x[0])):
            c = x[i][j]
            x[i][j] = '#' if c == '.' else '.'
            if n := check(x, old):
                return n
            x[i][j] = c


def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    data = [x.rstrip('\n').split('\n') for x in file.read().split('\n\n')]

    sum = 0
    for x in data:
        old = check(x, -1)
        v = other(x, old)
        # print('\n'.join(x))
        sum += v


    print(sum)

if __name__ == '__main__':
    main(sys.argv)
