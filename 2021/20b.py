#!/usr/bin/env python3

import sys

def vadd(v1, v2):
    return tuple(x + y for x, y in zip(v1, v2))

ALL_DIRS = [(y, x) for x in [-1,0,1] for y in [-1,0,1]]


def get_index(default, m, pos):
    l = "".join([m.get(vadd(pos, d), default) for d in ALL_DIRS])
    l = l.replace(".", "0").replace("#", "1")
    idx = int(l, 2)
    return idx


def step(m, lookup, default):
    nearby = {vadd(d, p) for p in m for d in ALL_DIRS}
    return {
        pos: lookup[get_index(default, m, pos)] for pos in nearby
    }


def draw(painted):
    minx = min(x for x, y in painted)
    miny = min(y for x, y in painted)
    maxx = max(x for x, y in painted)
    maxy = max(y for x, y in painted)

    l = ""
    for y in (list((range(miny, maxy+1)))):
        for x in range(minx, maxx+1):
            l += painted[x,y]
        l += "\n"
    print(l)


def main(args):
    data = [s.strip() for s in sys.stdin]

    algo = data[0]
    assert len(algo) == 512
    m = {(x, y): v for y, l in enumerate(data[2:]) for x, v in enumerate(l)}

    om = m
    print(ALL_DIRS)

    draw(m)
    for i in range(50):
        if algo[0] == '#':
            default = "." if i%2 == 0 else "#"
        else:
            default = '.'
        m = step(m, algo, default)
        print()
        draw(m)

    print(sum(v == '#' for v in m.values()))

if __name__ == '__main__':
    main(sys.argv)
