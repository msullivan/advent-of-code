#!/usr/bin/env python2

# z3 might have python 3 bindings but they weren't on my laptop from
# the install of z3 left over from grad school so back to python 2 it
# is!


from __future__ import print_function
from z3 import *

import sys
sys.setrecursionlimit(3000)


from collections import defaultdict, deque
import sys
import re
#from dataclasses import dataclass

def extract(s):
    return [int(x) for x in re.findall(r'-?\d+', s)]

def dist(x, y):
    return abs(x[0] - y[0]) + abs(x[1] - y[1]) + abs(x[2] - y[2])

def z3_abs(x):
    return If(x >= 0,x,-x)

def z3_dist(x, y):
    return z3_abs(x[0] - y[0]) + z3_abs(x[1] - y[1]) + z3_abs(x[2] - y[2])

def main(args):
    data = [extract(s.strip()) for s in sys.stdin]
    data = [(x[3], tuple(x[:-1])) for x in data]
    m = max(data)
    in_range = [x for x in data if dist(x[1], m[1]) <= m[0]]
    print(len(in_range))

    x = Int('x')
    y = Int('y')
    z = Int('z')
    orig = (x, y, z)
    cost_expr = x * 0
    for r, pos in data:
        cost_expr += If(z3_dist(orig, pos) <= r, 1, 0)
    opt = Optimize()
    cost = Int('cost')
    opt.add(cost == cost_expr)
    print("let's go")
    h = opt.maximize(cost)
    opt.check()
    opt.lower(h)
    model = opt.model()
    print(model)
    print(dist((0,0,0), (model[x].as_long(), model[y].as_long(), model[z].as_long())))


if __name__ == '__main__':
    sys.exit(main(sys.argv))
