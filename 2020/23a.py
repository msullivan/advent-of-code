#!/usr/bin/env python3

import sys
import re

def extract(s):
    return [int(x) for x in re.findall(r'-?\d+', s)]

def go(l):
    N = len(l)
    up = l[1:4]
    l = [l[0]] + l[4:]
    dest = l[0] - 1
    if dest == 0:
        dest = N
    while dest in up:
        dest -= 1
        if dest == 0:
            dest = N

    idx = l.index(dest)
    l = l[:idx+1] + up + l[idx+1:]
    l = l[1:] + [l[0]]

    return l


def main(args):
    # data = [x.split('\n') for x in sys.stdin.read().split('\n\n')]
    data = [s.strip() for s in sys.stdin]
    cups = [int(x) for x in data[0]]

    for i in range(100):
        cups = go(cups)

    print(cups)
    idx = cups.index(1)
    print(idx)
    cups = cups[idx:] + cups[:idx]
    print(cups)
    print(''.join(str(x) for x in cups)[1:])



if __name__ == '__main__':
    sys.exit(main(sys.argv))
