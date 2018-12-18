#!/usr/bin/env python3

import sys
from collections import defaultdict, deque
from dataclasses import dataclass

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

CYCLE = [UP, RIGHT, DOWN, LEFT]

# /
FORWARD_SLASH = { UP: RIGHT, RIGHT: UP, LEFT: DOWN, DOWN: LEFT }
# \
BACK_SLASH = { UP: LEFT, LEFT: UP, DOWN: RIGHT, RIGHT: DOWN }
DIRS = { '>': RIGHT, '<': LEFT, '^': UP, 'v': DOWN }

@dataclass
class Cart:
    dir: object
    pos: object
    turn: int = 0
    dead: bool = False


def main(args):
    data = [list(s.rstrip('\n')) for s in sys.stdin]
    print(data)

    noobs = []
    for y in range(len(data)):
        for x in range(len(data[0])):
            c = data[y][x]
            if c in DIRS:
                noob = Cart(DIRS[c], (x, y))
                noobs.append(noob)
                data[y][x] = '|' if c in 'v^' else '-'

    while True:
        order = sorted(noobs, key=lambda x: (x.pos[1], x.pos[0]))
        for noob in order:
            if noob.dead: continue

            noob.pos = (noob.pos[0] + noob.dir[0], noob.pos[1] + noob.dir[1])
            x, y = noob.pos
            if data[y][x] == '/':
                noob.dir = FORWARD_SLASH[noob.dir]
            elif data[y][x] == '\\':
                noob.dir = BACK_SLASH[noob.dir]
            elif data[y][x] == '+':
                turn = (noob.turn % 3) - 1
                noob.dir = CYCLE[(CYCLE.index(noob.dir) + turn) % 4]
                noob.turn += 1

            lol = (other for other in noobs if other.pos == noob.pos and other is not noob)
            for other in lol:
                other.dead = noob.dead = True
                noobs.remove(other)
                noobs.remove(noob)
                print('boom {},{}'.format(x, y))

        if len(noobs) == 1:
            x, y = noobs[0].pos
            print('{},{}'.format(x, y))
            return



    print(noobs)



if __name__ == '__main__':
    sys.exit(main(sys.argv))
