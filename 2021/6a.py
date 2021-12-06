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

    for _ in range(80):
        print(len(data))
        for i in range(len(data)):
            if data[i] == 0:
                data[i] = 6
                data.append(8)
            else:
                data[i] -= 1

    print(len(data))

if __name__ == '__main__':
    sys.exit(main(sys.argv))
