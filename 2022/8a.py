#!/usr/bin/env python3

import sys

def main(args):
    data = [[int(c) for c in s.rstrip('\n')] for s in sys.stdin]

    N = len(data)
    M = len(data[0])

    num = 0
    for i in range(N):
        for j in range(M):
            h = data[i][j]
            x = 0
            if (
                h > max([-1] + data[i][:j])
                or h > max([-1] + (data[i][j+1:]))
                or h > max([-1] + [data[k][j] for k in range(0, i)])
                or h > max([-1] + [data[k][j] for k in range(i+1, N)])
            ):
                x = 1
                num += 1

    print(num)

if __name__ == '__main__':
    main(sys.argv)
