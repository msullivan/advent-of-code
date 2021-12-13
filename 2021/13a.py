#!/usr/bin/env python3

import sys

import re

def extract(s):
    return [int(x) for x in re.findall(r'(-?\d+).?', s)]
def fold_x(dot, x):
    if dot[0] > x:
        diff = dot[0] - x
        return (x - diff, dot[1])
    return dot

def main(args):
    p1, p2 = sys.stdin.read().split("\n\n")

    dots = [tuple(extract(l)) for l in p1.split("\n")]
    instrs = p2.split("\n")

    i1 = extract(instrs[0])[0]
    # does assuming x always work??
    new = {fold_x(dot, i1) for dot in dots}
    print(len(new))


if __name__ == '__main__':
    main(sys.argv)
