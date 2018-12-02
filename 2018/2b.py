#!/usr/bin/env python3

import sys
from collections import defaultdict

def count(s1, s2):
    return len([0 for x1, x2 in zip(s1, s2) if x1 != x2]) == 1

def main(args):
    data = [s.strip() for s in sys.stdin]
    for x in data:
        for y in data:
            if count(x, y):
                print("".join([x1 for x1, x2 in zip(x, y) if x1 == x2]))
                print(x, y)
                return

if __name__ == '__main__':
    sys.exit(main(sys.argv))
