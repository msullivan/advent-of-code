#!/usr/bin/env python3

import copy
import sys
import time
from collections import defaultdict, deque
from intcode import IntCode

import array

DIRS = [(0, -1), (1, 0), (0, 1), (-1, 0)]

def add(v1, v2):
    return tuple(x + y for x, y in zip(v1, v2))

evals = 0

def inside(p, x, y):
    global evals
    evals += 1
    interp = IntCode(p)
    out = interp.run([x, y])
    return bool(out[0])

def box(p, x, y, sz):
    sz -= 1
    return inside(p, x, y) and inside(p, x+sz, y) and inside(p, x, y-sz) and inside(p, x+sz, y-sz)


def main(args):
    data = [s.strip() for s in sys.stdin]
    p = array.array('q', [int(x) for x in data[0].split(",")] + [0]*50)
    board = defaultdict(lambda: " ")

    # Part 1

    cnt = 0
    for x in range(50):
        for y in range(50):
            interp = IntCode(p)
            out = interp.run([x, y])
            cnt += out[0]
            board[(x, y)] = "#" if out[0] else "."


    draw(board)

    sz = 100
    row = 6
    col = 0
    while True:
        while not inside(p, col, row):
            col += 1

        if box(p, col, row, sz):
            break
        row += 1
        #row *= 2

    print(cnt)
    print(col, row)
    print(col*10000 + row-sz+1)
    print("evals", evals)


def draw(painted):
    minx = min(x for x, y in painted)
    miny = min(y for x, y in painted)
    maxx = max(x for x, y in painted)
    maxy = max(y for x, y in painted)
    l = ""
    for y in range(miny, maxy+1):
        l += "{:3} ".format(y)
        for x in range(minx, maxx+1):
            l += painted[x,y]
        l += "\n"
    print(l)



main([])

# 17 at 100
