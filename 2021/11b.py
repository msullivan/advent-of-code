#!/usr/bin/env python3

import sys


def vadd(v1, v2):
    return tuple(x + y for x, y in zip(v1, v2))


ADIRS = [(x,y) for x in [-1,0,1] for y in [-1,0,1] if not x == y == 0]


def step(m):
    for k in list(m):
        m[k] += 1

    togo = [k for k, v in m.items() if v > 9]
    flashes = 0
    while togo:
        flashes += 1
        v = togo.pop()
        for d in ADIRS:
            n = vadd(v, d)
            if n in m:
                m[n] += 1
                if m[n] == 10:
                    togo.append(n)

    for k in list(m):
        if m[k] > 9:
            m[k] = 0

    return flashes


def main(args):
    data = [s.strip() for s in sys.stdin]
    data = [[int(x) for x in l] for l in data]

    m = {(i, j): v for i, l in enumerate(data) for j, v in enumerate(l)}

    n = 0
    while True:
        flashes = step(m)
        n += 1
        if flashes == len(m):
            break

    print(n)

if __name__ == '__main__':
    main(sys.argv)
