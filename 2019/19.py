#!/usr/bin/env python3

# I solved this with programming but like not *correct* programming?
# It works for the input I gave and was developed while looking at the map.

import copy
import sys
import time
from collections import defaultdict, deque

class IntCode:
    def __init__(self, program, input = None, output = None):
        self.program = program.copy()
        self.ip = 0
        self.relative_base = 0
        self.input = input or []
        self.output = output or []

    @property
    def done(self):
        return self.ip == -1

    def execute(self):
        if self.done:
            return

        p = self.program
        ip = self.ip

        while True:
            instr = p[ip]

            def read(i):
                mode = (instr // (10**(1+i))) % 10
                if mode == 0:
                    return p[p[ip+i]]
                elif mode == 1:
                    return p[ip+i]
                else:
                    return p[p[ip+i] + self.relative_base]

            def write(i, v):
                mode = (instr // (10**(1+i))) % 10
                if mode == 0:
                    p[p[ip+i]] = v
                else:
                    assert mode == 2
                    p[p[ip+i] + self.relative_base] = v

            if instr % 100 == 1:
                write(3, read(1) + read(2))
                ip += 4
            elif instr % 100 == 2:
                write(3, read(1) * read(2))
                ip += 4
            elif instr % 100 == 3:
                if not self.input:
                    self.ip = ip
                    return
                write(1, self.input.pop(0))
                ip += 2
            elif instr % 100 == 4:
                self.output.append(read(1))
                ip += 2
            elif instr % 100 == 5:
                if read(1) != 0:
                    ip = read(2)
                else:
                    ip += 3
            elif instr % 100 == 6:
                if read(1) == 0:
                    ip = read(2)
                else:
                    ip += 3
            elif instr % 100 == 7:
                if read(1) < read(2):
                    write(3, 1)
                else:
                    write(3, 0)
                ip += 4
            elif instr % 100 == 8:
                if read(1) == read(2):
                    write(3, 1)
                else:
                    write(3, 0)
                ip += 4
            elif instr % 100 == 9:
                self.relative_base += read(1)
                ip += 2
            elif instr % 100 == 99:
                break

        self.ip = -1

    def run(self, input):
        self.input = input
        self.output = []
        self.execute()
        return self.output


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
    lp = [int(x) for x in data[0].split(",")]
    p = defaultdict(int, [(i, x) for i, x in enumerate(lp)])
    board = defaultdict(lambda: " ")

    # Part 1
    interp = IntCode(p)
    out = interp.run([])

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
