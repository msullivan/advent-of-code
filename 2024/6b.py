#!/usr/bin/env python3

import sys
from collections import defaultdict

def vadd(v1, v2):
    if len(v1) == 2:
        return v1[0] + v2[0], v1[1] + v2[1]
    elif len(v1) == 2:
        return v1[0] + v2[0], v1[1] + v2[1], v1[2] + v2[2]
    else:
        return tuple([x + y for x, y in zip(v1, v2)])

UP, RIGHT, DOWN, LEFT = VDIRS = (0, -1), (1, 0), (0, 1), (-1, 0),

def turn(v, d='left'):
    n = -1 if d == 'left' else 1
    return VDIRS[(VDIRS.index(v) + n) % len(VDIRS)]


def _try(m, pos, obstacle):
    m = m.copy()
    m[obstacle] = '#'

    seen = set()
    dir = UP
    while m[pos] != 'O':
        if (pos, dir) in seen:
            return seen, True
        seen.add((pos, dir))
        nxt = vadd(dir, pos)
        if m[nxt] == '#':
            dir = turn(dir, d='right')
        else:
            pos = nxt

    return seen, False


def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    data = [s.rstrip('\n') for s in file]


    m = defaultdict(lambda: 'O')
    for y, l in enumerate(data):
        for x, c in enumerate(l):
            m[x, y] = c
            if c == '^':
                pos = x, y

    seen_all, _ = _try(m, pos, (-1, -1))
    seen = {x for x, _ in seen_all}

    n = 0
    i = 0
    for spot, c in m.items():
        # This optimization wasn't in the original solution
        if spot not in seen:
            continue
        if spot != pos and c == '.':
            i += 1
            # print(i, spot)
            _, ok = _try(m, pos, spot)
            if ok:
                n += 1
    print(len(seen))
    print(n)


if __name__ == '__main__':
    main(sys.argv)
