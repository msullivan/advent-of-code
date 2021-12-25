#!/usr/bin/env python3

import sys

def east(v, maxx):
    if v[0] == maxx:
        return (0, v[1])
    return (v[0] + 1, v[1])

def south(v, maxy):
    if v[1] == maxy:
        return (v[0], 0)
    return (v[0], v[1] + 1)


def main(args):
    data = [s.strip() for s in sys.stdin]
    m = {(x, y): v for y, l in enumerate(data) for x, v in enumerate(l) if v != "\n"}
    maxx = max(x for x, y in m)
    maxy = max(y for x, y in m)
    m = {k: v for k, v in m.items() if v != '.'}

    moved = True
    cnts = 0
    while moved:
        cnts += 1
        moved = False
        newm = {}
        for k, v in m.items():
            if v == '>' and east(k, maxx) not in m:
                newm[east(k, maxx)] = '>'
                moved = True
            else:
                newm[k] = v
        m = newm

        newm = {}
        for k, v in m.items():
            if v == 'v' and south(k, maxy) not in m:
                newm[south(k, maxy)] = 'v'
                moved = True
            else:
                newm[k] = v
        m = newm

    print(cnts)

if __name__ == '__main__':
    main(sys.argv)
