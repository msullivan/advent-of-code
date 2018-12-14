#!/usr/bin/env python3

import sys
from collections import defaultdict, deque
#from dataclasses import dataclass

def main(args):
    data = [s.strip() for s in sys.stdin]

    initial = data[0].split(" ")[2]
    stuff = [x.split(' ') for x in data[2:]]
    stuff = dict([(x, z) for x, _, z in stuff])

    plants = defaultdict(lambda: '.')
    for i, x in enumerate(initial):
        plants[i] = x

    for i in range(200):
        print(''.join(plants[j] for j in range(-50, 150)))

        new = defaultdict(lambda: '.')
        bottom = min(plants.keys())
        top = max(plants.keys())
        for j in range(bottom-3, top+3):
            key = "".join(plants[k] for k in range(j-2, j+3))
            assert len(key) == 5
            new[j] = stuff[key]
        plants = new

#    print([k for k, v in stuff.items() if v == '#'])
    print(sum(k for k, v in plants.items() if v == '#'))

    # print(initial)
    # print(stuff)

if __name__ == '__main__':
    sys.exit(main(sys.argv))
