#!/usr/bin/env python3


from collections import defaultdict
import sys
import re

def extract(s):
    return [int(x) for x in re.findall(r'-?\d+', s)]


def main(args):
    # data = [x.split('\n') for x in sys.stdin.read().split('\n\n')]
    data = [s.strip() for s in sys.stdin]
    data = [int(x) for x in data[0].split(",")]

    times = {}
    counts = defaultdict(list)
    t = 0
    nums = []
    for x in data:
        times[x] = t
        counts[x] += [t]

        nums += [x]
        t += 1

    print(nums)
    print(times)
    while t < 2020:
        last = nums[-1]
        ls = counts[last]
        if len(ls) == 1:
            num = 0
        else:
            num = ls[-1] - ls[-2]
        counts[num] += [t]
        times[num]=t
        nums += [num]
        t += 1

    print(nums)
    print(nums[-1])

if __name__ == '__main__':
    sys.exit(main(sys.argv))
