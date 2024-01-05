#!/usr/bin/env python3

# N.B: PRESERVED FOR POSTERITY: relative_base is not preserved across
# calls and somehow it works! (It did not work for part 2.)

import sys
import re
import time
import itertools
from collections import defaultdict


def run(p, ip, input, output):
    if ip == -1:
        return -1

    relative_base = 0

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
                return ip
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

    return -1

DIRS = [(0, -1), (1, 0), (0, 1), (-1, 0)]

def main(args):
    data = [s.strip() for s in sys.stdin]
    lp = [int(x) for x in data[0].split(",")]
    p = defaultdict(int, [(i, x) for i, x in enumerate(lp)])
    colors = defaultdict(int)
    painted = set()

    ip = 0
    outs = []
    pos = (0, 0)
    dir = 0
    while ip != -1:
        ic = colors[pos]
        ins = [colors[pos]]

        ip = run(p, ip, ins, outs)
        print(ip, ic, pos, outs, len(painted))
        color, direction = outs
        print(ip, color, direction)
        colors[pos] = color
        painted.add(pos)
        if direction == 0:
            dir = (dir - 1) % 4
        else:
            dir = (dir + 1) % 4
        pos = (pos[0] + DIRS[dir][0], pos[1] + DIRS[dir][1])

        outs.clear()
    print(outs)
    print(len(painted))

    minx = min(x for x, y in painted)
    miny = min(y for x, y in painted)
    maxx = max(x for x, y in painted)
    maxy = max(y for x, y in painted)
    for y in range(miny, maxy+1):
        l = ""
        for x in range(minx, maxx):
            l += " #"[colors[x,y]]
        print(l)


if __name__ == '__main__':
    sys.exit(main(sys.argv))
