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

def main(args):
    data = [s.strip() for s in sys.stdin]
    lp = [int(x) for x in data[0].split(",")]
    p = defaultdict(int, [(i, x) for i, x in enumerate(lp)])
    board = defaultdict(lambda: " ")

    # Part 1
    interp = IntCode(p)
    out = interp.run([])

    s = "".join(chr(x) for x in out)
    print(s)
    m = s.split("\n")

    s = 0
    for y in range(len(m)):
        for x in range(len(m[y])):
            board[x,y] = m[y][x]


    for y in range(len(m)):
        for x in range(len(m[0])):
            if board[x,y] == "#" and all(board[add((x,y), dir)] == "#" for dir in DIRS):
                s += x*y

    part1 = s

    # Part 2
    # find the path. this is based on a heuristic of "go straight at crossroads"
    path = []
    pos = next(k for k, v in board.items() if v == "^")
    dir = 0
    moved = 0
    board[pos] = "%"
    while True:
        npos = add(pos, DIRS[dir])
        if board[npos] in "#%":
            moved += 1
            pos = npos
            board[npos] = "%"
            #path.append('1')
        else:
            if moved: path.append(str(moved))
            moved = 0
            for off, turn in [(-1, "L"), (1, "R")]:
                ndir = (dir + off) % 4
                if board[add(pos, DIRS[ndir])] in "#%":
                    path.append(turn)
                    dir = ndir
                    break
            else:
                break


    parts = []
    # Do some n^4? shit but n is 80 so who gaf
    # This is definitely not guarenteed to work but it does.
    for part in "ABC":
        max = 0
        maxi, maxj = -1, -1
        for i in range(len(path)):
            for j in range(i+1, len(path)):
                sz = j - i
                if sz <= max: continue
                piece = path[i:j]
                if any(x in piece for x in "ABC"): continue
                if len(",".join(piece)) > 20: continue

                for k in range(j, len(path)):
                    if piece == path[k:k+sz]:
                        max = sz
                        maxi, maxj = i, j

        parts.append(path[maxi:maxj])
        path = ",".join(path).replace(",".join(path[maxi:maxj]), part).split(",")

    input = "\n".join([",".join(x) for x in [path] + parts] + ["n\n"])
    print(input)

    interp = IntCode(p)
    interp.program[0] = 2
    out = interp.run([ord(x) for x in input])
    assert interp.done

    print(part1)
    print(out[-1])


if __name__ == '__main__':
    sys.exit(main(sys.argv))
