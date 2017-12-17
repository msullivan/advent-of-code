#!/usr/bin/env python3

import sys

def main(args):
    #cnt = 2017
    cnt = 50000000
    n = 3
    n = 345
    size = 0
    buf = [0]
    pos = 0

    at_1 = None

    for i in range(cnt):
        pos = (pos + n) % (i+1)
        if pos == 0:
            at_1 = i+1
        pos += 1

    print(at_1)

if __name__ == '__main__':
    sys.exit(main(sys.argv))
