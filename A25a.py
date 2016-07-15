#!/usr/bin/env python3

import sys, json

def calc(cnt):
    v = 20151125
    for i in range(cnt-1):
        v = (v * 252533) % 33554393
    return v


def main(args):
    N = 6100
    board = [[0]*N for i in range(N)]
    n = 1
    for i in range(N):
        for j in range(i):
            board[i-j-1][j] = n
            n += 1

    cnt = board[2978-1][3083-1]

    print(calc(1))
    print(calc(2))
    print(calc(3))
    print(calc(cnt))

#    print(board)

if __name__ == '__main__':
    sys.exit(main(sys.argv))


    # 0, 0
    # 1, 0
    # 0, 1
    # 2, 0
    # 1, 1
    # 0, 2
