#!/usr/bin/env python3

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

    fuck = 1
    last = -1
    for n, tile in tiles.items():
        cnt = 0
        for e in edges(tile):
            cnt += len(edge_map[e])
        # print(cnt)
        if cnt == 6:
            print("HEY", n)
            fuck *= n
            last = n
    print(fuck)

    print("starting in corner", n)
    mgrid = [[None] * 12 for x in range(12)]
    mgrid[0][0] = last, tiles[last]
    y = 0
    for x in range(1, 12):
        ln, lgrid = mgrid[y][x-1]


    # stile = test
    # print(start, stile)
    # for edge in edges(rotate(stile)):
    #     print(edge)
    #     print(edge_map[edge])

if __name__ == '__main__':
    sys.exit(main(sys.argv))
