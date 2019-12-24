#!/usr/bin/env python3

from __future__ import print_function

from collections import defaultdict, deque
import sys
import time
import math
import re
import copy

def extract(s):
    return [int(x) for x in re.findall(r'-?\d+', s)]

DIRS = [(0, -1), (1, 0), (0, 1), (-1, 0)]

def read(m, x, y):
    if y < 0 or y >= len(m) or x < 0 or x >= len(m[0]):
        return "."
    return m[y][x]

def _neighbors(x, y, l):
    nbrs = []
    for i, j in DIRS:
        x0, y0 = x+i, y+j
        #print(x, y, x0, y0)
        if (x0, y0) == (2, 2):
            if x == 1:
                nbrs.extend((0, k, l+1) for k in range(5))
            elif x == 3:
                nbrs.extend((4, k, l+1) for k in range(5))
            elif y == 1:
                nbrs.extend((k, 0, l+1) for k in range(5))
            elif y == 3:
                nbrs.extend((k, 4, l+1) for k in range(5))
            else:
                assert False
        elif x0 == -1:
            nbrs.append((1, 2, l-1))
        elif x0 == 5:
            nbrs.append((3, 2, l-1))
        elif y0 == -1:
            nbrs.append((2, 1, l-1))
        elif y0 == 5:
            nbrs.append((2, 3, l-1))
        else:
            assert not( y < 0 or y >= 5 or x < 0 or x >= 5)
            nbrs.append((x0, y0, l))

    assert len(nbrs) in (4, 8)
    return nbrs

def neighbors(x, y, l):
    nbrs = _neighbors(x, y, l)
    for nbr in nbrs:
        assert (x,y,l) in _neighbors(*nbr)
    return nbrs

def step(board):
    nboard = board.copy()
    live = [k for k, v in board.items() if v == "#"]
    for space in live:
        tocheck = [space] + neighbors(*space)
        for pos in tocheck:
#            print(pos)
            cnt = sum(board[nbr] == "#" for nbr in neighbors(*pos))
#            print((x, y), neighbors, board[y][x])#, neighbors_asdf)
            if board[pos] == "#" and cnt != 1:
#                print("die")
                nboard[pos] = "."
            elif board[pos] == "." and cnt in (1, 2):
#                print("born")
                nboard[pos] = "#"

    return nboard


def draw(board):
    lmin = min(l for _, _, l in board.keys())
    lmax = max(l for _, _, l in board.keys())

    print("==============")
    for l in range(lmin, lmax+1):
        print("Level", l)
        for y in range(5):
            line = ""
            for x in range(5):
                if (x, y) == (2, 2):
                    assert board[x, y, l] != "#"
                    line += "?"
                else:
                    line += board[x, y, l]
            print(line)
        print()


def main(args):
    data = [s.strip() for s in sys.stdin]
    m = [list(s) for s in data]

    board = defaultdict(lambda: ".")
    for y in range(len(m)):
        for x in range(len(m[y])):
            board[x,y,0] = m[y][x]
    del board[2,2,0]


    draw(board)
    seen = set()
    for i in range(200):
        board = step(board)
        draw(board)



    live = [k for k, v in board.items() if v == "#"]
    print(len(live))

if __name__ == '__main__':
    main(sys.argv)
