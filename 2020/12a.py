#!/usr/bin/env python3

import sys
import re

def extract(s):
    return [int(x) for x in re.findall(r'-?\d+', s)]

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

DIRS = { 'E': RIGHT, 'W': LEFT, 'N': UP, 'S': DOWN }
ROT = 'NESW'

def add(v1, v2):
    return tuple(x + y for x, y in zip(v1, v2))

def mul(k, v2):
    return tuple(k * y for y in v2)


def main(args):
    # data = [x.split('\n') for x in sys.stdin.read().split('\n\n')]
    data = [s.strip() for s in sys.stdin]

    pos = (0, 0)
    dir = 'E'
    for line in data:
        cmd = line[0]
        arg = int(line[1:])
        if cmd in DIRS:
            pos = add(pos, mul(arg, DIRS[cmd]))
        elif cmd in 'LR':
            arg //= 90
            i = ROT.index(dir)
            m = 1 if cmd == 'R' else -1
            i += m*arg
            dir = ROT[i % 4]
        elif cmd == 'F':
            pos = add(pos, mul(arg, DIRS[dir]))

    print(pos)
    # My original solution had this and worked, lol
    # print(abs(pos[0] + pos[1]))
    print(abs(pos[0]) + abs(pos[1]))

if __name__ == '__main__':
    sys.exit(main(sys.argv))
