#!/usr/bin/env python3

import sys
import re

def extract(s):
    return [int(x) for x in re.findall(r'(-?\d+).?', s)]


def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    data = [s.rstrip('\n') for s in file]

    pos = 50
    cnt = 0
    for line in data:
        m = -1 if line[0] == 'L' else 1
        n, = extract(line)

        # maths!  (original solution looped)
        npos = (pos + m * n)
        cnt += pos != 0 and npos <= 0
        cnt += abs(npos) // 100
        pos = npos % 100

    print(cnt)

if __name__ == '__main__':
    main(sys.argv)
