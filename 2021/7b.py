#!/usr/bin/env python3

import sys
import re

def extract(s, pos=False):
    p = '' if pos else '-?'
    return [int(x) for x in re.findall(fr'{p}\d+', s)]

def main(args):
    data = extract(sys.stdin.read())

    spots = {}
    for i in range(0, max(data)+1):
        x = 0
        for d in data:
            di = abs(i - d)
            z = di*(di+1)//2
            x += z
        spots[i] = x

    print(min(spots.values()))

if __name__ == '__main__':
    main(sys.argv)
