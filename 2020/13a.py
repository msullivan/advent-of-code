#!/usr/bin/env python3

import sys
import re

def extract(s):
    return [int(x) for x in re.findall(r'-?\d+', s)]


def main(args):
    # data = [x.split('\n') for x in sys.stdin.read().split('\n\n')]
    data = [s.strip() for s in sys.stdin]
    early = int(data[0])
    stamps = [int(x) if x != "x" else None for x in data[1].split(",")]

    i = early
    while True:
        matches = [x for x in stamps if x and i % x == 0]
        print("a", matches)
        if matches:
            break
        i += 1

    print(matches[0])
    print((i - early) * matches[0])

if __name__ == '__main__':
    sys.exit(main(sys.argv))
