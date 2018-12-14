#!/usr/bin/env python3

import sys

def main(args):
    seen = list(map(int, '598701'))
    things = [3, 7]
    n1 = 0
    n2 = 1
    i = 2
    while True:
        new = str(things[n1] + things[n2])
        for cc in new:
            c = int(cc)
            i += 1
            things.append(c)
            if i % 10000 == 0:
                print(i)
            if things[-len(seen):] == seen:
                print(i - len(seen))
                return
        n1 = (n1 + 1 + things[n1]) % len(things)
        n2 = (n2 + 1 + things[n2]) % len(things)


if __name__ == '__main__':
    sys.exit(main(sys.argv))
