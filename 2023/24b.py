#!/usr/bin/env python3

import sys
import re
from z3 import Int, If, Optimize, Solver, simplify

def extract(s):
    return [int(x) for x in re.findall(r'(-?\d+).?', s)]


def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin

    data = [extract(s.rstrip('\n')) for s in file]
    data = [(tuple(x[:3]), tuple(x[3:])) for x in data]

    solve = Solver()
    sx0 = Int('sx0')
    sy0 = Int('sy0')
    sz0 = Int('sz0')

    vx0 = Int('vx0')
    vy0 = Int('vy0')
    vz0 = Int('vz0')
    s0 = [sx0, sy0, sz0]
    v0 = [vx0, vy0, vz0]

    ts = []
    # XXX!!!! on my input, if I reverse it, z3 finishes instantly, and if I don't,
    # it churns for at least an hour.
    # Fuck around and find out, I guess.
    for i, (si, vi) in enumerate(reversed(data)):
        ti = Int('t' + str(i))
        solve.add(ti > 0)
        for i in range(3):
            solve.add(s0[i] + v0[i] * ti == si[i] + vi[i] * ti)

    print(solve)
    print(solve.check())
    model = solve.model()
    print(model)
    print(tuple(model[k].as_long() for k in s0))
    print(sum(model[k].as_long() for k in s0))


if __name__ == '__main__':
    main(sys.argv)
