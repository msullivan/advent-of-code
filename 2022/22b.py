#!/usr/bin/env python3

import sys
from collections import defaultdict, Counter, deque
from parse import parse
import re
import math

def extract(s):
    return [int(x) for x in re.findall(r'(-?\d+).?', s)]

def vadd(v1, v2):
    return tuple([x + y for x, y in zip(v1, v2)])
def vsub(v1, v2):
    return tuple([x - y for x, y in zip(v1, v2)])

def scale(k, v2):
    return tuple([k * y for y in v2])

def mag(v):
    return sum(abs(x) for x in v)

def dotp(v1, v2):
    return sum([x * y for x, y in zip(v1, v2)])


def ichr(i):
    return chr(ord('a') + i)

def iord(c):
    return ord(c.lower()) - ord('a')

def optidx(d, opt=max, nth=0):
    if not isinstance(d, dict):
        d = dict(enumerate(d))
    rv = opt(d.values())
    return [i for i, v in d.items() if v == rv][nth], rv

LETTERS = "abcdefghijklmnopqrstuvwxyz"

UP, RIGHT, DOWN, LEFT = VDIRS = (0, -1), (1, 0), (0, 1), (-1, 0),
DIRS = {'N': UP, 'E': RIGHT, 'S': DOWN, 'W': LEFT }
ALL_DIRS = [(x, y) for x in [-1,0,1] for y in [-1,0,1] if not x == y == 0]
FDIRS = [RIGHT, DOWN, LEFT, UP]

def turn(v, d='left'):
    n = -1 if d == 'left' else 1
    return VDIRS[(VDIRS.index(v) + n + len(VDIRS))%len(VDIRS)]


##############################
def draw(painted):
    minx = min(x for x, y in painted)
    miny = min(y for x, y in painted)
    maxx = max(x for x, y in painted)
    maxy = max(y for x, y in painted)

    l = ""
    # XXX: add reversed if needed
    for y in list((range(miny, maxy+1))):
        for x in range(minx, maxx+1):
            l += painted.get((x,y), " ")
        l += "\n"
    print(l)


def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    data = [x.rstrip('\n').split('\n') for x in file.read().split('\n\n')]
    # data = [int(s.rstrip('\n')) for s in file]
    # data = [s.rstrip('\n') for s in file]
    mapo, cmd = data

    m = defaultdict(lambda: ' ')
    for y, line in enumerate(mapo):
        for x, c in enumerate(line):
            m[(x, y)] = c

    cmd = cmd[0].replace('R', ' R ').replace('L', ' L ').split()
    print(cmd)

    # print(mapo)
    draw(m)

    for x in range(len(mapo[0])):
        if m[(x, 0)] == '.':
            start = (x, 0)
            break

    N = len(mapo)
    # print(N, N/4)
    N4 = N // 4
    print(len(mapo), len(mapo[-1]))
    N4 = 50


    X, Y = 1, 2

    TL, TR, BL, BR = 0, 1, 2, 3
    dirs = {
        (1, UP): (6, RIGHT, 1, ),
        (1, LEFT): (4, RIGHT, 1, ),
        (2, UP): (6, UP, 1, ),
        (2, RIGHT): (5, LEFT, 1, ),
        (2, DOWN): (3, LEFT, 1, ),
        (3, RIGHT): (2, UP, 1),
        (3, LEFT): (4, DOWN, 1,),
        (4, UP): (3, RIGHT, 1,),
        (4, LEFT): (1, RIGHT, 1),
        (5, RIGHT): (2, LEFT, ),
        (5, DOWN): (6, LEFT, ),
        (6, RIGHT): (5, UP, ),
        (6, DOWN): (2, DOWN, ),
        (6, LEFT): (1, DOWN, ),
    }
    TOPS = [
        (N4, 0),
        (N4*2, 0),
        (N4, N4),
        (0, N4*2),
        (N4, N4*2),
        (0, N4*3),
    ]
    CORNERS = {
        UP: (0, 0),
        RIGHT: (N4-1, 0),
        DOWN: (N4-1, N4-1),
        LEFT: (0, N4-1),
    }

    def get_face(p):
        x, y = p
        if y < N4:
            if x < 2*N4:
                return 1
            else:
                return 2
        elif y < N4*2:
            return 3
        elif y < N4*3:
            if x < N4:
                return 4
            else:
                return 5
        else:
            return 6

    def wrap(p, f):
        if m[p] != ' ':
            return p, f

        rf = (-f[0], -f[1])
        op = vadd(p, rf)
        face = get_face(op)

        p_rel = vsub(op, TOPS[face-1])
        corner = CORNERS[f]
        displacement = mag(vsub(p_rel, corner))

        nface, nf, *_ = dirs[face, f]

        canon_edge = turn(nf, 'left')
        canon_corner_dir = turn(canon_edge, 'left')
        canon_corner = CORNERS[canon_corner_dir]

        displacement2 = (N4-1) - displacement
        pos_rel = vadd(canon_corner, scale(displacement2, canon_edge))

        print()
        print(f'orig p={op}')
        print(f'FUCK: {face=} {nface=} {f=}, {nf=}')
        print(f'{displacement=} {p_rel=} {pos_rel=}')
        # print("FUCK, face = ", face, f, ft, "dir =", dirs[face, f])


        np = vadd(pos_rel, TOPS[nface-1])
        print(f'{np=}')
        print('nf', nf)
        return np, nf

        # print(p_rel)

        # ft = turn(f, 'right')
        # nb_p = dotp(f, p_rel)
        # nb_q = dotp(ft, p_rel)

        # nface, nf = dirs[face, f]
        # rnf = (-nf[0], -nf[1])
        # rnf2 = turn(rnf, 'right')

        # np_rel = vadd(scale(nb_p, rnf), scale(nb_q, rnf2))
        # np = vadd(np_rel, TOPS[nface-1])

        # print("FUCK, face = ", face, f, ft, "dir =", dirs[face, f])
        # print(nb_p, nb_q)
        # print('nfs', rnf, rnf2)
        # print(np_rel, np)

        # assert m[np] != ' '

        # return np

        # print('coord', op, p, face)
        # while True:
        #     np = vadd(p, rf)
        #     if m[np] == ' ':
        #         return p
        #     p = np


    print(start)
    facing = (1, 0)
    for entry in cmd:
        rfacing = scale(-1, facing)
        if entry == 'L':
            facing = turn(facing, 'left')
        elif entry == 'R':
            facing = turn(facing, 'right')
        else:
            amt = int(entry)
            for _ in range(amt):
                nstart, nfacing = wrap(vadd(start, facing), facing)
                nrfacing = scale(-1, nfacing)
                ostart, ofacing = wrap(vadd(nstart, nrfacing), nrfacing)
                assert start == ostart, (start, ostart)

                if m[nstart] == '#':
                    break
                start = nstart
                facing = nfacing

        print(start, facing)

    print(start, facing)
    print((start[1]+1)*1000 + 4*(start[0]+1) + FDIRS.index(facing))



if __name__ == '__main__':
    main(sys.argv)
