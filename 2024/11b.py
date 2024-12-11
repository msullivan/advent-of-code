#!/usr/bin/env python3

import sys
from collections import defaultdict
import re

def extract(s):
    return [int(x) for x in re.findall(r'(-?\d+).?', s)]


def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    data = [s.rstrip('\n') for s in file]

    l = extract(data[0])

    m = defaultdict(int)
    for x in l:
        m[x] += 1

    for i in range(75):
        nm = defaultdict(int)
        for x, cnt in m.items():
            sx = str(x)
            if x == 0:
                nm[1] += cnt
            elif len(sx) % 2 == 0:
                nm[int(sx[:len(sx)//2])] += cnt
                nm[int(sx[len(sx)//2:])] += cnt
            else:
                nm[x*2024] += cnt

        m = nm
        if i == 25-1:
            p1 = sum(m.values())

    print(p1)
    print(sum(m.values()))

if __name__ == '__main__':
    main(sys.argv)
