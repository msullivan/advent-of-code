#!/usr/bin/env python3

import sys
from collections import defaultdict, Counter, deque
import re
import os

def extract(s):
    return [int(x) for x in re.findall(r'(-?\d+).?', s)]

def vadd(v1, v2):
    if len(v1) == 2:
        return v1[0] + v2[0], v1[1] + v2[1]
    elif len(v1) == 3:
        return v1[0] + v2[0], v1[1] + v2[1], v1[2] + v2[2]
    else:
        # ... this is so slow.
        return tuple([x + y for x, y in zip(v1, v2)])


def draw(painted):
    minx = min(x for x, y in painted)
    miny = min(y for x, y in painted)
    maxx = max(x for x, y in painted)
    maxy = max(y for x, y in painted)

    l = ""
    # XXX: add reversed if needed
    for y in list((range(miny, maxy+1))):
        for x in range(minx, maxx+1):
            l += painted.get((x,y), ".")
        l += "\n"
    print(l)

def draw_img(painted):
    import numpy as np
    from PIL import Image

    minx = miny = 0
    miny = min(y for x, y in painted)
    maxx = max(x for x, y in painted)
    maxy = max(y for x, y in painted)

    array = np.zeros((maxx+1, maxy+1), dtype=np.dtype('B'))

    for pos, c in painted.items():
        if c == '#':
            array[pos] = 255

    im = Image.fromarray(array)
    return im


##############################

def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    # data = [x.rstrip('\n').split('\n') for x in file.read().split('\n\n')]
    # data = [int(s.rstrip('\n')) for s in file]
    data = [s.rstrip('\n') for s in file]

    ps = []
    vs = []
    for line in data:
        a, b, c, d = extract(line)
        ps.append((a, b))
        vs.append((c, d))

    W = 101
    H = 103
    #11 7

    output = ""

    seen = set()

    os.mkdir("day14")

    for i in range(100000000):
        # print('========================', i)
        m = defaultdict(lambda: ' ')
        for p in ps:
            m[p] = '#'

        img = draw_img(m)
        img.save(f'day14/{i:05}.png')
        output += f'<img src="{i:05}.png">\n'

        nps = []
        for p, v in zip(ps, vs):
            a, b = vadd(p, v)
            np = (a % W, b % H)
            nps.append(np)

        ps = nps

        xs = tuple(ps)
        if xs in seen:
            break
        seen.add(xs)

    with open('day14/index.html', 'w') as f:
        f.write(output)


if __name__ == '__main__':
    main(sys.argv)
