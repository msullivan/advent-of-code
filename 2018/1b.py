#!/usr/bin/env python3

import sys

def main(args):
    data = [s.strip() for s in sys.stdin]
    f = 0
    seen = set([0])
    while True:
        for x in data:
            f += int(x)
            if f in seen:
                print(f)
                sys.exit(0)
            seen.add(f)

if __name__ == '__main__':
    sys.exit(main(sys.argv))
