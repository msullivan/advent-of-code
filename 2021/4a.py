#!/usr/bin/env python3

import sys

import re

def extract(s, pos=False):
    p = '' if pos else '-?'
    return [int(x) for x in re.findall(fr'{p}\d+', s)]

def solved(board):
    for i in range(5):
        if all(board[i][j] is None for j in range(5)):
            return True
    for i in range(5):
        if all(board[j][i] is None for j in range(5)):
            return True

def main(args):
    # data = [x.split('\n') for x in sys.stdin.read().split('\n\n')]
    # data = [int(s.strip()) for s in sys.stdin]
    data = [s.strip() for s in sys.stdin]

    nums = extract(data[0])
    rest = "\n".join(data[1:]).split("\n\n")
    things = []
    for thing in rest:
        # print(repr(thing))
        things.append([extract(s) for s in thing.split('\n')])
        if not things[-1][0]:
            things[-1].pop(0)


    boards = things

    for num in nums:
        for board in boards:
            for i in range(5):
                for j in range(5):

                    if board[i][j] == num:
                        board[i][j] = None

        for board in boards:
            if solved(board):
                left = [x for y in board for x in y  if x is not None]
                ss = sum(left)
                print(ss * num)
                return




if __name__ == '__main__':
    sys.exit(main(sys.argv))
