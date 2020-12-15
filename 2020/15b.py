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

    counts = defaultdict(list)
    t = 0
    for x in data:
        counts[x] += [t]

        last = x
        t += 1

    while t < 30000000:
        if t % 1000 == 0: print(t)
        ls = counts[last]
        if len(ls) == 1:
            num = 0
        else:
            num = ls[-1] - ls[-2]
        counts[num] += [t]
        counts[num] = counts[num][-2:]
        last = num
        t += 1

    # print(nums)
    print(last)

if __name__ == '__main__':
    sys.exit(main(sys.argv))
