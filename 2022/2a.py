#!/usr/bin/env python3

import sys

def main(args):
    data = [s.strip().split(' ') for s in sys.stdin]

    # This... was not a good way to do this, but I decided to
    # prioritize typing over thinking.
    results = {
        "AX": 3,
        "AY": 6,
        "AZ": 0,
        "BX": 0,
        "BY": 3,
        "BZ": 6,
        "CX": 6,
        "CY": 0,
        "CZ": 3,
    }

    score = 0
    for a, b in data:
        me = "XYZ".index(b) + 1
        res = results[a+b]
        score += me + res

    print(score)

if __name__ == '__main__':
    main(sys.argv)
