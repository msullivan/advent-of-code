#!/usr/bin/env python3

import sys

def main(args):
    offs = [s.strip() for s in sys.stdin]
    banks = list(map(int, offs[0].split("\t")))
    seen = set()

    n = 0
    while True:
        if tuple(banks) in seen:
            break
        seen.add(tuple(banks))

        m = max(banks)
        i = banks.index(m)
        banks[i] = 0
        for j in range(m):
            banks[(i+1+j) % len(banks)] += 1
        n += 1

    print(n)

    start = tuple(banks)
    n = 0
    while True:
        m = max(banks)
        i = banks.index(m)
        banks[i] = 0
        for j in range(m):
            banks[(i+1+j) % len(banks)] += 1
        n += 1
        if tuple(banks) == start:
            break
    print(n)


if __name__ == '__main__':
    sys.exit(main(sys.argv))
