#!/usr/bin/env python3

import sys

def main(args):
    data = [[int(c) for c in s.rstrip('\n')] for s in sys.stdin]

    N = len(data)
    M = len(data[0])

    scs = []
    num = 0
    for i in range(N):
        for j in range(M):

            h = data[i][j]
            x = 0

            a = [(i+(x!=10),x) for i, x in enumerate(reversed([10] + data[i][:j])) if x >= h]
            b = [(i+(x!=10),x) for i, x in enumerate(((data[i][j+1:] + [10]))) if x >= h]

            up = [data[k][j] for k in range(0, i)]
            down = [data[k][j] for k in range(i+1, N)]

            c = [(i+(x!=10),x) for i, x in enumerate(reversed([10] + up)) if x >= h]
            d = [(i+(x!=10),x) for i, x in enumerate(((down + [10]))) if x >= h]
            # print(a, b, c, d)
            score = a[0][0]*b[0][0]*c[0][0]*d[0][0]
            scs.append(score)

    print(max(scs))


if __name__ == '__main__':
    main(sys.argv)
