#!/usr/bin/env python3

import sys
from collections import defaultdict

def extract(s):
    return [int(x) for x in re.findall(r'(-?\d+).?', s)]

def vadd(v1, v2):
    return v1[0] + v2[0], v1[1] + v2[1]

UP, RIGHT, DOWN, LEFT = VDIRS = (0, -1), (1, 0), (0, 1), (-1, 0),

def turn(v, d='left'):
    n = -1 if d == 'left' else 1
    return VDIRS[(VDIRS.index(v) + n) % len(VDIRS)]


##############################

def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    data = [s.rstrip('\n') for s in file]

    m = defaultdict(lambda: '.')
    for y, l in enumerate(data):
        for x, c in enumerate(l):
            m[x,y] = c

    vals = set(m)
    seen = set()
    sets = []
    for spot in vals:
        if spot in seen:
            continue
        grp = {spot}
        q = [spot]
        while q:
            x = q.pop()
            for n in VDIRS:
                xn = vadd(x, n)
                if m[xn] == m[spot] and xn not in seen:
                    q.append(xn)
                    seen.add(xn)
                    grp.add(xn)

        sets.append((grp, m[spot]))

    score1 = score2 = 0
    for s, c in sets:
        area = len(s)
        perim = 0
        edges = set()
        for x in s:
            for n in VDIRS:
                xn = vadd(x, n)
                if xn not in s:
                    perim += 1
                    edges.add((x, n))

        medges = []
        while edges:
            space, dir = edges.pop()
            grp = {space}
            for d in ['left', 'right']:
                td = turn(dir, d)
                n = space
                while ((x := vadd(n, td)), dir) in edges:
                    edges.discard((x, dir))
                    grp.add(space)
                    n = x

            medges.append(grp)

        score1 += area*perim
        score2 += area*len(medges)

    print(score1)
    print(score2)


if __name__ == '__main__':
    main(sys.argv)
