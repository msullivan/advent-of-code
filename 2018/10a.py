#!/usr/bin/env python3

import sys
from collections import defaultdict, deque

input = 2694
#input = 18

def eval(x, y, input):
    power = ((x + 10) * y + input) * (x + 10)
    power = (power % 1000) // 100
    power -= 5
    return power


def main(args):
    vals = {}
    for x in range(1, 301):
        for y in range(1, 301):
            vals[(x,y)] = eval(x, y, input)

    things = []
    for x in range(1, 299):
        for y in range(1, 299):
            lol = [(x+i,y+j) for i in range(3) for j in range(3)]
            val = sum(vals.get(z) for z in lol)
            things += [(val, (x, y))]
    print(max(things))

if __name__ == '__main__':
    sys.exit(main(sys.argv))
