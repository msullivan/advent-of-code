#!/usr/bin/env python3

import operator
import math
import functools
from collections import defaultdict
import sys
import re

def extract(s):
    return [int(x) for x in re.findall(r'-?\d+', s)]

def rotate(g):
    xs = []
    for i in range(len(g)):
        s = ''.join(x[i] for x in g)
        xs.append(s)

    return tuple(reversed(xs))

def flip(g):
    return tuple(reversed(g))

def ledge(g):
    return ''.join(x[0] for x in g)

def redge(g):
    return ''.join(x[-1] for x in g)

def edges(g):
    return [g[0], g[-1], ledge(g), redge(g)]

def all_edges(g):
    es = edges(g)
    return es + [''.join(reversed(x)) for x in es]

def moves(g):
    for _ in range(4):
        yield g
        yield flip(g)
        g = rotate(g)

MONSTER = """\
                  #
#    ##    ##    ###
 #  #  #  #  #  #   """.split('\n')

def main(args):
    data = [x.strip().split('\n') for x in sys.stdin.read().strip().split('\n\n')]

    # Parse
    tiles = {}
    for tile in data:
        n = extract(tile[0])[0]
        tiles[n] = flip(tile[1:])

    N = int(math.sqrt(len(tiles)))

    # Build map from possible edges to the tiles that use them
    edge_map = defaultdict(list)
    for n, tile in tiles.items():
        for e in all_edges(tile):
            edge_map[e].append(n)

    # Find the corners: they are the tiles that only have two edges
    # that are shared with other tiles.
    corners = []
    for n, tile in tiles.items():
        cnt = 0
        for e in edges(tile):
            cnt += len(edge_map[e]) - 1
        if cnt == 2:
            corners.append(n)

    # Pick a corner to be the top-left, and try rotations until the
    # unmatched edges are facing up and left.
    corner_n = corners[0]
    ltile = tiles[corner_n]
    while len(edge_map[ledge(ltile)]) == 2:
        ltile = rotate(ltile)

    # Place the tiles one at a time. Since they are uniquely matched
    # up, there's always one unique option for each spot. When going
    # across rows, we pick the one that lines up to the left, and in
    # the first column pick the one that matches at the top.
    def pick(ln, lgrid):
        """Find a tile and rotation of it to go to the right of ln/lgrid"""
        re = redge(lgrid)
        me = [x for x in edge_map[re] if x != ln][0]
        mtile = tiles[me]
        for mtile in moves(mtile):
            if re == ledge(mtile):
                break
        return me, mtile

    mgrid = [[None] * N for x in range(N)]
    mgrid[0][0] = corner_n, ltile
    for y in range(0, N):
        if y > 0:
            ln, lgrid = mgrid[y-1][0]
            # pick looks for something that matches on the right edge,
            # so rotate and flip so our bottom edge is the right edge,
            # and reverse the transform at the end
            me, mtile = pick(ln, flip(rotate(lgrid)))
            mgrid[y][0] = (me, flip(rotate(mtile)))

        for x in range(1, N):
            ln, lgrid = mgrid[y][x-1]
            mgrid[y][x] = pick(ln, lgrid)

    # Strip the borders off of each tile
    ngrid = [[None] * N for x in range(N)]
    for i, row in enumerate(mgrid):
        for j, (_, col) in enumerate(row):
            x = list(col[1:-1])
            for k in range(len(x)):
                x[k] = x[k][1:-1]
            ngrid[i][j] = x

    # Build one big image
    pic = []
    for i, row in enumerate(ngrid):
        for i2 in range(len(row[0])):
            s = ''
            for j, col in enumerate(ngrid[i]):
                s += col[i2]
            pic.append(s)

    # Look for monsters
    for pic in moves(pic):
        cnt = 0
        for y in range(len(pic)-len(MONSTER)):
            for x in range(len(pic)-len(MONSTER[0])):
                # Check if there's a monster starting at this position
                match = True
                for y0 in range(len(MONSTER)):
                    for x0 in range(len(MONSTER[y0])):
                        if MONSTER[y0][x0] == '#' and pic[y+y0][x+x0] != '#':
                            match = False
                            break
                    if not match:
                        break

                if match:
                    cnt += 1

        if cnt:
            break

    # Wooooooo
    part1 = functools.reduce(operator.mul, corners)
    print(part1)

    everything = ''.join(pic).count('#')
    monster = ''.join(MONSTER).count('#')

    print(everything - monster*cnt)

if __name__ == '__main__':
    sys.exit(main(sys.argv))
