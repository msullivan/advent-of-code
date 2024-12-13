#!/usr/bin/env python3

import sys
import re
import math

import numpy as np

def extract(s):
    return [int(x) for x in re.findall(r'(-?\d+).?', s)]

def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    data = [x.rstrip('\n').split('\n') for x in file.read().split('\n\n')]

    ans = 0
    for group in data:
        xa, ya = extract(group[0])
        xb, yb = extract(group[1])
        xt, yt = extract(group[2])
        xt += 10000000000000
        yt += 10000000000000

        lhs = np.array([[xa, xb], [ya, yb]], dtype=np.int64)
        rhs = np.array([xt, yt], dtype=np.int64)
        x = np.linalg.solve(lhs, rhs)
        A, B = x
        print(A, B)
        iA = int(round(A))
        iB = int(round(B))
        # This was my first take and it was horrific. 1e-2 to 1e-4 for
        # abs_tol work, but 1e-5 doesn't. But how are you supposed to
        # figure that out?? 1e-2 working surprised me.
        # if (
        #     math.isclose(iA, A, rel_tol=0, abs_tol=1e-2)
        #     and math.isclose(iB, B, rel_tol=0, abs_tol=1e-2)
        #     and A > 0
        #     and B > 0
        # ):
        # Instead, just check that the equation holds with them rounded to int
        if (
            iA*xa + iB*xb == xt
            and iA*ya + iB*yb == yt
            and A > 0
            and B > 0
        ):
            print('!', A, B)
            ans += 3*iA + iB

    print(ans)



if __name__ == '__main__':
    main(sys.argv)
