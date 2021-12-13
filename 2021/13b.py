#!/usr/bin/env python3

import sys

import re

def extract(s):
    return [int(x) for x in re.findall(r'(-?\d+).?', s)]

def fold(dot, dir, x):
    if 'x' in dir and dot[0] > x:
        diff = dot[0] - x
        return (x - diff, dot[1])
    if 'y' in dir and dot[1] > x:
        diff = dot[1] - x
        return (dot[0], x - diff)
    return dot

def fold_y(dot, y):
    return dot

def main(args):
    p1, p2 = sys.stdin.read().split("\n\n")

    dots = [tuple(extract(l)) for l in p1.split("\n")]
    instrs = p2.strip().split("\n")

    i1 = extract(instrs[0])[0]
    new = {fold(dot, instrs[0], i1) for dot in dots}
    print(len(new))

    for instr in instrs:
        i1 = extract(instr)[0]
        dots = {fold(dot, instr, i1) for dot in dots}

    max_x = max(x for x, y in dots)
    max_y = max(y for x, y in dots)

    for y in range(max_y+1):
        l = ""
        for x in range(max_x+1):
            c = "#" if (x, y) in dots else " "
            l += c
        print(l)


if __name__ == '__main__':
    main(sys.argv)
