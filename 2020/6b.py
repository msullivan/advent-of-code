#!/usr/bin/env python3

import sys
import re

def extract(s):
    return [int(x) for x in re.findall(r'-?\d+', s)]


def main(args):
    data = [x.split('\n') for x in sys.stdin.read().split('\n\n')]

    total = 0
    letters = "abcdefghijklmnopqrstuvwxyz"

    for group in data:
        seen = set(letters)
        for person in group:
            seen = seen & set(person)

        total += len(seen)

    print(total)

if __name__ == '__main__':
    sys.exit(main(sys.argv))
