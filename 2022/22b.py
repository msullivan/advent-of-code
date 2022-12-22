#!/usr/bin/env python3

import sys
from collections import defaultdict


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


UP, RIGHT, DOWN, LEFT = VDIRS = (0, -1), (1, 0), (0, 1), (-1, 0),
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

    # print(mapo)
    draw(m)

    for x in range(len(mapo[0])):
        if m[(x, 0)] == '.':
            start = (x, 0)
            break

    N = len(mapo)
    N4 = N // 4

    CORNERS = {
        UP: (0, 0),
        RIGHT: (N4-1, 0),
        DOWN: (N4-1, N4-1),
        LEFT: (0, N4-1),
    }

    # XXX: I have basically no idea how to derive this from the input i
    dirs = {
        (1, UP): (6, RIGHT),
        (1, LEFT): (4, RIGHT),
        (2, UP): (6, UP),
        (2, RIGHT): (5, LEFT),
        (2, DOWN): (3, LEFT),
        (3, RIGHT): (2, UP),
        (3, LEFT): (4, DOWN),
        (4, UP): (3, RIGHT),
        (4, LEFT): (1, RIGHT),
        (5, RIGHT): (2, LEFT),
        (5, DOWN): (6, LEFT),
        (6, RIGHT): (5, UP),
        (6, DOWN): (2, DOWN),
        (6, LEFT): (1, DOWN),
    }

    # Compute top positions from the input; top to bottom, left to right
    tops = []
    for i in range(0, 4):
        for j in range(0, 4):
            c = (j*N4, i*N4)
            if m.get(c, ' ') != ' ':
                tops.append(c)

    def get_face(p):
        px, py = p
        for i, (cx, cy) in enumerate(tops):
            if cx <= px < cx+N4 and cy <= py < cy+N4:
                return i + 1

    def wrap(p, f):
        if m[p] != ' ':
            return p, f

        rf = scale(-1, f)
        op = vadd(p, rf)
        face = get_face(op)

        # Find how far the point is from the "leading corner" on the
        # exit edge, then reflect that across the middle of the entry
        # edge of the new face.

        p_rel = vsub(op, tops[face-1])
        corner = CORNERS[f]
        displacement = mag(vsub(p_rel, corner))

        nface, nf = dirs[face, f]

        canon_edge = turn(nf, 'left')
        canon_corner_dir = turn(canon_edge, 'left')
        canon_corner = CORNERS[canon_corner_dir]

        displacement2 = (N4-1) - displacement
        pos_rel = vadd(canon_corner, scale(displacement2, canon_edge))
        np = vadd(pos_rel, tops[nface-1])

        # print()
        # print(f'orig p={op}')
        # print(f'FUCK: {face=} {nface=} {f=}, {nf=}')
        # print(f'{displacement=} {p_rel=} {pos_rel=}')
        # print(f'{np=}')
        # print('nf', nf)

        return np, nf


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
