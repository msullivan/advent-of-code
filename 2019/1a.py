#!/usr/bin/env python3

import sys

def main(args):
    data = [int(s.strip()) for s in sys.stdin]
    total = 0
    for x in data:
        total += (x // 3) - 2

    print(total)


if __name__ == '__main__':
    sys.exit(main(sys.argv))
