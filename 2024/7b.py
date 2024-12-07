#!/usr/bin/env python3

import sys
import re
import itertools

def extract(s):
    return [int(x) for x in re.findall(r'(-?\d+).?', s)]

def test(mask, vals, tgt):
    v = vals[0]
    for j, n in enumerate(vals[1:]):
        if mask[j] == '+':
            v += n
        elif mask[j] == '*':
            v *= n
        else:
            v = int(str(v) + str(n))
        if v > tgt:
            return False
    return v == tgt


def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    data = [s.rstrip('\n') for s in file]

    score = 0
    for i, line in enumerate(data):
        print(i, line)
        tgt, *vals = extract(line)
        n = len(vals) - 1
        cnt = 0
        for asdf in itertools.product(*['+*|'] * n):
            if test(asdf, vals, tgt):
                score += tgt
                break

    print(score)

if __name__ == '__main__':
    main(sys.argv)
