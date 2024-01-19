#!/usr/bin/env python3

import sys
import re

def extract(s):
    return [int(x) for x in re.findall(r'(-?\d+).?', s)]

def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    data = [s.rstrip('\n') for s in file]

    numbers = {}
    ops = {}

    for line in data:
        x, y = line.split(': ')
        nums = extract(line)
        if nums:
            numbers[x] = nums[0]
        else:
            a, op, b = y.split(' ')
            ops[x] = (a, op, b)

    backup = dict(numbers)
    def go(x):
        if x in numbers:
            return numbers[x]
        a, op, b = ops[x]
        z = eval(f'int({go(a)} {op} {go(b)})')
        numbers[x] = z  # not actually needed; it's just a tree
        return z

    part1 = go('root')

    lhs, _, rhs = ops['root']
    numbers = backup
    del numbers['humn']

    def find_humn(x):
        a, op, b = ops[x]
        try:
            v = go(a)
        except KeyError as e:
            return a, go(b), 0, op
        return b, v, 1, op

    expr, val, _, _ = find_humn('root')
    while expr != 'humn':
        expr, other, which, op = find_humn(expr)
        if op == '+':
            val -= other
        elif op == '*':
            val //= other
        elif op == '-':
            if which == 0:
                val += other
            else:
                val = -(val - other)
        elif op == '/':
            if which == 0:
                val *= other
            else:
                raise AssertionError('denominator!')
        else:
            raise AssertionError('invalid op')

    print(part1)
    print(val)



if __name__ == '__main__':
    main(sys.argv)
