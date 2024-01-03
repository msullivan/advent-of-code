#!/usr/bin/env python3

# This was not the original approach. My original approach shifted one
# at a time and took like a minute. See 14a for that.

import sys

def fslide(l):
    for j in range(len(l[0])):
        open = None
        for i in range(len(l)):
            c = l[i][j]
            xo = open
            if open is None and c == '.':
                open = i
            elif open is not None and c == 'O':
                l[open][j] = 'O'
                l[i][j] = '.'
                open += 1
                change = True
            elif c != '.':
                open = None

    return l


def rot(l):
    l = [list(c) for c in zip(*l[::-1])]
    return l


def cycle(l):
    for _ in range(4):
        l = fslide(l)
        l = rot(l)
    return l


def score(m):
    sum = 0
    for i, row in enumerate(m):
        i = len(m)-i
        for c in row:
            if c == 'O':
                sum += i

    return sum


def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    data = [s.rstrip('\n') for s in file]

    m = [list(s) for s in data]

    i = 0
    seen = {}
    scores = []
    print('\n'.join(''.join(r) for r in m))
    print()

    nl = m
    while True:
        key = tuple(tuple(r) for r in nl)
        sc = score(nl)
        scores.append(sc)

        print(i, sc)
        if key in seen:
            print('???', i)
            break
        seen[key] = i
        nl = cycle(nl)

        i += 1

    loop = i - seen[key]
    tgt = 1000000000
    dst = tgt - seen[key]
    spot = dst % loop
    print(scores[seen[key] + spot])

    # sum = score(m)
    # print(sum)

if __name__ == '__main__':
    main(sys.argv)
