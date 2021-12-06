#!/usr/bin/env python3

import sys

from collections import Counter
import re

def extract(s, pos=False):
    p = '' if pos else '-?'
    return [int(x) for x in re.findall(fr'{p}\d+', s)]


def main(args):
    data = [s.strip() for s in sys.stdin]
    data = extract(data[0])

    cs = Counter(data)

    for n in range(256):
        ncs = Counter()
        for i in range(9):
            if i == 0:
                ncs[6] += cs[i]
                ncs[8] += cs[i]
            else:
                ncs[i-1] += cs[i]
        cs = ncs
        if n == 79:
            print(sum(cs.values()))  # part A

    print(sum(cs.values()))

if __name__ == '__main__':
    sys.exit(main(sys.argv))
