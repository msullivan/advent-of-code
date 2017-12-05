#!/usr/bin/env python3

import sys

def main(args):
    offs = [int(s.strip()) for s in sys.stdin]

    j = 0
    i = 0
    while i >= 0 and i < len(offs):
        off = offs[i]
        offs[i] += 1
        i += off
        j +=1
    print(j)

if __name__ == '__main__':
    sys.exit(main(sys.argv))
