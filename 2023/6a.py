#!/usr/bin/env python3

import sys
import re

def extract(s):
    return [int(x) for x in re.findall(r'(-?\d+).?', s)]


def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    data = [s.rstrip('\n') for s in file]

    # How I should have done part 2
    # data[0] = data[0].replace(' ', '')
    # data[1] = data[1].replace(' ', '')

    times = extract(data[0])
    dists = extract(data[1])

    ans = 1
    for time, dist in zip(times, dists):
        n = 0
        for i in range(time-1):
            traved = i * (time-i)
            if traved > dist:
                n += 1
        ans *= n

    print(ans)

if __name__ == '__main__':
    main(sys.argv)
