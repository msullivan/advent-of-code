#!/usr/bin/env python3
# I wrote this after part 2

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
        opt.add(sum([ps[j] for j, b in enumerate(buttons) if i in b]) % 2 == t)

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
    data = [l.split(' ')[0:-1] for l in file]
    buttons = [[extract(x) for x in xs[1:]] for xs in data]
    target = [xs[0] for xs in data]
    target = [[int(x == '#') for x in xs[1:-1]] for xs in target]
    res = sum(solve(buttons, target) for buttons, target in zip(buttons, target))
    print(res)


if __name__ == '__main__':
    main(sys.argv)
