#!/usr/bin/env python3

import sys

def main(args):
    nubs = [s.strip() for s in sys.stdin]
    n = 0
    m = 0

    for line in nubs:
        parts = line.split("\t")
        nums = [int(s) for s in parts if s]
        for x in nums:
            for y in nums:
                if x % y == 0 and x != y:
                    m += (x // y)

        n += (max(nums) - min(nums))
    print(n)
    print(m)


if __name__ == '__main__':
    sys.exit(main(sys.argv))
