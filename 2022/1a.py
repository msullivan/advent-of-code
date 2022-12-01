#!/usr/bin/env python3

import sys

def main(args):
    data = [x.strip().split('\n') for x in sys.stdin.read().split('\n\n')]
    ys = [sum(int(y) for y in x) for x in data]
    print(max(ys))

if __name__ == '__main__':
    main(sys.argv)
