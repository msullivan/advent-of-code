#!/usr/bin/env python3

import sys

import functools
import json

def cmp(x1, x2):
    if isinstance(x1, int) and isinstance(x2, int):
        return x1 - x2
    elif isinstance(x1, list) and isinstance(x2, list):
        for y1, y2 in zip(x1, x2):
            n = cmp(y1, y2)
            if n != 0:
                return n
        return len(x1) - len(x2)
    elif isinstance(x1, int):
        return cmp([x1], x2)
    elif isinstance(x2, int):
        return cmp(x1, [x2])
    else:
        raise AssertionError('uh')


def main(args):
    data = [x.rstrip('\n').split('\n') for x in sys.stdin.read().split('\n\n')]

    all = []
    score = 0
    for i, (l1, l2) in enumerate(data):
        l1 = json.loads(l1)
        l2 = json.loads(l2)
        n = cmp(l1, l2)
        if n < 0:
            score += (i + 1)
        all.extend([l1, l2])

    print(score)

    all.append([2])
    all.append([6])

    new = sorted(all, key=functools.cmp_to_key(cmp))
    i1 = new.index([2])
    i2 = new.index([6])
    print((i1+1)*(i2+1))


if __name__ == '__main__':
    main(sys.argv)
