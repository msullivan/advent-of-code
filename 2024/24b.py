#!/usr/bin/env python3

import sys
import random


def run(vals, evals, x=None, y=None):
    vals = dict(vals)
    evals = dict(evals)

    if x is not None:
        for i in range(45):
            vals[f'x{i:02}'] = x & 1
            x >>= 1
    if y is not None:
        for i in range(45):
            vals[f'y{i:02}'] = y & 1
            y >>= 1


    def eval(v):
        if v in vals:
            return vals[v]

        v1, op, v2 = evals[v]
        n1 = eval(v1)
        n2 = eval(v2)
        if op == 'AND':
            r = n1 & n2
        elif op == 'OR':
            r = n1 | n2
        else:
            r = n1 ^ n2
        vals[v] = r
        return r

    names = vals.keys() | evals.keys()
    zs = [z for z in names if z[0] == 'z']
    zs.sort()
    zs.reverse()

    v = 0
    for z in zs:
        v <<= 1
        try:
            v |= eval(z)
        except RecursionError:
            return None

    return v


def get_deps(exprs, v):
    if v not in exprs:
        return [v]
    x1, _, x2 = exprs[v]
    # return [x1, x2] + get_deps(exprs, x1) + get_deps(exprs, x2)
    return [v] + get_deps(exprs, x1) + get_deps(exprs, x2)


def analyze(evals):
    ordering = {}
    def order(evals, x):
        if x in evals and x not in ordering:
            x1, _, x2 = evals[x]
            order(evals, x1)
            order(evals, x2)
            ordering[x] = len(ordering)

    for v in sorted(evals):
        if v[0] == 'z':
            order(evals, v)

    return ordering


def test(evals, bits):
    for _ in range(50):
        x = random.getrandbits(bits)
        y = random.getrandbits(bits)
        mask = ((1 << bits) - 1)
        ex_z = (x + y) & mask
        run_z = run({}, evals, x, y)
        if run_z is None:
            break
        actual_z = run_z  & mask
        if ex_z != actual_z:
            for v in [x, y, ex_z, actual_z]:
                print(f'{v:020b}')
            assert ex_z == actual_z, (ex_z, actual_z)


def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    data = [x.rstrip('\n').split('\n') for x in file.read().split('\n\n')]

    inits = data[0]
    exprs = data[1]

    vals = {}
    for init in inits:
        n, v = init.split(': ')
        vals[n] = int(v)

    evals = {}
    for cmd in exprs:
        v1, op, v2, _, res = cmd.split(' ')
        evals[res] = v1, op, v2

    oevals = dict(evals)

    flipped = []

    # I used the pretty printer to manually inspect it, and the test
    # function to validate.
    ex1, ex2 = 'gwh', 'z09'
    evals[ex1], evals[ex2] = evals[ex2], evals[ex1]
    flipped.extend([ex1, ex2])

    ex1, ex2 = 'wgb', 'wbw'
    evals[ex1], evals[ex2] = evals[ex2], evals[ex1]
    flipped.extend([ex1, ex2])

    ex1, ex2 = 'z21', 'rcb'
    evals[ex1], evals[ex2] = evals[ex2], evals[ex1]
    flipped.extend([ex1, ex2])

    ex1, ex2 = 'z39', 'jct'
    evals[ex1], evals[ex2] = evals[ex2], evals[ex1]
    flipped.extend([ex1, ex2])

    # Print it out
    ordering = analyze(evals)
    for v in ordering:
        x1, op, x2 = evals[v]
        print(f'{x1} {op} {x2} -> {v}')
        if v[0] == 'z':
            print()


    for i in range(44):
        print('==', i)
        test(evals, i)

    print(','.join(sorted(flipped)))


if __name__ == '__main__':
    main(sys.argv)
