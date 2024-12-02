#!/usr/bin/env python3

import sys
import re

def extract(s):
    return [int(x) for x in re.findall(r'(-?\d+).?', s)]


def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    # data = [x.rstrip('\n').split('\n') for x in file.read().split('\n\n')]
    # data = [int(s.rstrip('\n')) for s in file]
    data = [extract(s.rstrip('\n')) for s in file]

    n = 0
    for x in data:
        asdfs = [list(x)]
        for i in range(len(x)):
            xx = list(x)
            xx.pop(i)
            asdfs.append(xx)

        ook = False

        for x in asdfs:
            ok = True
            if x != sorted(x) and x != list(reversed(sorted(x))):
                ok = False
            for a, b in zip(x, x[1:]):
                if abs(a-b) < 1 or abs(a-b) > 3:
                    ok = False

            ook |= ok

        if ook:
            n += 1

    print(n)


if __name__ == '__main__':
    main(sys.argv)
