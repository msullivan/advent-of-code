#!/usr/bin/env python3

import sys
import math

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

    nodes = {s for s in d if s[-1] == 'A'}
    repeat = set()

    snodes = sorted(nodes)

    stops = []
    for node in nodes:
        steps = 0
        while True:
            if node[-1] == 'Z':
                break
            s = dirs[steps % len(dirs)]
            r = s == 'R'
            node = d[node][r]
            steps += 1
        stops.append(steps)

    prod = 1
    for x in stops:
        prod *= x
    print(math.lcm(*stops))


if __name__ == '__main__':
    main(sys.argv)
