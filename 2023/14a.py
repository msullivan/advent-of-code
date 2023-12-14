#!/usr/bin/env python3

import sys
import copy

def slide(l):
    l = copy.deepcopy(l)
    for i in range(len(l)-1):
        for j in range(len(l[0])):
            if l[i][j] == '.' and l[i+1][j] == 'O':
                l[i][j] = 'O'
                l[i+1][j] = '.'

    return l

def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    data = [s.rstrip('\n') for s in file]

    m = [list(s) for s in data]

    i = 0
    while True:
        nl = slide(m)
        if nl == m:
            break
        print(i, nl)
        print(nl)
        print(m)
        print([x == y for x, y in zip(nl, m)])
        print(nl[0])
        print(m[0])
        m = nl

        i+= 1

    sum = 0
    for i, row in enumerate(m):
        i = len(m)-i
        for c in row:
            if c == 'O':
                sum += i

    print(sum)

if __name__ == '__main__':
    main(sys.argv)
