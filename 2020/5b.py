#!/usr/bin/env python3

# I was pretty sure that the code was just straightforward binary but
# also I was tired and not firing on all cylinders so I figured I'd
# just mindlessly type out the directions and hope that would be fast
# enough. It almost was: 103 on **. Sigh. Should have just used my
# brain.

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
    for x in range(maxseen):
        if x not in seen and x+1 in seen and x-1 in seen:
            print(x)



    # print(data)

if __name__ == '__main__':
    sys.exit(main(sys.argv))
