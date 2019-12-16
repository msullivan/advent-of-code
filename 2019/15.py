#!/usr/bin/env python3

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


DIRS = [(0, -1), (0, 1), (1, 0), (-1, 0)]

def draw(painted):
    minx = min(x for x, y in painted)
    miny = min(y for x, y in painted)
    maxx = max(x for x, y in painted)
    maxy = max(y for x, y in painted)
    l = ""
    for y in range(miny, maxy+1):
        for x in range(minx, maxx+1):
            l += painted[x,y]
        l += "\n"
    print(l)


def step(p, i):
    p2 = copy.deepcopy(p)
    asdf = p2.run([i])
    assert not p2.done
    (out,) = asdf
    return p2, out

def add(v1, v2):
    return tuple(x + y for x, y in zip(v1, v2))

def main(args):
    data = [s.strip() for s in sys.stdin]
    lp = [int(x) for x in data[0].split(",")]
    p = defaultdict(int, [(i, x) for i, x in enumerate(lp)])
    board = defaultdict(lambda: " ")

    # Part 1
    interp = IntCode(p)
    q = deque([(interp, 0, (0, 0))])
    seen = {(0, 0)}

    while q:
        p, steps, pos = q.popleft()
        for dir in range(0, 4):
            nextpos = add(pos, DIRS[dir])
            if nextpos in seen:
                continue
            seen.add(nextpos)

            p2, state = step(p, dir+1)
            if state == 2:
                part1 = steps+1
                source = nextpos
                board[nextpos] = "."
                print(nextpos, steps+1)
            elif state == 1:
                board[nextpos] = "."
                q.append((p2, steps+1, nextpos))
            elif state == 0:
                board[nextpos] = "#"

    draw(board)


    # Part 2
    q = deque([(0, source)])
    seen = {source}

    while q:
        steps, pos = q.popleft()
        for dir in range(0, 4):
            nextpos = add(pos, DIRS[dir])
            if nextpos in seen:
                continue
            seen.add(nextpos)

            if board[nextpos] == ".":
                q.append((steps+1, nextpos))

    print(part1)
    print(steps)


if __name__ == '__main__':
    sys.exit(main(sys.argv))
