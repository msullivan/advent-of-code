#!/usr/bin/env python3

import sys

dirs = {
    'n': (0, 1, -1),
    's': (0, -1, 1),
    'ne': (1, 0, -1),
    'nw': (-1, 1, 0),
    'se': (1, -1, 0),
    'sw': (-1, 0, 1),
}

def main(args):
    data = [s.strip() for s in sys.stdin]
    moves = data[0].split(",")

    x,y,z = 0,0,0
    farthest = 0
    for move in moves:
       dx,dy,dz = dirs[move]
       x+=dx
       y+=dy
       z+=dz

       farthest = max(farthest, max(map(abs,(x,y,z))))

    print(max(map(abs,(x,y,z))))
    print(farthest)

if __name__ == '__main__':
    sys.exit(main(sys.argv))
