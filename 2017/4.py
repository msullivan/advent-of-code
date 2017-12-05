#!/usr/bin/env python3

import sys

def main(args):
    nubs = [s.strip() for s in sys.stdin]
    valid = 0

    for nub in nubs:
        words = nub.split(" ")
        swords = set(words)
        if len(words) == len(swords): valid +=1

    print(valid)

    valid = 0
    for nub in nubs:
        words = nub.split(" ")
        words = [tuple(sorted(w)) for w in words]
        swords = set(words)
        if len(words) == len(swords): valid +=1
    print(valid)

if __name__ == '__main__':
    sys.exit(main(sys.argv))
