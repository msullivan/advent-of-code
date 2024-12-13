#!/usr/bin/env python3

import sys
from collections import defaultdict, Counter, deque
from parse import parse
import re
import math
import itertools
import heapq

def extract(s):
    return [int(x) for x in re.findall(r'(-?\d+).?', s)]


def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    data = [x.rstrip('\n').split('\n') for x in file.read().split('\n\n')]

    ans = 0
    for group in data:
        xa, ya = extract(group[0])
        xb, yb = extract(group[1])
        xt, yt = extract(group[2])
        xt += 10000000000000
        yt += 10000000000000

        # A = ((tx - ty) - b*(xb - yb)) / (xa - ya)

        xbp = xb * ya
        xtp = xt * ya
        ybp = yb * xa
        ytp = yt * xa
        if (xtp - ytp) == (xbp - ybp):
            print("FUCK", (xa, ya, xb, yb, xt, yt))
            continue  # ???

        B = (xtp - ytp) / (xbp - ybp)
        A = (xt - B * xb) / xa

        # print(xa, ya, xb, yb, xt, yt)
        # print(A, B)
        if int(A) == A and int(B) == B and A > 0 and B > 0:
            assert A*xa + B*xb == xt
            assert A*ya + B*yb == yt

            tokens = A*3 + B
            ans += tokens

    print(int(ans))


if __name__ == '__main__':
    main(sys.argv)
