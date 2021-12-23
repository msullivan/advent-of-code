#!/usr/bin/env python3

import sys
from collections import defaultdict
import re

def extract(s):
    return [int(x) for x in re.findall(r'(-?\d+).?', s)]


def main(args):
    data = [s.strip() for s in sys.stdin]

    cmds = [(s.split(" ")[0], extract(s)) for s in data]
    cmds = [(s, ((x[0], x[2], x[4]), (x[1], x[3], x[5]))) for s, x in cmds]

    grids = defaultdict(bool)
    i = 0
    for cmd, ((xmin, ymin, zmin), (xmax, ymax, zmax)) in cmds:
        flag = cmd == "on"
        for x in range(max(xmin, -50), min(xmax, 50)+1):
            for y in range(max(ymin, -50), min(ymax, 50)+1):
                for z in range(max(zmin, -50), min(zmax, 50)+1):
                    grids[x,y,z] = flag
        print(i, sum(grids.values()))

        i += 1

    print(sum(grids.values()))

if __name__ == '__main__':
    main(sys.argv)
