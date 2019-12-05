#!/usr/bin/env python3

import sys

DIRS = {"R": (1, 0), "L": (-1, 0), "U": (0, 1), "D": (0, -1)}

def trace(wire):
    x, y = 0, 0
    for s in wire:
        d = s[0]
        n = int(s[1:])
        dx, dy = DIRS[d]
        for i in range(n):
            x += dx
            y += dy
            yield x, y

def main(args):
    data = [s.strip() for s in sys.stdin]
    wire1 = [x for x in data[0].split(",")]
    wire2 = [x for x in data[1].split(",")]

    spots = set(trace(wire1)) & set(trace(wire2))
    print(min([abs(x)+abs(y) for x, y in spots]))

if __name__ == '__main__':
    sys.exit(main(sys.argv))
