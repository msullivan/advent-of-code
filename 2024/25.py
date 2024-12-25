#!/usr/bin/env python3

import sys

def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    data = [x.rstrip('\n').split('\n') for x in file.read().split('\n\n')]

    locks = []
    keys = []
    for obj in data:
        trans = list(map(list, zip(*obj)))
        key = tuple(sum(c == '#' for c in l)-1 for l in trans)

        if '#' in obj[0]:
            locks.append(key)
        else:
            keys.append(key)

    n = 0
    for key in keys:
        for lock in locks:
            if all(x + y <= 5 for x, y in zip(key, lock)):
                n += 1

    print(n)

if __name__ == '__main__':
    main(sys.argv)
