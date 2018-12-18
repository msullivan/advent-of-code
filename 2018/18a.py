#!/usr/bin/env python3

import sys
from collections import defaultdict, deque
#from dataclasses import dataclass

def adj(x, y):
    for i in range(-1, 2):
        for j in range(-1, 2):
            if not (i == 0 and j == 0):
                yield (x+i, y+j)

def main(args):
    data = [s.strip() for s in sys.stdin]
    map = defaultdict(str)

    for y in range(len(data)):
        for x in range(len(data[0])):
            map[x, y] = data[y][x]

    for i in range(10):
        print(i)
        new = defaultdict(str, map)
        for y in range(len(data)):
            for x in range(len(data[0])):
                if map[x, y] == '.':
                    if len([a for a in adj(x, y) if map[a] == '|']) >= 3:
                        new[x, y] = '|'
                elif map[x, y] == '|':
                    if len([a for a in adj(x, y) if map[a] == '#']) >= 3:
                        new[x, y] = '#'
                elif map[x, y] == '#':
                    if not (len([a for a in adj(x, y) if map[a] == '#']) >= 1
                            and len([a for a in adj(x, y) if map[a] == '|']) >= 1):
                        new[x, y] = '.'
        map = new

    wooded = len([x for x in map.values() if x == '|'])
    yards = len([x for x in map.values() if x == '#'])
    print(wooded*yards)

if __name__ == '__main__':
    sys.exit(main(sys.argv))
