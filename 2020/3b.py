#!/usr/bin/env python3

import sys

def main(args):
    data = [s.strip() for s in sys.stdin]

    things = [(1,1), (3,1), (5,1), (7,1), (1,2)]

    res = 1
    for dx, dy in things:
        x = 0
        y = 0
        n = len(data[0])
        ts = 0
        while y < len(data):
            if data[y][x % n] == '#':
                ts += 1
            x += dx
            y += dy

        res *= ts

    print(res)


if __name__ == '__main__':
    sys.exit(main(sys.argv))
