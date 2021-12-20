#!/usr/bin/env python3

import sys
import re

def extract(s):
    return [int(x) for x in re.findall(r'(-?\d+).?', s)]

def vsub(v1, v2):
    return tuple(x - y for x, y in zip(v1, v2))

def mdist(v1, v2):
    return sum(abs(x - y) for x, y in zip(v1, v2))

def crossp(a, b):
    a1, a2, a3 = a
    b1, b2, b3 = b
    return (a2*b3 - a3*b2, -(a1*b3 - a3*b1), a1*b2 - a2*b1)

def dot(x, y):
    return sum(a*b for a, b in zip(x, y))

def rotate(x, rot):
    # ... this is a matrix multiplication
    i, j, k = rot
    return (dot(i, x), dot(j, x), dot(k, x))

def rebase(p, rot, l):
    return [vsub(rotate(x, rot), p) for x in l]


def match(rots, s1, s2):
    ss1 = set(s1)
    for o1 in s1:
        mdists1 = set([mdist(o1, x) for x in s1])
        for zo2 in s2:
            # This is the big optimization that gets the time down to
            # 3.75s (from like 2m): only try the rotations if there are
            # at least 12 points in s2 with manhattan distances that
            # also appear in 1.
            mdists2 = [mdist(zo2, x) for x in s2]
            if sum([x in mdists1 for x in mdists2]) < 12:
                continue

            # Alright actually try each rotation
            for rot in rots:
                delta = vsub(rotate(zo2, rot), o1)

                rs2 = rebase(delta, rot, s2)
                matches = ss1 & set(rs2)
                if len(matches) >= 12:
                    return delta, rot, rs2

    return None


def main(args):
    data = [x.split('\n') for x in sys.stdin.read().split('\n\n')]
    data = [[tuple(extract(s)) for s in x[1:] if s] for x in data]

    tops = [
        (1,0), (0,1), (-1,0), (0,-1)
    ]
    rots = []
    for i in range(3):
        for n in [1, -1]:
            for top in tops:
                t = list(top)
                t.insert(i, 0)
                f = [0, 0]
                f.insert(i, n)
                rots.append((tuple(f), tuple(t), crossp(f, t)))

    solved = {}
    solved[0] = ((0, 0, 0), rots[0])
    done = set()
    wl = [0]

    sensors = set(data[0])

    while wl:
        i = wl.pop()
        d1 = data[i]

        pos, rot = solved[i]
        d1 = rebase(pos, rot, d1)

        for j, d2 in enumerate(data):
            if j in done or i == j: continue

            res = match(rots, d1, d2)
            if res:
                delta, nrot, new = res
                sensors.update(new)
                print("FOUND", vsub((0,0,0), delta), nrot, i, j)
                wl.append(j)
                solved[j] = (delta, nrot)
        done.add(i)

    print(len(sensors))
    print(max(mdist(x[0], y[0]) for x in solved.values() for y in solved.values()))


if __name__ == '__main__':
    main(sys.argv)
