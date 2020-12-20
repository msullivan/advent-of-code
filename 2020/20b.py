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

    print(tiles)
    start, test = next(iter(tiles.items()))

    print()
    print('\n'.join(test))
    print()
    print('\n'.join(rotate(test)))

    print(all_edges(test))
    print(all_edges(rotate(test)))

    edge_map = defaultdict(list)
    for n, tile in tiles.items():
        print("AAAA", tile)
        for e in all_edges(tile):
            edge_map[e].append(n)

    print([len(x) for x in edge_map.values()])
    print(edge_map)

    part1 = 1
    last = -1
    for n, tile in tiles.items():
        cnt = 0
        for e in edges(tile):
            cnt += len(edge_map[e])
        # print(cnt)
        if cnt == 6:
            print("HEY", n)
            part1 *= n
            last = n
    print(part1)

    ltile = tiles[last]
    while len(edge_map[ledge(ltile)]) == 2:
        print('rotating initial')
        ltile = rotate(ltile)
    if len(edge_map[ltile[0]]) == 2:
        print('flipping initial??')
        ltile = list(reversed(ltile))

    N = int(math.sqrt(len(tiles)))

    print("starting in corner", n)
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
                print('rotating')
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
                print('rotating')
                mrev = list(reversed(mtile))
                if re == ledge(mrev):
                    mtile = mrev
                    break
                mtile = rotate(mtile)

            mgrid[y][x] = me, mtile
            print(me, ln)
            # break

    # print(len(mgrid))
    ngrid = copy.deepcopy(mgrid)
    for i, row in enumerate(ngrid):
        for j, col in enumerate(ngrid[i]):
            print(i, j)
            x = list(col[1])
            x.pop(0)
            x.pop()
            for k in range(len(x)):
                x[k] = x[k][1:-1]
            ngrid[i][j] = x


    # print("FUUUUUCK")
    print(ngrid)

    pic = []
    for i, row in enumerate(ngrid):
        for i2 in range(8):
            s = ''
            for j, col in enumerate(ngrid[i]):
                s += col[i2]
            pic.append(s)

    print(pic)
    print(len(pic))
    print([len(x) for x in pic])

    # pic = PIC
    # pic = MONSTER + MONSTER
    # print(pic)
    print(MONSTER)
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


                # print("CHECK")
                # print(repr(pic[y][x:x+t]), repr(MONSTER[0]), pic[y][x:x+t] == MONSTER[0])
                # print(repr(pic[y+1][x:x+t]), repr(MONSTER[1]), pic[y+1][x:x+t] == MONSTER[1])
                # print(repr(pic[y+2][x:x+t]), repr(MONSTER[2]), pic[y+2][x:x+t] == MONSTER[2])
                # print(repr(pic[y][x:x+t]), repr(MONSTER[0]))
                # if pic[y][x:x+t] == MONSTER[0] and pic[y+1][x:x+t] == MONSTER[1] and pic[y+2][x:x+t] == MONSTER[2]:
                #     cnt += 1
        print("monster count!", cnt)
        if cnt:
            break
        pic = rotate(pic)
        if i == 3:
            pic = list(reversed(pic))

    everything = ''.join(pic).count('#')
    monster = ''.join(MONSTER).count('#')
    print(everything, monster)
    print(part1)
    print(everything - monster*cnt)



    # stile = test
    # print(start, stile)
    # for edge in edges(rotate(stile)):
    #     print(edge)
    #     print(edge_map[edge])

if __name__ == '__main__':
    sys.exit(main(sys.argv))
