#!/usr/bin/env python3

import sys
import re
import time
import itertools
import copy
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

def draw(painted):
    minx = min(x for x, y in painted)
    miny = min(y for x, y in painted)
    maxx = max(x for x, y in painted)
    maxy = max(y for x, y in painted)
    for y in range(miny, maxy+1):
        l = ""
        for x in range(minx, maxx+1):
            l += painted[x,y]
        print(l)


def go(interp, input):
    output = interp.run(input)
    groups = [output[i:i+3] for i in range(0, len(output), 3)]
    score = next((b for x, y, b in groups if x == -1), None)
    return {(x, y): " |#_*"[b] for x, y, b in groups if x >= 0}, score

def get_stuff(board):
    ball_coord = next(k for k, v in board.items() if v == "*")
    paddle_coord = next(k for k, v in board.items() if v == "_")  # XXX:
    return ball_coord, paddle_coord

def main(args):
    data = [s.strip() for s in open("13.input")]
    lp = [int(x) for x in data[0].split(",")]
    p = defaultdict(int, [(i, x) for i, x in enumerate(lp)])

    # Part 1
    interp = IntCode(p)
    output = interp.run([])
    groups = [output[i:i+3] for i in range(0, len(interp.output), 3)]
    part1 = len([x for x in groups if x[2] == 2])

    # Part 2
    interp = IntCode(p)
    interp.program[0] = 2

    press = 0
    board = defaultdict(lambda: " ")

    step = 0

    board.update(go(interp, [])[0])
    draw(board)

    last = interp.program.copy()
    lol = None
    while not interp.done:
        new_board, _ = go(copy.deepcopy(interp), [0])
        aboard = board.copy()
        aboard.update(new_board)
        next_ball_coord, next_paddle_coord = get_stuff(aboard)

        ball_coord, paddle_coord = get_stuff(board)

        press = next_ball_coord[0] - next_paddle_coord[0]
        if ball_coord[1] + 1 == paddle_coord[1] and ball_coord[0] == paddle_coord[0]:
            press = 0
        if press:
            press = press // abs(press)


        # ball_coord, paddle_coord = get_stuff(board)

        print("Ball:", ball_coord)
        print("Paddle:", paddle_coord)
        print("Press:", press)

# #        print("HACKS:", [k for k, v in board.items() if v == last[k]])
#         hack = {k for k, v in interp.program.items() if v == paddle_coord[0]}
#         print("HACKS:", hack)
#         if lol is not None:
#             lol &= hack
#         else:
#             lol = hack
#         print("LOL:", lol)

        # print("Move: ", end='')
        # sys.stdout.flush()
        # move = sys.stdin.readline().strip()
        # press = 1 if move == "d" else -1 if move == "a" else 0

        #interp.program[392] = ball_coord[0]
        #press = 0
        real_new_board, score = go(interp, [press])
        board.update(real_new_board)

        print("====================", step)
        draw(board)
        if score is not None:
            print("Score:", score)

        press = 0
        step += 1

    print(part1)
    print(score)


if __name__ == '__main__':
    sys.exit(main(sys.argv))
