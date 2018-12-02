#!/usr/bin/env python3

import sys
from collections import defaultdict

def count(s, k):
    x = defaultdict(int)
    for c in s:
        x[c] += 1
    return len([a for a in x.values() if a == k])


def main(args):
    data = [s.strip() for s in sys.stdin]
    a = len([x for x in data if count(x, 2)])
    b = len([x for x in data if count(x, 3)])
    print(a, b, a*b)

if __name__ == '__main__':
    sys.exit(main(sys.argv))
