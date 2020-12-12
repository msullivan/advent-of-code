#!/usr/bin/env python3

# this was a friday day 12? really??

import sys

UP = (0, 1)
DOWN = (0, -1)
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
    wpos = (10, 1)
    dir = 'E'
    for line in data:
        cmd = line[0]
        arg = int(line[1:])
        if cmd in DIRS:
            wpos = add(wpos, mul(arg, DIRS[cmd]))
        elif cmd in 'LR':
            arg //= 90
            if cmd == 'L':
                arg = -arg+4

            # 1, 2 becomes 2, -1
            # 2, -1 becomes -1, -2
            for _ in range(arg):
                wpos = (wpos[1], -wpos[0])

        elif cmd == 'F':
            pos = add(pos, mul(arg, wpos))

        print(line, pos, wpos)

    print(pos)
    print(abs(pos[0]) + abs(pos[1]))

if __name__ == '__main__':
    sys.exit(main(sys.argv))
