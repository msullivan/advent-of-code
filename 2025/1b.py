#!/usr/bin/env python3

import sys
from collections import defaultdict, Counter, deque
# from parse import parse
import re
import math
import itertools
import heapq

def extract(s):
    return [int(x) for x in re.findall(r'(-?\d+).?', s)]


def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    # data = [x.rstrip('\n').split('\n') for x in file.read().split('\n\n')]
    # data = [int(s.rstrip('\n')) for s in file]
    data = [s.rstrip('\n') for s in file]

    pos = 50
    cnt = 0
    for line in data:
        m = -1 if line[0] == 'L' else 1
        n = extract(line)[0]
        for _ in range(n):
            n = 1
            opos = pos
            pos = (pos + m * n) % 100
            cnt += (pos == 0)
        # cnt += (n // 100)


    print(cnt)

if __name__ == '__main__':
    main(sys.argv)
