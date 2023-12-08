#!/usr/bin/env python3

import sys

def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    data = [s.rstrip('\n') for s in file]

    dirs = data[0]
    d = {}
    for line in data[2:]:
        x, yz = line.split(" = (")
        y, z = yz.split(", ")
        z = z.replace(")", "")
        d[x] = (y, z)

    steps = 0
    node = 'AAA'
    while node != 'ZZZ':
        s = dirs[steps % len(dirs)]
        r = s == 'R'
        node = d[node][r]
        steps += 1

    print(steps)

if __name__ == '__main__':
    main(sys.argv)
