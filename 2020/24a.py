#!/usr/bin/env python3

from collections import defaultdict

import sys
import re

def add(v1, v2):
    return tuple(x + y for x, y in zip(v1, v2))

def extract(s):
    return [int(x) for x in re.findall(r'-?\d+', s)]

dirs = {
    'e': (1, -1, 0),
    'w': (-1, 1, 0),
    'ne': (1, 0, -1),
    'nw': (0, 1, -1),
    'se': (0, -1, 1),
    'sw': (-1, 0, 1),
}

def split(x):
    i = 0
    while i < len(x):
        if x[i] in 'ns':
            yield x[i:i+2]
            i += 2
        else:
            yield x[i]
            i += 1

def main(args):
    # data = [x.split('\n') for x in sys.stdin.read().split('\n\n')]
    data = [list(split(s.strip())) for s in sys.stdin]

    # white is false
    map = defaultdict(bool)
    for path in data:
        coord = 0, 0, 0
        for step in path:
            coord = add(coord, dirs[step])
        map[coord] = not map[coord]

    print(map)
    print(len([x for x in map.values() if x]))

    # print(data)

if __name__ == '__main__':
    sys.exit(main(sys.argv))
