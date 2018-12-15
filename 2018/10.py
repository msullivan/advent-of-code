#!/usr/bin/env python3

from collections import defaultdict
import sys
import re

def extract(s):
    return [int(x) for x in re.findall(r'-?\d+', s)]

def main(args):
    data = [extract(s.strip()) for s in sys.stdin]
    # This is a pretty silly abuse of complex numbers.
    data = [(complex(a, b), complex(c, d)) for a, b, c, d in data]
    xs, vs = zip(*data)
    xs = list(xs)

    # Just look to see when they start getting further apart.
    nlast = 100000000000000000000
    for i in range(20000):
        nxs = xs[:]
        for j in range(len(xs)):
            nxs[j] += vs[j]

        center = sum(nxs) / len(nxs)
        total_distance = sum(abs(x - center) for x in nxs)
        print(i, center, total_distance)
        if total_distance > nlast:
            break

        xs = nxs
        nlast = total_distance

    poses = [(int(x.real), int(x.imag)) for x in xs]
    xxs, yxs = zip(*poses)
    poses = set(poses)
    for y in range(min(yxs), max(yxs)+1):
        s = ""
        for x in range(min(xxs), max(xxs)+1):
            c = '*' if (x, y) in poses else ' '
            s += c
        print(s)


if __name__ == '__main__':
    sys.exit(main(sys.argv))
