#!/usr/bin/env python3

import sys

def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    data = [s.rstrip('\n') for s in file]

    cols = set()
    rows = set()

    for y, l in enumerate(data):
        for x, c in enumerate(l):
            if c == '#':
                rows.add(y)
                cols.add(x)

    N = 1000000

    galaxies = []
    yreal = 0
    for y, r in enumerate(data):
        row = ""
        if y not in rows:
            yreal += N-1
        xreal = 0
        for x, c in enumerate(r):
            if x not in cols:
                xreal += N-1
            if c == '#':
                galaxies.append((xreal, yreal))
            xreal += 1
        yreal += 1

    sum = 0
    for i, (x1, y1) in enumerate(galaxies):
        for j, (x2, y2) in enumerate(galaxies[i+1:]):
            dst = abs(y2-y1) + abs(x2-x1)
            sum += dst

    print(sum)

if __name__ == '__main__':
    main(sys.argv)
