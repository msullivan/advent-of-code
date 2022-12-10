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

    m = list('.' * (40*6))

    for i, line in enumerate(data):
        pos = (cycle-1)%40
        if abs(pos-X) <= 1:
            m[cycle-1] = '#'

        if cycle in ns:
            strength += cycle * X
            z = ns.index(cycle)


        cycle += 1

        if not line.startswith('addx'):
            continue

        pos = (cycle-1)%40
        if abs(pos-X) <= 1:
            m[cycle-1] = '#'

        if cycle in ns:
            strength += cycle * X
        cycle += 1

        n = extract(line)[0]
        X += n

    for r in range(6):
        for c in range(40):
            print(m[r*40+c], end='')
        print()

    print(strength)

if __name__ == '__main__':
    main(sys.argv)
