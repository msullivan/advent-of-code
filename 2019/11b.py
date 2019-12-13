#!/usr/bin/env python3

import sys
import re
import time
import itertools
from collections import defaultdict

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

    def run(self):
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


DIRS = [(0, -1), (1, 0), (0, 1), (-1, 0)]

def main(args):
    data = [s.strip() for s in sys.stdin]
    lp = [int(x) for x in data[0].split(",")]
    p = defaultdict(int, [(i, x) for i, x in enumerate(lp)])
    colors = defaultdict(int)
    colors[0,0] = 1
    painted = set()


    interp = IntCode(p)

    pos = (0, 0)
    dir = 0
    while not interp.done:
        ic = colors[pos]
        interp.input = [colors[pos]]

        interp.run()
        color, direction = interp.output
        interp.output.clear()
#        direction, color = color, direction
        print(color, direction)
        colors[pos] = color
        painted.add(pos)
        if direction == 0:
            dir = (dir - 1) % 4
        else:
            dir = (dir + 1) % 4
        pos = (pos[0] + DIRS[dir][0], pos[1] + DIRS[dir][1])

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
