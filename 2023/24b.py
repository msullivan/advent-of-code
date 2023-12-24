#!/usr/bin/env python3

import sys
import re
from z3 import Real, Solver

# My first take at this used Int instead of Real, and ran for an hour
# without finishing. Then I reversed the input and it finished
# instantly. Fuck around and find out, I guess.
#
# Switching it to Real seems more legit I guess.

def extract(s):
    return [int(x) for x in re.findall(r'(-?\d+).?', s)]

def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin

    data = [extract(s.rstrip('\n')) for s in file]
    data = [(tuple(x[:3]), tuple(x[3:])) for x in data]

    solve = Solver()
    Ntyp = Real

    sx0 = Ntyp('sx0')
    sy0 = Ntyp('sy0')
    sz0 = Ntyp('sz0')

    vx0 = Ntyp('vx0')
    vy0 = Ntyp('vy0')
    vz0 = Ntyp('vz0')
    s0 = [sx0, sy0, sz0]
    v0 = [vx0, vy0, vz0]

    ts = []
    for i, (si, vi) in enumerate(data):
        ti = Ntyp('t' + str(i))
        for i in range(3):
            solve.add(s0[i] + v0[i] * ti == si[i] + vi[i] * ti)

    print(solve)
    print(solve.check())
    model = solve.model()
    print(model)
    print(tuple(model[k].as_long() for k in s0))
    print(tuple(model[k].as_long() for k in v0))
    print(sum(model[k].as_long() for k in s0))


if __name__ == '__main__':
    main(sys.argv)
