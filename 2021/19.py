#!/usr/bin/env python3

import sys
import re

def extract(s):
    return [int(x) for x in re.findall(r'(-?\d+).?', s)]

def vsub(v1, v2):
    return tuple(x - y for x, y in zip(v1, v2))

def mdist(v1, v2):
    return sum(abs(x - y) for x, y in zip(v1, v2))

def recenter(p, l):
    return [vsub(x, p) for x in l]

def crossp(a, b):
    a1, a2, a3 = a
    b1, b2, b3 = b
    return (a2*b3 - a3*b2, -(a1*b3 - a3*b1), a1*b2 - a2*b1)

def dot(x, y):
    return sum(a*b for a, b in zip(x, y))

def rotate(x, rot):
    i, j, k = rot
    return (dot(i, x), dot(j, x), dot(k, x))


def match(rots, s1, s2):
    ss1 = set(s1)
    for o1 in s1:
        # print("OUT", o1)
        # rs1 = recenter(o1, s1)
        for rot in rots:
            rs2 = [rotate(x, rot) for x in s2]
            for o2 in rs2:
                p = vsub(o2, o1)
                cnt = 0
                for z in rs2:
                    if vsub(z, p) in ss1:
                        cnt += 1
                if cnt >= 12:
                    return o1, o2, rot, recenter(p, rs2)

                # # print("IN", o1)
                # rrs2 = recenter(vsub(o2, o1), rs2) # XXX
                # matches = ss1 & set(rrs2)
                # if len(matches) >= 12:
                #     return (o1, o2, rot, rrs2)

    return None


def main(args):
    data = [x.split('\n') for x in sys.stdin.read().split('\n\n')]
    data = [[tuple(extract(s)) for s in x[1:] if s] for x in data]

    tops = [
        (1,0),
        (0,1),
        (-1,0),
        (0,-1),
    ]
    rots = []
    for i in range(3):
        for n in [-1, 1]:
            for top in tops:
                t = list(top)
                t.insert(i, 0)
                f = [0, 0]
                f.insert(i, n)
                rots.append((tuple(f), tuple(t), crossp(f, t)))

    # XXX: is this really needed
    for i, (x, y, z) in enumerate(rots):
        if rotate((1,2,3), (x,y,z)) == (1,2,3):
            id_rot = i
            break
    else:
        raise AssertionError

    solved = {}
    solved[0] = ((0, 0, 0), rots[id_rot])
    done = set()
    wl = [0]

    sensors = set(data[0])

    while wl:
        i = wl.pop()
        d1 = data[i]

        pos, rot = solved[i]
        d1 = [rotate(x, rot) for x in d1]
        d1 = recenter(pos, d1) # XXX

        for j, d2 in enumerate(data):
            if j in done or i == j: continue

            res = match(rots, d1, d2)
            if res:
                a1, b1, r, new = res
                sensors.update(new)
                delta = vsub(b1, a1)
                print("REL", delta, r, i, j)
                wl.append(j)
                solved[j] = (delta, r)
        done.add(i)

    print(len(sensors))
    print(max(mdist(x[0], y[0]) for x in solved.values() for y in solved.values()))


if __name__ == '__main__':
    main(sys.argv)
