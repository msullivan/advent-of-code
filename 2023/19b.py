#!/usr/bin/env python3

import sys
import re

def extract(s):
    return [int(x) for x in re.findall(r'(-?\d+).?', s)]

NUMS = {'x': 0, 'm': 1, 'a': 2, 's': 3}


def set(obj, i, v):
    obj = list(obj)
    obj[i] = v
    return tuple(obj)


def split(op, obj):
    num = extract(op)[0]
    key = NUMS[op[0]]

    if '>' in op:
        num += 1

    lo, hi = obj[key]
    if hi <= num:
        rt, rf = obj, None
    elif lo > num:
        rt, rf = None, obj
    else:
        assert lo <= num < hi
        lsplit = lo, num
        rsplit = num, hi
        rt, rf = set(obj, key, lsplit), set(obj, key, rsplit)

    if '>' in op:
        rt, rf = rf, rt

    return rt, rf


def apply(rules, obj):
    queue = [('in', obj)]
    accepted = []
    while queue:
        r, obj = queue.pop()
        print(r, obj)
        if r == 'R':
            continue
        if r == 'A':
            accepted.append(obj)
            continue

        rx = rules[r]
        cmds = rx.split(',')
        for cmd in cmds:
            if ':' not in cmd:
                queue.append((cmd, obj))
                break

            op, tgt = cmd.split(':')

            rt, rf = split(op, obj)
            if rt:
                queue.append((tgt, rt))
            if rf:
                obj = rf
            else:
                assert 0
                break

    return accepted


def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    data = [x.rstrip('\n').split('\n') for x in file.read().split('\n\n')]

    rules, objs = data
    drules = {}
    for r in rules:
        n, x = r.split('{')
        drules[n] = x[:-1]

    rules = drules

    sobjs = objs
    objs = []

    obj = tuple((1, 4001) for _ in range(4))
    acc = apply(rules, obj)

    res = 0
    for obj in acc:
        mul = 1
        for x, y in obj:
            mul *= (y-x)
        res += mul

    print(res)


if __name__ == '__main__':
    main(sys.argv)
