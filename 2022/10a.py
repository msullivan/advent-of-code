#!/usr/bin/env python3

import sys
import re

def extract(s):
    return [int(x) for x in re.findall(r'(-?\d+).?', s)]

def main(args):
    data = [s.rstrip('\n') for s in sys.stdin]

    ns = [20, 60, 100, 140, 180, 220]
    X = 1
    last = None
    strength = 0
    cycle = 1
    for i, line in enumerate(data):
        if cycle in ns:
            strength += cycle * X
        cycle += 1

        if not line.startswith('addx'):
            continue

        if cycle in ns:
            strength += cycle * X
        cycle += 1

        n = extract(line)[0]
        X += n


    print(strength)

if __name__ == '__main__':
    main(sys.argv)
