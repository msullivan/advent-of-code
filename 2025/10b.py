#!/usr/bin/env python3

import sys
import re
from z3 import Int, Optimize, sat

def extract(s):
    return [int(x) for x in re.findall(r'(-?\d+).?', s)]


def solve(buttons, target):
    print(buttons)
    print(target)
    ps = [Int(f'P{i}') for i in range(len(buttons))]
    v = Int('sum')

    opt = Optimize() # ??
    for p in ps:
        opt.add(p >= 0)
    for i, t in enumerate(target):
        opt.add(sum([ps[j] for j, b in enumerate(buttons) if i in b]) == t)

    opt.add(v == sum(ps))
    opt.minimize(v)
    assert opt.check() == sat
    model = opt.model()

    print(model)
    res = model[v].as_long()
    print(res)
    return res


def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    data = [l.split(' ')[1:] for l in file]
    data = [[extract(x) for x in xs] for xs in data]
    res = sum(solve(buttons, target) for *buttons, target in data)
    print(res)


if __name__ == '__main__':
    main(sys.argv)
