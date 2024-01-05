#!/usr/bin/env python3

import sys
from collections import defaultdict
from intcode import IntCode


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
    p = [int(x) for x in data[0].split(",")]

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

    while not interp.done:
        ball_coord, paddle_coord = get_stuff(board)

        press = ball_coord[0] - paddle_coord[0]
        if press:
            press = press // abs(press)

        # print("Move: ", end='')
        # sys.stdout.flush()
        # move = sys.stdin.readline().strip()
        # press = 1 if move == "d" else -1 if move == "a" else 0

        real_new_board, score = go(interp, [press])
        board.update(real_new_board)

        # print("\x1b[2J")
        # print("====================", step)
        # print("Ball:", ball_coord)
        # print("Paddle:", paddle_coord)
        # print("Press:", press)
        # print("Score:", score)
        # draw(board)

        press = 0
        step += 1

    print(part1)
    print(score)


if __name__ == '__main__':
    sys.exit(main(sys.argv))
