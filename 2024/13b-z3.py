#!/usr/bin/env python3

import sys
import re
from z3 import Int, Optimize, sat

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

        opt = Optimize() # ??
        A, B = Int('A'), Int('B')
        opt.add(A*xa + B*xb == xt)
        opt.add(A*ya + B*yb == yt)
        opt.add(A >= 0)
        opt.add(B >= 0)
        opt.minimize(A*3 + B)

        if opt.check() != sat:
            continue
        model = opt.model()
        print(model)
        ans += model[A].as_long()*3 + model[B].as_long()

    print(ans)



if __name__ == '__main__':
    main(sys.argv)
