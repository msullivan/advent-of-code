#!/usr/bin/env python3

import sys

from collections import defaultdict, Counter

def cts(data):
    cs = Counter()
    for line in data:
        for i in range(len(line)):
            if line[i] == "1":
                cs[i] += 1
    n = len(data)
    zs = ["1" if cs[i]/n >= 0.5 else "0" for i in range(len(line))]
    ys = ["0" if cs[i]/n >= 0.5 else "1" for i in range(len(line))]
    return cs, zs, ys


def main(args):
    data = [s.strip() for s in sys.stdin]

    cs, zs, ys = cts(data)

    gamma = int("".join(zs), 2)
    eps = int("".join(ys), 2)
    print(gamma*eps)

    l = len(data[0])

    o2 = data
    for i in range(l):
        _, most, _ = cts(o2)
        o2 = [x for x in o2 if x[i] == most[i]]
        if len(o2) == 1:
            break
    print(o2)

    co2 = data
    for i in range(l):
        _, _, least = cts(co2)
        co2 = [x for x in co2 if x[i] == least[i]]
        if len(co2) == 1:
            break
    print(co2)

    o2v = int("".join([o2[0]]), 2)
    co2v = int("".join(co2[0]), 2)
    print(o2v, co2v)
    print(o2v*co2v)


if __name__ == '__main__':
    sys.exit(main(sys.argv))
