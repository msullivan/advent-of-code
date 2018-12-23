#!/usr/bin/env python3

from collections import defaultdict, deque
import sys
import re
#from dataclasses import dataclass

def extract(s):
    return [int(x) for x in re.findall(r'-?\d+', s)]

def dist(x, y):
    return abs(x[0] - y[0]) + abs(x[1] - y[1]) + abs(x[2] - y[2])

def main(args):
    data = [extract(s.strip()) for s in sys.stdin]
    data = [(x[3], tuple(x[:-1])) for x in data]
    m = max(data)
    in_range = [x for x in data if dist(x[1], m[1]) <= m[0]]
    print(len(in_range))


if __name__ == '__main__':
    sys.exit(main(sys.argv))
