#!/usr/bin/env python3

from collections import defaultdict, deque
import sys
import re
#from dataclasses import dataclass

def extract(s):
    return [int(x) for x in re.findall(r'-?\d+', s)]

def dist(x, y):
    return abs(x[0] - y[0]) + abs(x[1] - y[1]) + abs(x[2] - y[2]) + abs(x[3] - y[3])

def main(args):
    data = [extract(s.strip()) for s in sys.stdin]

    constos = []

    for line in data:
        match = None
        for i in range(len(constos)):
            consto = constos[i]
            if consto and any(dist(x, line) <= 3 for x in consto):
                if match is None:
                    match = consto
                    match.append(line)
                else:
                    match.extend(consto)
                    constos[i] = None
        if match is None:
            constos.append([line])

    print(len([x for x in constos if x]))

if __name__ == '__main__':
    sys.exit(main(sys.argv))
