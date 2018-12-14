#!/usr/bin/env python3

import sys

def bit(n, i):
    return (n >> i) & 1

def rule(n):
    d = {}
    states = '.#'
    for i in range(8):
        s = ''.join(states[bit(i, j)] for j in range(2, -1, -1))
        for l in states:
            for r in states:
                d[l+s+r] = states[bit(n, i)]

    return d

def main(args):
    d = rule(int(args[1]))
    for k, v in d.items():
        print('{} => {}'.format(k, v))

if __name__ == '__main__':
    sys.exit(main(sys.argv))
