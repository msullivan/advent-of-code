#!/usr/bin/env python3

import sys
import re

def extract(s):
    return [int(x) for x in re.findall(r'(-?\d+).?', s)]

def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    data = [s.rstrip('\n') for s in file]

    cap = {'red': 12, 'green': 13, 'blue': 14}

    p1sum = 0
    p2sum = 0
    for line in data:
        game, rest = line.split(": ")
        parts = [[y.split(' ') for y in x.split(', ')] for x in rest.split('; ')]
        ds = [{k: int(v) for v, k in part} for part in parts]

        ok = all(
            all(v <= cap[k] for k, v in d.items())
            for d in ds
        )
        if ok:
            p1sum += extract(game)[0]

        pwr = 1
        for c in cap:
            pwr *= max(d.get(c, 0) for d in ds)
        p2sum += pwr

    print(p1sum)
    print(p2sum)

if __name__ == '__main__':
    main(sys.argv)
