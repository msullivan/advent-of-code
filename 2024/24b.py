#!/usr/bin/env python3

import sys
from collections import defaultdict, Counter, deque
# from parse import parse
import re
import math
import itertools
import heapq
import random

def extract(s):
    return [int(x) for x in re.findall(r'(-?\d+).?', s)]

def vadd(v1, v2):
    if len(v1) == 2:
        return v1[0] + v2[0], v1[1] + v2[1]
    elif len(v1) == 3:
        return v1[0] + v2[0], v1[1] + v2[1], v1[2] + v2[2]
    else:
        # ... this is so slow.
        return tuple([x + y for x, y in zip(v1, v2)])

def ichr(i):
    return chr(ord('a') + i)

def iord(c):
    return ord(c.lower()) - ord('a')

def optidx(d, opt=max, nth=0):
    if not isinstance(d, dict):
        d = dict(enumerate(d))
    rv = opt(d.values())
    return [i for i, v in d.items() if v == rv][nth], rv

LETTERS = "abcdefghijklmnopqrstuvwxyz"

UP, RIGHT, DOWN, LEFT = VDIRS = (0, -1), (1, 0), (0, 1), (-1, 0),
DIRS = {'N': UP, 'E': RIGHT, 'S': DOWN, 'W': LEFT }
ALL_DIRS = [(x, y) for x in [-1,0,1] for y in [-1,0,1] if not x == y == 0]

def gnbrs(s, dirs=VDIRS):
    return [(dir, vadd(s, dir)) for dir in dirs]

def turn(v, d='left'):
    n = -1 if d == 'left' else 1
    return VDIRS[(VDIRS.index(v) + n) % len(VDIRS)]


##############################

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

    lordering = list(ordering)

    return ordering, lordering


def test(evals, bits):
    for _ in range(50):
        x = random.getrandbits(bits)
        y = random.getrandbits(bits)
        # x = y = 511
        # print(x, '+', y)
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
    # data = [int(s.rstrip('\n')) for s in file]
    # data = [s.rstrip('\n') for s in file]

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

    ex1, ex2 = 'gwh', 'z09'
    evals[ex1], evals[ex2] = evals[ex2], evals[ex1]

    flipped = [ex1, ex2]

    ex1, ex2 = 'wgb', 'wbw'
    evals[ex1], evals[ex2] = evals[ex2], evals[ex1]
    flipped.extend([ex1, ex2])

    ex1, ex2 = 'z21', 'rcb'
    evals[ex1], evals[ex2] = evals[ex2], evals[ex1]
    flipped.extend([ex1, ex2])

    ex1, ex2 = 'z39', 'jct'
    evals[ex1], evals[ex2] = evals[ex2], evals[ex1]
    flipped.extend([ex1, ex2])


    # asdf
    ordering, _ = analyze(evals)
    for v in ordering:
        x1, op, x2 = evals[v]
        print(f'{x1} {op} {x2} -> {v}')
        if v[0] == 'z':
            print()


    test(evals, 44)

    print(','.join(sorted(flipped)))

    return


    # should be all 1s
    v = run(vals, evals, ~0, 0)
    print(bin(v))
    for i in range(45):
        if v & (1 << i) == 0:
            break
    print('FIRST FUCKED', i)
    first_broken = i

    deps = get_deps(evals, f'z{i:02}')
    edeps = get_deps(evals, f'z{i-1:02}')
    print(deps)
    # print(len(deps), len(set(deps)))
    exdeps = [d for d in deps if d not in edeps and d in evals]
    print(exdeps)
    # exdeps = sorted(list({d for d in deps if d in evals}))
    # print(exdeps)

    ok = False
    for i, ex1 in enumerate(exdeps):
        for ex2 in exdeps[i+1:]:
            evals2 = evals.copy()
            evals2[ex1], evals2[ex2] = evals2[ex2], evals2[ex1]
            v = run(vals, evals2, ~0, 0)
            if v is not None:
                # print('CHECK', bin(v))
                mask = (1 << (first_broken+1)) - 1
                if v & mask == mask:
                    print("OK!!!", ex1, ex2)
                    ok = True
                    break
        if ok:
            break

    assert ok

    first_pair = ex1, ex2
    flipped = [*first_pair]
    print(first_pair)
    print(ex1, evals[ex1])
    print(ex2, evals[ex2])


    v = run(vals, evals, ~0, 0)
    print(bin(v), 'FIRST AGAIN')

    print("CHECK AGAIN")
    v = run(vals, evals2, 0, 0)
    print(bin(v))
    v = run(vals, evals2, ~0, 0)
    print(bin(v))
    v = run(vals, evals2, 0, ~0)
    print(bin(v))
    v = run(vals, evals2, ~0, ~0)
    print(bin(v))

    print()

    exdeps = [d for d in deps if d not in first_pair and d in evals]
    evals2_o = evals2

    import random

    asdf = []
    ok = False
    for i, ex1 in enumerate(exdeps):
        # for ex2 in exdeps[i+1:]:
        for ex2 in evals.keys():
            if ex2 == ex1 or ex2 in flipped:
                continue
            evals2 = evals2_o.copy()
            evals2[ex1], evals2[ex2] = evals2[ex2], evals2[ex1]

            print("TRY", ex1, ex2)
            passed = 0
            for _ in range(50):
                x = random.getrandbits(first_broken)
                y = random.getrandbits(first_broken)
                # x = y = 511
                print(x, '+', y)
                mask = ((1 << (first_broken+1)) - 1)
                ex_z = (x + y) & mask
                run_z = run(vals, evals2, x, y)
                if run_z is None:
                    break
                actual_z = run_z  & mask
                if ex_z != actual_z:
                    break
                    for v in [x, y, ex_z, actual_z]:
                        print(f'{v:020b}')
                    # print(f{)
                    # print(bin(y))
                    # print(bin(ex_z))
                    # print(bin(actual_z))
                    assert ex_z == actual_z, (ex_z, actual_z)
                passed += 1
            else:
                print('???', passed)
                asdf.append((ex1, ex2))
                # ok = True
                # break
        if ok:
            break

    print(asdf)
    assert ok
    print(ok, ex1, ex2)
    flipped += [ex1, ex2]
    print(flipped)


    print("CHECK AGAIN")
    v = run(vals, evals2, 0, 0)
    print(bin(v))
    v = run(vals, evals2, ~0, 0)
    print(bin(v))
    v = run(vals, evals2, 0, ~0)
    print(bin(v))
    v = run(vals, evals2, ~0, ~0)
    print(bin(v))


    # print(bin(v))
    # for i in range(1, 45):
    #     if v & (1 << i) == 0:
    #         break
    # print('SECOND FUCKED', i)
    # second_broken = i

    # deps = get_deps(evals2, f'z{i:02}')
    # edeps = get_deps(evals2, f'z{i-1:02}')

    # print(deps)
    # ideps = sorted([d for d in deps if d[0] in 'xy'])
    # print("ideps", ideps)

    # print(len(deps), len(set(deps)))
    # exdeps = [d for d in deps if d not in edeps and d in evals]
    # print(exdeps)
    # print(evals['z10'])
    # assert len(exdeps) == 2
    # ex1, ex2 = exdeps

    # evals3 = evals2.copy()
    # evals3[ex1], evals3[ex2] = evals3[ex2], evals3[ex1]
    # v = run(vals, evals3, ~0, 0)
    # print(bin(v))

    # v = run(vals, evals3, ~0, ~0)
    # print(bin(v))


if __name__ == '__main__':
    main(sys.argv)
