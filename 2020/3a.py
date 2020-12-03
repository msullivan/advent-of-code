#!/usr/bin/env python3

import sys

def main(args):
    data = [s.strip() for s in sys.stdin]

    x = 0
    y = 0
    n = len(data[0])
    ts = 0
    while y < len(data):
        if data[y][x % n] == '#':
            ts += 1
        x += 3
        y += 1

    print(ts)


if __name__ == '__main__':
    sys.exit(main(sys.argv))
