#!/usr/bin/env python3

import sys

def main(args):
    data = [x.split('\n') for x in sys.stdin.read().split('\n\n')]
    ys = [sum(int(y) for y in x if y) for x in data]
    ys.sort()
    print(sum(ys[-3:]))

if __name__ == '__main__':
    main(sys.argv)
