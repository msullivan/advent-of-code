#!/usr/bin/env python3

import sys

def on(board, i, j):
    if i < 0 or i >= 100 or j < 0 or j >= 100: return False
    return board[i][j] == "#"

def rigcorners(board):
    board[0][0] = board[-1][0] = board[0][-1] = board[-1][-1] = '#'

def evolve(board):
    newboard = [["."]*100 for i in range(100)]

    for i in range(100):
        for j in range(100):
            count = 0
            for a in range(-1,2):
                for b in range(-1,2):
                    if not (a == 0 and b == 0):
                        if on(board, i+a, j+b):
                            count += 1
            if on(board, i, j):
                if count == 2 or count == 3:
                    newboard[i][j] = '#'
                else:
                    newboard[i][j] = '.'
            else:
                if count == 3:
                    newboard[i][j] = '#'
                else:
                    newboard[i][j] = '.'
    rigcorners(newboard)
    return newboard


def main(args):
    board = [[c for c in s.strip()] for s in sys.stdin]

    for i in range(100):
        board = evolve(board)

    count = 0
    for a in board:
        for b in a:
            if b == '#':
                count += 1
    print(count)

if __name__ == '__main__':
    sys.exit(main(sys.argv))
