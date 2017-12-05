#!/usr/bin/env python3

import sys

def main(args):
    nub = [s.strip() for s in sys.stdin][0]
    nub2 = nub + nub[0]
    n = 0

    for i in range(len(nub)):
        if nub2[i] == nub2[i+1]:
            n += int(nub2[i])

    print(n)

    n = 0
    l = len(nub)
    h = l//2
    for i in range(l):
        if nub[i] == nub[(i+h) % l]:
            n += int(nub[i])

    print(n)


if __name__ == '__main__':
    sys.exit(main(sys.argv))
