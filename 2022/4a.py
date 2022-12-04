#!/usr/bin/env python3

import sys
import re

def extract(s):
    return [int(x) for x in re.findall(r'(-?\d+).?', s)]

def main(args):
    data = [s.strip() for s in sys.stdin]

    cnt = 0
    for line in data:
        a1, a2, b1, b2 = extract(line)
        if a1 <= b1 <= b2 <= a2:
            cnt += 1
        elif b1 <= a1 <= a2 <= b2:
            cnt += 1

    print(cnt)

if __name__ == '__main__':
    main(sys.argv)
