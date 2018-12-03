#!/usr/bin/env python3

from collections import defaultdict
import sys
import re

def extract(s):
    return [int(x) for x in re.findall(r'-?\d+', s)]

def main(args):
    data = [extract(s.strip()) for s in sys.stdin]
    map = defaultdict(set)
    doubled = 0

    ok = set(x[0] for x in data)
    for id, x, y, l, w in data:
        for i in range(l):
            for j in range(w):
                c = x + i, y + j
                map[c].add(id)
                if len(map[c]) > 1:
                    ok -= map[c]
    print(list(ok)[0])




if __name__ == '__main__':
    sys.exit(main(sys.argv))
