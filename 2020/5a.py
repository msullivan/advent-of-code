#!/usr/bin/env python3

import sys

def main(args):
    data = [s.strip() for s in sys.stdin]

    maxseen = 0
    seen = set()
    for row in data:
        lo, hi = 0, 128
        for c in row[:7]:
            mid = (lo+hi)//2
            if c == 'F':
                hi = mid
            else:
                lo = mid
        rown = lo

        lo, hi = 0, 8
        for c in row[7:]:
            mid = (lo+hi)//2
            if c == 'L':
                hi = mid
            else:
                lo = mid

        seat = lo
        id = rown*8+seat
        maxseen = max(maxseen, id)
        seen.add(id)

    print(maxseen)


    # print(data)

if __name__ == '__main__':
    sys.exit(main(sys.argv))
