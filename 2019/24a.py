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

def step(board):
    m = board
    nboard = copy.deepcopy(board)
    for y in range(len(board)):
        for x in range(len(m[0])):
#            neighbors_asdf = {(y+i, x+j) for i, j in DIRS if read(m, y+i, x+j) == "#"}
            neighbors = sum(read(m, x+i, y+j) == "#" for i, j in DIRS)
            print((x, y), neighbors, board[y][x])#, neighbors_asdf)
            if board[y][x] == "#" and neighbors != 1:
                print("die")
                nboard[y][x] = "."
            elif board[y][x] == "." and neighbors in (1, 2):
                print("born")
                nboard[y][x] = "#"

    return nboard


def main(args):
    data = [s.strip() for s in sys.stdin]
    board = [list(s) for s in data]

    print("START", board)
    seen = set()
    while True:
        tb = tuple(tuple(x) for x in board)
        if tb in seen:
            break
        seen.add(tb)

        board = step(board)
        print("STEP", board)

    print(board)
#    print(seen)

    score = 0
    pow = 1
    for l in board:
        for x in l:
            if x == "#":
                score += pow
            pow *= 2
    print(score)




if __name__ == '__main__':
    main(sys.argv)
