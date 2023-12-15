#!/usr/bin/env python3

import sys

def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    data = file.read().replace('\n', '').split(',')

    sum = 0
    for node in data:
        val = 0
        for c in node:
            val += ord(c)
            val *= 17
            val %= 256
        print(node, val)
        sum += val

    print(sum)

if __name__ == '__main__':
    main(sys.argv)
