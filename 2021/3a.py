#!/usr/bin/env python3

import sys

from collections import defaultdict, Counter

def main(args):
    data = [s.strip() for s in sys.stdin]

    cs = Counter()
    for line in data:
        for i in range(len(line)):
            if line[i] == "1":
                cs[i] += 1

    n = len(data)
    zs = ["1" if cs[i]/n > 0.5 else "0" for i in range(len(line))]
    ys = ["0" if cs[i]/n > 0.5 else "1" for i in range(len(line))]
    gamma = int("".join(zs), 2)
    eps = int("".join(ys), 2)
    print(gamma*eps)

if __name__ == '__main__':
    sys.exit(main(sys.argv))
