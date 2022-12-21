#!/usr/bin/env python3

import sys
from collections import defaultdict
import re
from z3 import Int, If, Optimize

def extract(s):
    return [int(x) for x in re.findall(r'(-?\d+).?', s)]

def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    data = [s.rstrip('\n') for s in file]

    numbers = {}
    ops = {}
    opt = Optimize() # ??
    for line in data:
        x, y = line.split(': ')
        thing = Int(x)
        numbers[x] = thing

    for line in data:
        x, y = line.split(': ')
        nums = extract(line)
        if x == 'humn':
            pass
        elif nums:
            opt.add(numbers[x] == nums[0])
        else:
            a, op, b = y.split(' ')
            na, nb = numbers[a], numbers[b]
            if x == 'root':
                eq = na == nb
            elif op == '+':
                eq = na + nb
            elif op == '-':
                eq = na - nb
            elif op == '*':
                eq = na * nb

            if x == 'root':
                opt.add(eq)
            elif op == '/':
                # Have to have it turned into multiplication or it might produce
                # multiple valid answers!
                # ... for my competition solve I just used division though
                # and I got away with it
                opt.add(na == numbers[x] * nb)
            else:
                opt.add(numbers[x] == eq)

    z = opt.check()
    print(z)
    model = opt.model()
    print(model[numbers['humn']].as_long())

if __name__ == '__main__':
    main(sys.argv)
