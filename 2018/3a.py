#!/usr/bin/env python3

from collections import defaultdict
import sys
import re

def extract(s):
    return [int(x) for x in re.findall(r'-?\d+', s)]

def main(args):
    data = [extract(s.strip()) for s in sys.stdin]
    map = defaultdict(int)
    doubled = 0

    for _, x, y, l, w in data:
        for i in range(l):
            for j in range(w):
                c = x + i, y + j
                if map[c] == 1: doubled += 1
                map[c] += 1
    print(doubled)




if __name__ == '__main__':
    sys.exit(main(sys.argv))
