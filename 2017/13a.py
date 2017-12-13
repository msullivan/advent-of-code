#!/usr/bin/env python3

import sys

def step(depths, pos, dir):
    for k in depths.keys():
        if pos[k] == depths[k]-1:
            dir[k] = -1
        if pos[k] == 0:
            dir[k] = 1
        pos[k] += dir[k]

def main(args):
    data = [s.strip() for s in sys.stdin]

    depths = {}
    for line in data:
        k, v = map(int, line.split(": "))
        depths[k] = v

    positions = {k: 0 for k in depths.keys()}
    dirs = {k: 1 for k in depths.keys()}


    print(depths)
    print(positions)

    cost = 0
    for i in range(max(depths.keys())+1):
        if i in positions and positions[i] == 0:
            print(i, depths[i])
            cost += i*depths[i]
        step(depths, positions, dirs)

    print(cost)



if __name__ == '__main__':
    sys.exit(main(sys.argv))
