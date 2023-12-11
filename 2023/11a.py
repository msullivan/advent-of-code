#!/usr/bin/env python3

import sys

def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    data = [s.rstrip('\n') for s in file]

    cols = set()
    rows = set()
    galaxies = set()

    for y, l in enumerate(data):
        for x, c in enumerate(l):
            if c == '#':
                galaxies.add((x, y))
                rows.add(y)
                cols.add(x)

    new = []
    for i, x in enumerate(data):
        new.append(x)
        if '#' not in x:
            new.append(x)
    data = new

    new2 = []
    for y, r in enumerate(data):
        row = ""
        for x, c in enumerate(r):
            row += c
            if x not in cols:
                row += c
        new2.append(row)

    galaxies = []

    for y, l in enumerate(new2):
        for x, c in enumerate(l):
            if c == '#':
                galaxies.append((x, y))
                rows.add(y)
                cols.add(x)

    print(galaxies)

    galaxies = list(galaxies)
    sum = 0
    n = 0
    for i, (x1, y1) in enumerate(galaxies):
        for j, (x2, y2) in enumerate(galaxies[i+1:]):
            j += i+1
            n += 1
            dst = abs(y2-y1) + abs(x2-x1)
            print(i+1, j+1, dst)
            sum += dst

    print(n)
    print(sum)

if __name__ == '__main__':
    main(sys.argv)
