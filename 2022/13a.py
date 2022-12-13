#!/usr/bin/env python3

import sys
import ast

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
    else:
        return cmp(x1, [x2])


def main(args):
    data = [x.rstrip('\n').split('\n') for x in sys.stdin.read().split('\n\n')]

    score = 0
    for i, (l1, l2) in enumerate(data):
        l1 = ast.literal_eval(l1)
        l2 = ast.literal_eval(l2)
        n = cmp(l1, l2)
        if n < 0:
            score += (i + 1)

    print(score)

if __name__ == '__main__':
    main(sys.argv)
