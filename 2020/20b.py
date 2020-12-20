#!/usr/bin/env python3

import math
import copy
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
    return tuple(reversed(xs))

def ledge(g):
    return ''.join(x[0] for x in g)

def redge(g):
    return ''.join(x[-1] for x in g)

def edges(g):
    return sorted([
        g[0], g[-1], ledge(g), redge(g),
    ])

def all_edges(g):
    es = edges(g)
    return sorted(es + [''.join(reversed(x)) for x in es])

MONSTER = """\
                  # |
#    ##    ##    ###
 #  #  #  #  #  #   """.replace("|", "").split('\n')

PIC = """\
.#.#..#.##...#.##..#####
###....#.#....#..#......
##.##.###.#.#..######...
###.#####...#.#####.#..#
##.#....#.##.####...#.##
...########.#....#####.#
....#..#...##..#.#.###..
.####...#..#.....#......
#..#.##..#..###.#.##....
#.####..#.####.#.#.###..
###.#.#...#.######.#..##
#.####....##..########.#
##..##.#...#...#.#.#.#..
...#..#..#.#.##..###.###
.#.#....#.##.#...###.##.
###.#...#..#.##.######..
.#.#.###.##.##.#..#.##..
.####.###.#...###.#..#.#
..#.#..#..#.#.#.####.###
#..####...#.#.#.###.###.
#####..#####...###....##
#.##..#..#...#..####...#
.#.###..##..##..####.##.
...###...##...#...#..###""".split('\n')

def main(args):
    data = [x.strip().split('\n') for x in sys.stdin.read().split('\n\n')]
    # data = [s.strip() for s in sys.stdin]

    tiles = {}
    for tile in data:
        n = extract(tile[0])[0]
        tiles[n] = tile[1:]

    start, test = next(iter(tiles.items()))

    edge_map = defaultdict(list)
    for n, tile in tiles.items():
        for e in all_edges(tile):
            edge_map[e].append(n)

    part1 = 1
    last = -1
    for n, tile in tiles.items():
        cnt = 0
        for e in edges(tile):
            cnt += len(edge_map[e]) - 1
        if cnt == 2:
            part1 *= n
            last = n

    ltile = tiles[last]
    while len(edge_map[ledge(ltile)]) == 2:
        ltile = rotate(ltile)
    if len(edge_map[ltile[0]]) == 2:
        ltile = list(reversed(ltile))

    N = int(math.sqrt(len(tiles)))

    mgrid = [[None] * N for x in range(N)]
    mgrid[0][0] = last, ltile
    y = 0
    for y in range(0, N):
        if y > 0:
            ln, lgrid = mgrid[y-1][0]
            be = lgrid[-1]
            me = [x for x in edge_map[be] if x != ln][0]
            mtile = tiles[me]
            while be != mtile[0]:
                mrev = list(reversed(mtile))
                if be == mrev[0]:
                    mtile = mrev
                    break
                mtile = rotate(mtile)
            mgrid[y][0] = me, mtile


        for x in range(1, N):
            if x == y == 0: continue

            ln, lgrid = mgrid[y][x-1]
            re = redge(lgrid)
            me = [x for x in edge_map[re] if x != ln][0]
            mtile = tiles[me]
            while re != ledge(mtile):
                mrev = list(reversed(mtile))
                if re == ledge(mrev):
                    mtile = mrev
                    break
                mtile = rotate(mtile)

            mgrid[y][x] = me, mtile

    ngrid = copy.deepcopy(mgrid)
    for i, row in enumerate(ngrid):
        for j, col in enumerate(ngrid[i]):
            x = list(col[1])
            x.pop(0)
            x.pop()
            for k in range(len(x)):
                x[k] = x[k][1:-1]
            ngrid[i][j] = x

    pic = []
    for i, row in enumerate(ngrid):
        for i2 in range(len(row[0])):
            s = ''
            for j, col in enumerate(ngrid[i]):
                s += col[i2]
            pic.append(s)

    cnt = 0
    for i in range(8):
        t = len(MONSTER[0])
        for y in range(len(pic)-len(MONSTER)):
            for x in range(len(pic)-len(MONSTER[0])):
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
        pic = rotate(pic)
        if i == 3:
            pic = list(reversed(pic))

    everything = ''.join(pic).count('#')
    monster = ''.join(MONSTER).count('#')
    print(part1)
    print(everything - monster*cnt)

if __name__ == '__main__':
    sys.exit(main(sys.argv))
