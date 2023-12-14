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

def rot(l):
    l = [list(c) for c in zip(*l)]
    return l

def fslide(m):
    while True:
        nl = slide(m)
        if nl == m:
            break
        m = nl

    return nl



def cycle(l):
    l = fslide(l)
    # print('\n'.join(''.join(r) for r in l))
    # print()
    l = rot(l)
    l = fslide(l)
    l = rot(l)[::-1]
    l = fslide(l)
    # l = l[::-1]
    l = rot(l[::-1])[::-1]
    l = fslide(l)
    l = rot(l[::-1])
    # print('s')
    # print('\n'.join(''.join(r) for r in l))
    # print()
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
