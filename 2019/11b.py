#!/usr/bin/env python3

import sys
import re
import time
import itertools
from collections import defaultdict


def run(p, ip, input, output, relative_base):
    if ip == -1:
        return -1

    while True:
        instr = p[ip]

        def read(i):
            mode = (instr // (10**(1+i))) % 10
            if mode == 0:
                return p[p[ip+i]]
            elif mode == 1:
                return p[ip+i]
            else:
                return p[p[ip+i] + relative_base]

        def write(i, v):
            mode = (instr // (10**(1+i))) % 10
            if mode == 0:
                p[p[ip+i]] = v
            else:
                assert mode == 2
                p[p[ip+i] + relative_base] = v


        if instr % 100 == 1:
            write(3, read(1) + read(2))
            ip += 4
        elif instr % 100 == 2:
            write(3, read(1) * read(2))
            ip += 4
        elif instr % 100 == 3:
            if not input:
                return ip, relative_base
            write(1, input.pop(0))
            ip += 2
        elif instr % 100 == 4:
            output.append(read(1))
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
            relative_base += read(1)
            ip += 2
        elif instr % 100 == 99:
            break

    return -1, 0

DIRS = [(0, -1), (1, 0), (0, 1), (-1, 0)]

def main(args):
    data = [s.strip() for s in sys.stdin]
    lp = [int(x) for x in data[0].split(",")]
    p = defaultdict(int, [(i, x) for i, x in enumerate(lp)])
    colors = defaultdict(int)
    colors[0,0] = 1
    painted = set()

    ip = 0
    outs = []
    pos = (0, 0)
    dir = 0
    rb = 0
    while ip != -1:
        ic = colors[pos]
        ins = [colors[pos]]
        print(ins)

        ip, rb = run(p, ip, ins, outs, rb)
        print(ip, ic, pos, outs, len(painted))
        color, direction = outs
#        direction, color = color, direction
        print(ip, color, direction)
        colors[pos] = color
        painted.add(pos)
        if direction == 0:
            dir = (dir - 1) % 4
        else:
            dir = (dir + 1) % 4
        pos = (pos[0] + DIRS[dir][0], pos[1] + DIRS[dir][1])

        outs.clear()

        # minx = min(x for x, y in painted)
        # miny = min(y for x, y in painted)
        # maxx = max(x for x, y in painted)
        # maxy = max(y for x, y in painted)
        # for y in range(miny, maxy+1):
        #     l = ""
        #     for x in range(minx, maxx+1):
        #         l += " #"[colors[x,y]]
        #     print(l)
        # print("========================")


    print(outs)
    print(len(painted))

    minx = min(x for x, y in painted)
    miny = min(y for x, y in painted)
    maxx = max(x for x, y in painted)
    maxy = max(y for x, y in painted)
    for y in range(miny, maxy+1):
        l = ""
        for x in range(minx, maxx+1):
            l += " #"[colors[x,y]]
        print(l)


if __name__ == '__main__':
    sys.exit(main(sys.argv))
