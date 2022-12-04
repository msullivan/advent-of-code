#!/usr/bin/env python3

import sys
import re

def main(args):
    data = [s.strip() for s in sys.stdin]

    cnt = 0
    for line in data:
        a1, a2, b1, b2 = extract(line)

        if a1 <= b1 and b1 <= a2:
            cnt += 1
        elif b1 <= a1 and a1 <= b2:
            cnt += 1

    print(cnt)

if __name__ == '__main__':
    main(sys.argv)
