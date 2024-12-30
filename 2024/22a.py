#!/usr/bin/env python3

import sys

def compute(n, i):
    for _ in range(i):
        n = (n ^ (n * 64)) % 16777216
        n = (n ^ (n // 32)) % 16777216
        n = (n ^ (n * 2048)) % 16777216
    return n


def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    data = [int(s.rstrip('\n')) for s in file]

    print(sum(compute(n, 2000) for n in data))


if __name__ == '__main__':
    main(sys.argv)
